#!/usr/bin/env python3
"""
Fetch all Instagram posts with captions from the @favela_brass account.
Uses the Instagram Graph API via Facebook login.

Usage:
    # Set your token (from Graph API Explorer):
    export IG_ACCESS_TOKEN="your_token_here"

    # Run:
    python3 favelabrass/scripts/fetch_instagram_posts.py

    # Output: favelabrass/imports/instagram_posts.json
"""

import json
import os
import subprocess
import sys
import urllib.request
import urllib.error
from datetime import datetime

IG_ACCOUNT_ID = "17841401244515413"  # @favela_brass
API_VERSION = "v24.0"
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"
SERVER_SSH = "root@45.55.73.116"
SERVER_DB = "/root/favelabrass.db"

# Fields to fetch per post
MEDIA_FIELDS = ",".join([
    "id",
    "caption",
    "media_type",        # IMAGE, VIDEO, CAROUSEL_ALBUM
    "media_url",
    "thumbnail_url",
    "permalink",
    "timestamp",
    "like_count",
    "comments_count",
    "insights.metric(reach,impressions,saved,shares)",
])

STORY_METRICS = "reach,replies,shares,navigation,follows,profile_visits"
ACCOUNT_METRICS = "reach,profile_views,accounts_engaged,total_interactions"


def get_token():
    token = os.environ.get("IG_ACCESS_TOKEN")
    if not token:
        token_file = os.path.expanduser("~/.config/fab-ia/ig_token.txt")
        if os.path.exists(token_file):
            with open(token_file) as f:
                token = f.read().strip()
    if not token:
        print("ERROR: No access token found.")
        print("Set IG_ACCESS_TOKEN env var or save token to ~/.config/fab-ia/ig_token.txt")
        sys.exit(1)
    return token


def api_get(url):
    """Make a GET request to the Graph API."""
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"API Error {e.code}: {error_body}")
        return None


def fetch_all_posts(token):
    """Fetch all posts with pagination."""
    all_posts = []

    # First request
    url = f"{BASE_URL}/{IG_ACCOUNT_ID}/media?fields={MEDIA_FIELDS}&limit=50&access_token={token}"

    page = 1
    while url:
        print(f"  Fetching page {page}...")
        data = api_get(url)

        if not data:
            break

        posts = data.get("data", [])
        all_posts.extend(posts)
        print(f"  Got {len(posts)} posts (total: {len(all_posts)})")

        # Check for next page
        paging = data.get("paging", {})
        url = paging.get("next")
        page += 1

    return all_posts


def fetch_account_info(token):
    """Fetch basic account info."""
    url = f"{BASE_URL}/{IG_ACCOUNT_ID}?fields=username,name,followers_count,media_count&access_token={token}"
    return api_get(url)


def fetch_account_insights(token):
    """Fetch last-30-days account-level insights (reach, profile views, etc)."""
    import time as _time
    now = int(_time.time())
    since = now - 30 * 24 * 60 * 60
    url = (
        f"{BASE_URL}/{IG_ACCOUNT_ID}/insights"
        f"?metric={ACCOUNT_METRICS}"
        f"&period=day&metric_type=total_value"
        f"&since={since}&until={now}"
        f"&access_token={token}"
    )
    return api_get(url)


def fetch_stories(token):
    """Fetch currently-live Stories (24h window) with insights."""
    fields = (
        "id,media_type,permalink,thumbnail_url,timestamp,"
        f"insights.metric({STORY_METRICS})"
    )
    url = f"{BASE_URL}/{IG_ACCOUNT_ID}/stories?fields={fields}&access_token={token}"
    data = api_get(url)
    return data.get("data", []) if data else []


def _flatten_insights(item):
    """Extract `insights.data[*]` into flat `metric_<name>` fields on the dict."""
    insights = item.pop("insights", None)
    if insights and "data" in insights:
        for m in insights["data"]:
            name = m["name"]
            values = m.get("values", [{}])
            val = values[0].get("value", 0) if values else 0
            if isinstance(val, dict):
                # `navigation` returns a breakdown dict
                for sub, sv in val.items():
                    item[f"metric_{name}_{sub}"] = sv
            else:
                item[f"metric_{name}"] = val


def _run_sql_on_server(sql):
    """Run SQL on the server DB. Uses SSH when running locally; direct sqlite3 when on the server."""
    if os.path.exists(SERVER_DB):
        subprocess.run(
            ["sqlite3", SERVER_DB],
            input=sql, text=True, check=True,
        )
    else:
        subprocess.run(
            ["ssh", SERVER_SSH, f"sqlite3 {SERVER_DB}"],
            input=sql, text=True, check=True,
        )


def write_stories_to_db(stories, captured_at):
    """Upsert stories into the server DB."""
    if not stories:
        return 0
    rows = []
    for s in stories:
        def i(k):
            v = s.get(k)
            return int(v) if v is not None else 0
        rows.append((
            s.get("id", ""),
            s.get("timestamp", ""),
            captured_at,
            s.get("media_type", ""),
            s.get("permalink", ""),
            s.get("thumbnail_url", ""),
            i("metric_reach"),
            i("metric_replies"),
            i("metric_shares"),
            i("metric_navigation"),
            i("metric_follows"),
            i("metric_profile_visits"),
        ))
    sql_lines = []
    for r in rows:
        values = ",".join(
            "'" + str(v).replace("'", "''") + "'" if isinstance(v, str) else str(v)
            for v in r
        )
        sql_lines.append(
            f"INSERT OR REPLACE INTO instagram_stories "
            f"(id,posted_at,captured_at,media_type,permalink,thumbnail_url,"
            f"reach,replies,shares,navigation,follows,profile_visits) "
            f"VALUES ({values});"
        )
    sql = "\n".join(sql_lines)
    _run_sql_on_server(sql)
    return len(rows)


def write_account_snapshot_to_db(account, insights, captured_at):
    """Write account-level snapshot to server DB over SSH."""
    metrics_by_name = {}
    for m in (insights or {}).get("data", []):
        val = m.get("total_value", {}).get("value")
        if val is None:
            vals = m.get("values", [])
            val = vals[0].get("value") if vals else None
        metrics_by_name[m["name"]] = int(val) if isinstance(val, (int, float)) else 0

    row = (
        captured_at,
        int(account.get("followers_count") or 0),
        int(account.get("media_count") or 0),
        metrics_by_name.get("reach", 0),
        metrics_by_name.get("profile_views", 0),
        metrics_by_name.get("accounts_engaged", 0),
    )
    sql = (
        "INSERT OR REPLACE INTO instagram_account_snapshots "
        "(captured_at,followers_count,media_count,reach_30d,profile_views_30d,accounts_engaged_30d) "
        f"VALUES ('{row[0]}',{row[1]},{row[2]},{row[3]},{row[4]},{row[5]});"
    )
    _run_sql_on_server(sql)


def save_token(token):
    """Save token to config file for reuse."""
    token_dir = os.path.expanduser("~/.config/fab-ia")
    os.makedirs(token_dir, exist_ok=True)
    token_file = os.path.join(token_dir, "ig_token.txt")
    with open(token_file, "w") as f:
        f.write(token)
    os.chmod(token_file, 0o600)
    print(f"  Token saved to {token_file}")


def main():
    token = get_token()

    # Save token for future use
    save_token(token)

    # Fetch account info
    print("\n📊 Fetching account info...")
    account = fetch_account_info(token)
    if account:
        print(f"  Account: @{account.get('username')}")
        print(f"  Followers: {account.get('followers_count', 'N/A')}")
        print(f"  Total posts: {account.get('media_count', 'N/A')}")

    # Fetch all posts
    print("\n📝 Fetching all posts...")
    posts = fetch_all_posts(token)

    if not posts:
        print("  No posts found. Check your token permissions.")
        sys.exit(1)

    # Process and clean up
    for post in posts:
        _flatten_insights(post)

    # Fetch Stories (live within 24h) and account-level insights
    print("\n📸 Fetching live Stories...")
    stories = fetch_stories(token)
    for s in stories:
        _flatten_insights(s)
    print(f"  Got {len(stories)} live stories")

    print("\n📊 Fetching account-level insights (30d)...")
    account_insights = fetch_account_insights(token)
    if account_insights:
        for m in account_insights.get("data", []):
            tv = m.get("total_value", {})
            print(f"  {m['name']}: {tv.get('value', 'n/a')}")

    captured_at = datetime.now().isoformat()

    # Persist stories and account snapshot to server DB
    try:
        n = write_stories_to_db(stories, captured_at)
        print(f"  Wrote {n} stories to server DB")
    except subprocess.CalledProcessError as e:
        print(f"  Warning: failed to write stories to server DB: {e}")

    try:
        write_account_snapshot_to_db(account, account_insights, captured_at)
        print("  Wrote account snapshot to server DB")
    except subprocess.CalledProcessError as e:
        print(f"  Warning: failed to write account snapshot: {e}")

    # Build output
    output = {
        "account": account,
        "account_insights_30d": account_insights,
        "fetched_at": captured_at,
        "total_posts": len(posts),
        "posts": posts,
        "stories_live": stories,
    }

    # Save
    output_path = os.path.join(os.path.dirname(__file__), "..", "imports", "instagram_posts.json")
    output_path = os.path.normpath(output_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Saved {len(posts)} posts to {output_path}")

    # Quick summary
    types = {}
    for p in posts:
        t = p.get("media_type", "UNKNOWN")
        types[t] = types.get(t, 0) + 1

    print("\n📈 Post types:")
    for t, count in sorted(types.items()):
        print(f"  {t}: {count}")

    # Show date range
    dates = [p.get("timestamp", "") for p in posts if p.get("timestamp")]
    if dates:
        print(f"\n📅 Date range: {min(dates)[:10]} to {max(dates)[:10]}")

    # Show a sample caption
    with_captions = [p for p in posts if p.get("caption")]
    print(f"\n✍️  Posts with captions: {len(with_captions)}/{len(posts)}")


if __name__ == "__main__":
    main()
