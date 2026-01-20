# Favela Brass Style Guide

## Brand Colors (Official)

| Color | Hex | Usage |
|-------|-----|-------|
| **Purple** | `#5A0E7A` | Primary brand color, headers, accents |
| **Dark Purple** | `#3E0B59` | Backgrounds, dark mode base |
| **Yellow** | `#FEF100` | Highlights, CTAs, emphasis |
| **Green** | `#62CC3C` | Positive values, income, success |
| **Black** | `#000000` | Text on light backgrounds, contrast |
| **White** | `#FFFFFF` | Text on dark backgrounds, light mode base |

## Extended Palette

| Color | Hex | Usage |
|-------|-----|-------|
| **Red** | `#E74C3C` | Negative values, expenses, alerts |
| **Muted White** | `rgba(255,255,255,0.6)` | Secondary text, labels |

## Color Applications

### Financial Reports
- **Income/positive:** Green `#62CC3C`
- **Expenses/negative:** Red `#E74C3C`
- **Totals/results:** Yellow `#FEF100`
- **Background:** Dark gradient from `#3E0B59` to `#5A0E7A`

### Gradients
- **Header text:** `linear-gradient(90deg, #FEF100, #62CC3C)` with background-clip
- **Background:** `linear-gradient(135deg, #3E0B59 0%, #5A0E7A 100%)`
- **Highlight boxes:** `linear-gradient(135deg, rgba(98, 204, 60, 0.15), rgba(98, 204, 60, 0.05))`

## Typography

- **Primary font:** `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`
- **Headers:** Bold, gradient or purple `#5A0E7A`
- **Body:** White `#FFFFFF` on dark backgrounds
- **Secondary text:** `rgba(255,255,255,0.6)`

## Component Styles

### Cards
```css
background: rgba(255,255,255,0.05);
border-radius: 16px;
border: 1px solid rgba(255,255,255,0.1);
```

### Sections
```css
background: rgba(255,255,255,0.03);
border-radius: 16px;
padding: 30px;
```

### Section Headers
```css
color: #FEF100;
border-bottom: 1px solid rgba(255,255,255,0.1);
```

## Logo & Assets

- Logo files should be stored in `/favelabrass/assets/`
- Preferred format: SVG for web, PNG for documents

## Language

- Reports for board/external: Portuguese (Brazil)
- Internal documentation: English or Portuguese as appropriate
- Currency format: `R$ 1.234` (Brazilian style with dot as thousands separator)
