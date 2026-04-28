# Iris x Tom Checkin

**Date:** 2026-02-27T14:31:06-03:00

## Summary

A reunião tratou da identificação e correção de problemas no portal de presenças, no fluxo de comunicação via bot/Slack e na conciliação das horas e presenças dos professores. Após checagens iniciais de conexão e atualização de participantes, foi mencionado que uma ausência por doença na equipe vinha afetando a comunicação informal. A equipe revisou o fluxo técnico: o usuário envia mensagem ao bot, o cloud/bot registra e repassa as mensagens, e Tom analisa e aciona correções, solicitando testes e retorno da Iris. Identificou-se limitação do bot para receber screenshots no chat, então a orientação passou a ser envio de prints por WhatsApp ou cópia das mensagens para o Slack quando necessário acelerar o diagnóstico.

Foi constatado um erro persistente na turma "banda roxa" no dia 18 com porcentagem incorreta; Iris ficará responsável por orientar professores e sinalizar erros, enquanto Tom encaminhará as sinalizações ao chat/cloud e consultará Cláudio sobre o caso. A discussão também abordou procedimentos de auditoria das horas, a necessidade de visualização por professor, relatórios mensais que Tom pode gerar, registro de ensaios e aulas particulares, e dúvidas sobre duplicidade em eventos/produção. Houve alinhamento sobre atualização de agenda, problemas de sincronização e a rotina de conferência mensal das horas; matrículas via escolas serão importadas por planilha enviada a Tom e apresentações/fichas deverão ser incluídas no sistema em seguida.

## Action Items

- [ ] Iris Nascimento: Orientar os professores na próxima semana sobre o preenchimento de presenças e pedir que sinalizem qualquer erro
- [ ] Tom Ashe: Encaminhar para o chat/Cloud as sinalizações de erro enviadas pela Iris assim que receber o alerta
- [ ] Tom Ashe: Perguntar ao Cláudio sobre a inconsistência da presença da banda roxa no dia 18
- [ ] Iris Nascimento: Enviar prints ou descrições detalhadas do erro da turma “banda roxa” para o Tom via WhatsApp ou Slack direct
- [ ] Tom Ashe: Ativar ou acompanhar a habilitação do envio de arquivos pelo bot para permitir screenshots no chat
- [ ] Tom Ashe: Verificar e confirmar que todos os dados de janeiro estão corretos no sistema
- [ ] Iris Nascimento: Fazer a comparação entre as horas que a Raíssa recebeu e os registros do sistema para fevereiro
- [ ] Tom Ashe: Gerar relatório com o total de horas que todos os professores fizeram no mês anterior e enviar/ou disponibilizar para conferência
- [ ] Tom Ashe: Verificar e melhorar o registro de ensaios no sistema para que ensaios extras apareçam corretamente
- [ ] Iris Nascimento: Não excluir eventos até receber confirmação; aguardar confirmação da Zola antes de remover
- [ ] Tom Ashe: Investigar e corrigir a falha de atualização da agenda que impede alterações aparecerem para todos usuários
- [ ] Tom Ashe: Colocar a atualização da agenda no cloud para forçar sincronização entre usuários
- [ ] Iris Nascimento: Atualizar ou confirmar as presenças, agenda e horários para permitir a auditoria regular
- [ ] Tom Ashe: Receber a planilha de matrículas enviada por Iris e importar os dados para o sistema/cloud

## Topics Discussed

- O fluxo de atendimento passa pelo bot e o Tom monitora as mensagens para consertos e pedir testes de validação
- O bot/Cloud registra e processa respostas e Tom envia retorno ao usuário solicitando testes adicionais
- Há incerteza histórica sobre recebimento de screenshots pelo bot no Slack, mas foi informado que prints funcionam em outros canais e que há trabalho para habilitar upload de arquivos
- Iris começará a orientar professores para preencher presenças na semana seguinte e pediu que sinalizem qualquer erro observado
- Tom se compromete a encaminhar sinalizações de erro para o chat/Cloud e registrar os casos para tratamento
- A turma “banda roxa” teve um registro de presença com percentual incorreto referente ao dia 18 que precisa investigação
- Comunicação rápida entre Iris e Tom ficará preferencialmente por Slack/WhatsApp para envio de prints e cópias de mensagens até o bot receber arquivos
- É necessário comparar mensalmente as horas que os professores enviam com as horas registradas no sistema.
- Uma visualização histórica por professor facilitaria a auditoria das aulas e reduziria o trabalho de conferir aluno a aluno.
- Há um relatório que Tom pode gerar rapidamente para somar horas dos professores do mês anterior.
- Existe uma árvore de auditoria no sistema que foi identificada durante a reunião.
- Cancelamentos devem ser excluídos do sistema somente após confirmação dos envolvidos.
- Houve falha de sincronização da agenda que impede ver alterações imediatamente para todos os usuários.
- Matrículas das escolas serão enviadas via Google Forms e depois importadas por planilha para o sistema.

## Key Questions

- O fluxo funciona enviando a mensagem para o bot e ele te encaminha as informações?
- O bot/serviço entende screenshots (prints)?
- É possível editar as datas das presenças na interface?
- Você se referia a fevereiro?
- Como será feita a conferência das horas enviadas pelos professores?
- Todos os links usam a mesma senha ou senhas diferentes?

## Participants

- Iris Nascimento
- Tom Ashe

## Transcript

**Iris Nascimento** [29536891974:44]: Tchau. É isso aí! Tá me ouvindo?

**UNKNOWN_SPEAKER** [29536899590:35]: Oi, Iris, tudo bem?

**Iris Nascimento** [29536899623:34]: Tudo bem, boa tarde. O internet tá meio ruim, aí eu tô sem vídeo.

**UNKNOWN_SPEAKER** [29536899739:01]: Tá caindo direto.

**Iris Nascimento** [29536899763:45]: Ah, caraca, é muito chuva, né? É, fica solando. Quando chove, assim, é certo.

**UNKNOWN_SPEAKER** [29536899879:12]: Tudo bem?

**UNKNOWN_SPEAKER** [29536899895:41]: Tudo.

**Tom Ashe** [29536899903:56]: Tudo aqui e você? Tudo bem também. Na verdade, eu peguei... Eu já te falei, o Tiago ficou doente.

**UNKNOWN_SPEAKER** [29536900050:07]: Ficou doente?

**Tom Ashe** [29536900063:58]: É, sim.

**Tom Ashe** [29536900077:48]: Febre, sabe? Só febre? Febre, mas não é virose, esse tipo de coisa, mas depois de dois dias com febre alta, ele foi no hospital, essas coisas. Ah, sim. E depois também se pegou, depois eu peguei. Então, então... Eita!

**Tom Ashe** [29536900354:31]: Mas eu tô melhorando.

**Tom Ashe** [29536900382:11]: Foi a virose, né?

**Tom Ashe** [29536900409:51]: É, esse tipo de coisa. Mas eu tô... Você tem coisa para ver comigo? Então, só ver a questão lá do portal.

**UNKNOWN_SPEAKER** [29536900622:00]: Eu falei lá com...

**Iris Nascimento** [29536900665:30]: Eu queria até entender como é que funciona. Eu mando a mensagem para o chat, bot, e aí ele te encaminha? Mesmo já resolve.

**Tom Ashe** [29536900932:16]: O que acontece? Você manda mensagem para o bot e o ciclo... Eu vou estar trabalhando com o bot da próxima rodada. Eu vou para o bot e eu falo, tem mensagem da Iris? Aí ele respondeu, ele vai checar as mensagens dele. Ele vai falar assim, ela testou isso e não funcionou, ela tá relatando isso. Aí eu vou ver o que é que tá acontecendo. Ah, eu vi, tem esse problema, vou consertar aqui, beleza. Agora eu vou mandar outra mensagem para ela, aí eu vou pedir para ela testar e me dar um retorno.

 Aí eu falo, beleza. Aí depois, né, depois de um tempinho, depois eu vejo quando você responde o bot, e quando você responder, É, eu mando para o bot, eu falo, ô bot, a Insta respondeu, aí ele pega a sua resposta, ele processa, manda mensagem para você de novo, entendeu?

**Iris Nascimento** [29536902033:50]: Então, está nesse ciclo. Sim, entendi. Então, você, de qualquer forma, tem que fazer um trabalho aí de ajustar no sistema.

**Tom Ashe** [29536902180:24]: Sim, eu alerto o cloud quando você responde, ele processa isso e te manda outra mensagem, entendeu?

**UNKNOWN_SPEAKER** [29536902316:37]: Entendi.

**Iris Nascimento** [29536902326:06]: Beleza. Então, eu falei com ele lá das justificativas, ele falou que tinha resolvido, mas não resolveu. Então, é só...

**Tom Ashe** [29536902515:39]: Sim, aí manda para ele. E você pode mandar print para ele também, eu acho.

**UNKNOWN_SPEAKER** [29536902657:49]: Ah, ele entende?

**Tom Ashe** [29536902686:15]: Sim, sim.

**Tom Ashe** [29536902705:12]: Aqui, ele entende print, com certeza. A única que... Mandar print pelo Slack. A única incógnita é se ele recebe print pelo Slack. Mas eu acho que recebe. E qualquer coisa pode mandar também. Mas a coisa para agilizar nosso tempo, manda diretamente para ele, sabe? Não, não, claro. Ainda não está funcionando. Aí ele vai, ah, então, teria que ser outra coisa.

**UNKNOWN_SPEAKER** [29536903207:36]: Tá. E insistir até resolver, né?

**Iris Nascimento** [29536903260:22]: É mágico, sim.

**Iris Nascimento** [29536903279:54]: Deixa eu atualizar, o Chanso, ele já tá usando o Slack, tá funcionando, deu certo. Ele fez as presenças dessa semana. E aí eu sugeri dele me mandar no meu chat. Porque quando ele confirma a presença, eu recebo a notificação que a presença foi salva. Ah, tá.

**UNKNOWN_SPEAKER** [29536903592:20]: No meu chat.

**Iris Nascimento** [29536903611:52]: Aí eu consigo acompanhar, conforme os professores vão dando a presença, eu vejo se tá salvando.

**Iris Nascimento** [29536903716:09]: Perfeito, perfeito.

**Iris Nascimento** [29536903730:02]: Aí, semana que vem, eu vou fazer esse processo. O Chancelor já deu uma orientação para ele, ontem, mas acho que está dando tudo certo com ele, porque ele só tem duas aulas na semana, tem que ver agora de sábado, como é que vai ser amanhã. Mas, aí, na próxima semana, já vou começar a passar essas orientações para os professores preencherem.

**UNKNOWN_SPEAKER** [29536904167:20]: Sim.

**Iris Nascimento** [29536904176:15]: Qualquer erro, se eles sentirem que está com algum erro, alguma coisa, eu pedi para eles sempre observarem todas as informações. Sim. E me trazer, me sinalizar.

**Tom Ashe** [29536904388:16]: Assim que dá erro, me sinaliza que eu já mando para o chat e já deixei registrado. Não, isso é ótimo. Aí a gente consegue... Mas está estável agora, né? O sistema? As presenças, sim.

**Iris Nascimento** [29536904668:30]: Por exemplo, aqui ainda estou vendo o erro das presenças da banda roxa, que está dando 79, esse aqui. Esse aqui do dia 18, todos presentes, mas aqui está dando menos.

**Tom Ashe** [29536904944:33]: Então, deixa eu só perguntar para o Cláudio aqui.

**Iris Nascimento** [29536905024:42]: Aí eu fico na dúvida de como Exemplificar isso para ele entender. A presença da banda roxa de 18 não está constando porcentagem, alguma coisa assim.

**Tom Ashe** [29536905292:47]: Isso, imagine se você precisava mandar uma mensagem para mim. Exatamente como você mandou para mim. Pera aí, pera aí. Aqui. Ah, não. Ele não recebe screenshots pelo chat.

**Iris Nascimento** [29536906172:57]: Não, mas eu posso escrever, não tem problema.

**Tom Ashe** [29536906275:54]: Mandei mensagem para ele aqui, mas ele não me confirmou que recebeu.

**Iris Nascimento** [29536906430:19]: Aqui também, na parte de saídas, fica assim. Você está A internet está lenta. Acho que você não consegue ver. Quando eu abro aqui, na seleção do aluno, você está vendo branco?

**Tom Ashe** [29536906772:01]: Não, eu só vejo que nada que está acontecendo. Vou dar um print aqui.

**Iris Nascimento** [29536906975:24]: Para você ver Nessa parte aqui, na seleção dos alunos, está assim Está aparecendo assim, está vendo? Ele tem que rolar em cima do branco Sim, não tem problema.

**Tom Ashe** [29536907477:40]: Não, beleza. Eu posso ter um problema com esse diálogo. Acho que é isso, por enquanto, a questão das justificativas e isso, das saídas. Essas coisas com print, você pode me mandar por WhatsApp. Me mandar por WhatsApp. Oh, WhatsApp é o Slack. Mas me manda... E eu copio sua mensagem e mando para ele direto, se tem alguma coisa que precisa de print. Porque, realmente, se precisar de um print, ele consegue ver sim, consegue ver muito bem.



**Iris Nascimento** [29536908326:46]: mandei para você. Você tinha falado sobre conseguir editar as datas das presenças, mas isso acho que ainda não está habilitado, por exemplo, aqui eu não consigo mexer. Então, manda para baixo, eu não consigo clicar, eu não consigo eu vou então mandando para ele acho que a gente pode seguir assim se você não tiver recebendo as mensagens aí eu copio e colo para você no direct do slack mesmo sim eu acho que ele tá recebendo mas depois confere se ele se eu mandei agora falando o problema da banda roxa.



**Tom Ashe** [29536909256:50]: Depois você confere se chegou pra você. Ele tá, no momento tá tramitando, tramitando, porque ele tá tentando colocar para você poder, poder mandar arquivo. Seria muito bom.

**Iris Nascimento** [29536909598:49]: É, mas tá, pode ser. Tu diz dos prints.

**Tom Ashe** [29536909697:46]: Dos prints.

**Tom Ashe** [29536909715:01]: Eu posso descrever também, não tem problema não.

**Iris Nascimento** [29536909784:01]: Nesse caso aí do layout, que realmente é difícil de escrever, né?

**Tom Ashe** [29536909887:30]: Mas pode ir. Mas é isso, parece que... A última coisa que você mandou pra ele foi antes disso, né? Foi uns 1,5, né?

**Iris Nascimento** [29536910094:29]: 1,35, coisa assim. Foi... A última coisa que eu mandei foi 10...

**Tom Ashe** [29536910233:11]: mandei agora uma coisa, agora é pouco e antes disso eu mandei 10,40 que é o erro das justificativas ele tá pegando, você pode confiar nesse canal aparece no meu Slack quando você manda, aí eu atualizo ele. Eu falo, olha lá, você tem mensagem.

**Iris Nascimento** [29536910801:09]: Então tá, eu acho que talvez essas reuniões então nem façam mais, não tenha tanta necessidade agora, né, se a gente for usar Esse canal de comunicação.

**Tom Ashe** [29536911097:38]: Eu acho que seria bom a gente ter só uma coisa rapidinho, que não é só isso. Eu acho que vale a pena a gente ter esse ponto de contato. Não tem que ser muito longo, mas... Tá, beleza. Ok. Tá, tá. Agora você pode mandar screenshot.

**Tom Ashe** [29536911509:34]: a imagem.

**Tom Ashe** [29536911536:35]: Ele conseguiu? Sim. Então, então... Então, essa parte tá bom. O que eu queria ver contigo, são duas coisas. Primeira coisa é que, só pra deixar claro, a gente quer, mesmo a gente está passando o sistema para os professores agora, mas todos os dados de janeiro certinhos, todos os presentes certinhos no nosso sistema. Fevereiro, né, você diz?

**UNKNOWN_SPEAKER** [29536912189:23]: Fevereiro, Fama.

**Tom Ashe** [29536912205:17]: Fevereiro. Ok. Os professores estão mandando suas horas para a Raíssa. Ela pediu para eles mandarem o número de horas, mas a gente tem que conferir isso contra o sistema, sabe?

**Iris Nascimento** [29536912457:44]: Seria bom ter, então, esse horário de cada professor, né?

**Iris Nascimento** [29536912530:57]: Porque eu acho que eu não tenho acesso a isso aqui. Ou isso fica, tipo, financeiro, alguma coisa assim. Ah, eu vou ver.

**Tom Ashe** [29536912699:21]: Eu vou ver isso. Mas o importante...

**Iris Nascimento** [29536912750:36]: Eu posso fazer essa comparação também.

**Tom Ashe** [29536912794:32]: Mas você pode editar com a raiz, sabe?

**Iris Nascimento** [29536912853:07]: Mas aí ela vai me perguntar como é que vai ser assim?

**Tom Ashe** [29536912937:18]: Os professores mandam as horas para ela e depois... Mas como é que vai ser a conferência?

**Iris Nascimento** [29536913051:00]: Ela vai me conferir comigo?

**Tom Ashe** [29536913084:26]: Ela não vai precisar conferir contigo, ela vai, porque a conferência vai ser antes o que o professor falar e o que está no sistema, entendeu?

**Iris Nascimento** [29536913258:19]: Então, é isso que eu tô dizendo, talvez seja bom ter uma aba de horas de professores.

**Tom Ashe** [29536913378:47]: Porque essa está na parte das presenças, etc. Poderia ser, mas as ois dos professores é mais uma parte das finanças, do fólio de pagamento, sabe? Então...

**Iris Nascimento** [29536913614:08]: Então, mas é isso que a Raíssa vai conferir, não é?

**Tom Ashe** [29536913710:01]: A questão do pagamento. Exatamente, mas a gente tem outros sites para finanças, entendeu?

**Iris Nascimento** [29536913832:02]: Bom, deixa eu pensar Como é que eu posso explicar? Eu vou fazer a conferência na questão das aulas, dos professores, está batendo com o que eles estão registrando. Com o que foi registrado, no caso, fevereiro. No final, no final, não vou conseguir ver o total de horas, entendeu?

**Tom Ashe** [29536914287:49]: Mas a coisa que... O que a gente precisa de você é de ver que as presenças estão certas. Entendi.

**Iris Nascimento** [29536914465:41]: Para você conferir... Porque, por exemplo, se o professor falou, dei tanto de aula, sei lá, 10 horas de aula, e no sistema estiver constando 10 horas de aula, teoricamente está correto. E aí, quando tem divergência, eu consigo ir olhando para poder ver. Porque se eu for olhar toda, tipo, for olhar por professor, vamos ver se eu consigo aqui. Aqui também não parece.

**UNKNOWN_SPEAKER** [29536915068:24]: Ok, tudo bem.

**Iris Nascimento** [29536915096:39]: É porque, por exemplo, o ideal seria eu clicar no professor histórico aqui das aulas do mês.

**Tom Ashe** [29536915246:41]: Sim, mas a questão é que a gente tem isso, mas não seria problema ser sua, entendeu? Porque quem tá organizando, pode errar isso.

**Iris Nascimento** [29536915413:12]: Não, entendi, mas aí tem que, o sistema tem que refletir o que ela recebe de informação, é isso que eu tô querendo tentar entrar no, como é que a gente faz isso para poder essa informação para ela também.

**Tom Ashe** [29536915699:54]: Isso, mas isso está tranquilo, porque eu posso fazer isso, sabe? Eu posso perguntar aqui quantas horas que todos os professores fizeram no mês passado, rapidinho aqui vai me dar um relatório, mas essa parte, porque é um desgaste para você, o único problema aí, a questão seria para avaliar se tivermos divergência, mas o importante, o que a gente precisa diversificar é que as horas das aulas são certas.

 Registradas, sim.

**Iris Nascimento** [29536916314:04]: Estou registrando tudo, só que a questão mesmo, a dificuldade é a conferência, porque, por exemplo, se eu for conferir, se eu clicar aluno por aluno para ver todas as aulas que ele foi, vai dar um trabalhão. Mas, por exemplo, se tiver aqui o histórico do professor, aulas que o professor deu, já fica mais fácil eu conseguir analisar, que aí eu consigo analisar por professor ao invés de analisar por aluno.



**Tom Ashe** [29536916862:42]: Não sei se deu para entender. Sim, eu estava querendo alguma coisa para você poder fazer esse auditório, não dar por professor.

**Iris Nascimento** [29536917044:17]: E isso, se for por professor, fica mais fácil, porque aí vai ter o histórico das aulas do professor ali e vai estar registrado a aula do aluno naturalmente.

**Tom Ashe** [29536917296:27]: É, se você vai, você tá vendo a aba pro professor, né? Isso. Então, tá dando os registros recentes.

**Tom Ashe** [29536917461:40]: É, só os recentes.

**Tom Ashe** [29536917496:36]: O problema aqui é que não dá para ver o resumo do mês.

**UNKNOWN_SPEAKER** [29536917617:07]: Isso, exatamente.

**Tom Ashe** [29536917635:39]: Mas, se você escolar para baixo, tá vendo aulas particulares para o professor?

**UNKNOWN_SPEAKER** [29536917756:10]: Ah, sim.

**Tom Ashe** [29536917774:43]: Clique no nome do professor aí. Tá vendo?

**Iris Nascimento** [29536917848:53]: Vou clicar no Chamos. Ah, beleza.

**Tom Ashe** [29536917979:50]: Dá pra ver sim agora. É, eu acho que sim. Então, com isso, eu acho que... Mas a coisa que também tem a questão dos... Eu tenho que ver essa questão dos ensaios. Dá pra gravar ensaios extras? Eu acho que a gente ainda tem que melhorar essa parte de poder avaregar o que aconteceu, né? Eu ainda tô...

**Iris Nascimento** [29536918345:23]: O chanso não tem os ensaios dele, mas tem as aulas particulares.

**Tom Ashe** [29536918419:52]: Então, tem que ter ensaios aí. Isso é... Eu acho que ainda não está 100% isso. Auditoria. Você está com uma árvore de auditoria aí?

**Iris Nascimento** [29536918757:20]: Sim, sim.

**UNKNOWN_SPEAKER** [29536918854:47]: Ah, então tá aí, né? Já fez.

**Iris Nascimento** [29536918934:34]: Ah, percebi. Esse eu não tinha visto ainda.

**Tom Ashe** [29536919025:45]: Ah, tá. Que é o que falta preencher. Como compare atividades desesperadas com as presenças registradas, exatamente. Mas será que está certo? Então, agora, a coisa geral que eu queria falar, aí você pode ver isso, mas o que é... Lembro, no final do ano passado, a gente estava falando dali, ficar mais na frente com as crianças e você mais na questão da code, do sistema, etc., etc. Então, basicamente, o que seria muito bom era você...

 Era de você ficar... Vamos, Ana, só para eu não esquecer as alturas que eu tenho que... Mas é esse trabalho que eu preciso, sabe? Qualquer coisa que você sente que pode ser melhor, se fala, mas os lados um pouquinho. E a... Eu dei uma olhada, sim.

**UNKNOWN_SPEAKER** [29536920957:05]: No portal, né?

**Tom Ashe** [29536920988:09]: Mas aí, eu preciso que quando vocês... Essa é a nossa agenda agora, sabe? Aí, quando mudar alguma coisa, tem que estar aqui, certo? E dá pra clicar as coisas e confirmar, sabe? Posso confirmar aqui, então. Tá vendo aqui que dá para editar? Então, o que... O que eu preciso é... Aí a gente... Esses dados, a equipe precisa... Se a gente tiver essas dadas, né, tudo atualizado, se o baixo estiver com dúvida, me fala, ou fala pra gente, e que a gente tem que...

 Isso tem que ser uma referência confiável para as pessoas. Tá. E Savarce, eles mudaram as datas.

**Iris Nascimento** [29536922261:39]: Esse aqui é... Sería cancelado. Seria a Zola dia 06 de 03.

**Tom Ashe** [29536922368:51]: O Wesley agora falou que seria possível. Mas a própria Zola não me responde. A própria Natasha não me responde quando eu tô falando pra ela. O problema é que vai ficar muito em cima na hora.

**UNKNOWN_SPEAKER** [29536922653:11]: Exatamente.

**Tom Ashe** [29536922660:53]: Então acaba caindo por isso. Será que ela vai responder agora mesmo? Tá, então vou esperar.

**Iris Nascimento** [29536922802:14]: Aí eu posso, nesse caso aqui, excluir. Ou cancelar. É, tem que ser excluir. Calma, deixa ela confirmar. Não, sim, não vou mexer não, mas se fosse o caso, seria excluir.

**Tom Ashe** [29536923074:31]: Se realmente ficar cancelado, aí excluir. Mas como a gente não sabe se eles vão...

**UNKNOWN_SPEAKER** [29536923234:16]: Tá.

**UNKNOWN_SPEAKER** [29536923243:13]: Bagbrash, tá confirmado.

**Iris Nascimento** [29536923270:04]: Não vai ser de 11, né? Vai ser de 18.

**Tom Ashe** [29536923359:31]: Mas eu já atualizei lá, não? Não atualizei ainda? Não, tá 11 ainda. Isso tá estranho, porque eu achei que atualizei lá. Deixa eu ver.

**Iris Nascimento** [29536923609:55]: Atualizei agora, 18.

**Tom Ashe** [29536923650:54]: Ainda está mostrando 11, então tem problema aí da atualização da agenda. Vou colocar lá no cloud. Mas são essas coisas, a gente...

**Iris Nascimento** [29536923965:10]: É, por exemplo, está confirmado, então, dia 3.

**Tom Ashe** [29536924103:11]: Mas eu tenho que... Ah, mas não estão registrando. Vou colocar aqui. Da agenda.

**Iris Nascimento** [29536924349:08]: Então, na sexta também a gente pode fazer essa atualização da agenda, né, porque normalmente vocês decidem isso na reunião de liderança, ou na própria terça, né? Ok, desculpa, qual é essa? Sobre a atualização da agenda, eu esse retorno após a reunião de liderança que vocês definiram.

**Tom Ashe** [29536924896:46]: Sim, mas também na pedagógica também, qualquer coisa que vocês resolvem, que eu também posso fazer diretamente lá, mas é importante que se tiver alguma coisa na pedagógica também, as frases, o importante é que isso fica atualizado, que todo mundo te olhe. Tá. Então acho que é isso, parece que não tá atualizando.

**Iris Nascimento** [29536925745:27]: Deixa eu fazer um refresh. É aqui, eu atualizei agora também e continua dia 11. Beleza, então acho que...

**Iris Nascimento** [29536925991:57]: Felicidades, Abbas, que eu sou responsável.

**Iris Nascimento** [29536926069:47]: Então, são presenças. Eu tenho que conferir tudo. Agenda e os horários.

**Tom Ashe** [29536926213:31]: Por enquanto, mas indo mais para frente, era isso que eu estava querendo de você ver, não que você tem que atualizar tudo, mas você tem que ver o que está atualizado, entendeu? Essa é a função. Por exemplo, a lojinha está tudo certo, vai chegando lá aos poucos, sabe? Mas, por exemplo, instrumentos. Eu não sei se instrumentos apareceu ainda, mas a ideia é de você estar fazendo esse cheque para ver se as coisas estão em dia, em termos dos dados.

 Por exemplo, horários. Com certeza, os horários das aulas têm que estar certos, horários, presença, agenda, planejamento mais ou menos, a lojinha, responsabilidade da raiz e produção, acho que é só de ver que está em dia, lanches, lanches Eventos, é outra coisa. É porque tem agenda e eventos, tem duas coisas diferentes. É, mas eventos é mais para... Produção. Produção, exatamente. Para as fichas. Ah, beleza.

 Mas ainda... Sim, ainda está... Deixa eu ver. Ah, sim. Não, está meio duplicado. Eu vou ver isso. Eventos devem... Não, eventos é mais para detalhar os eventos.

**Iris Nascimento** [29536928369:11]: É, mais de produção mesmo, né?

**Tom Ashe** [29536928416:35]: Mais informações. Ah, sim, sim.

**Iris Nascimento** [29536928456:05]: É isso, realmente. Que nem a... A ficha, né? É, o cronograma.

**Tom Ashe** [29536928550:54]: Isso, não é exatamente o que a gente quer. Beleza. Mas acho que... Então, acho que tá... Para a gente hoje tá o quê? A gente só tem que tá vendo esses bugs, né?

**Iris Nascimento** [29536928819:32]: É, toda... Todos os links aqui, é a mesma senha ou é uma senha para cada coisa?

**UNKNOWN_SPEAKER** [29536928938:31]: Ah, tem senhas diferentes para diferentes coisas.

**Iris Nascimento** [29536928986:36]: Por exemplo, o guia do Slack, professores. Se eu copiar esse link aqui e mandar para eles funcionar?

**Tom Ashe** [29536929110:14]: Não, mas deixa o guia do Slack por enquanto.

**UNKNOWN_SPEAKER** [29536929172:03]: Sem usar então?

**Tom Ashe** [29536929192:40]: Deixa eu ver o que tem lá agora. Ah, não. Não, mas tá bom. Não, mas os professores não vão conseguir entrar nisso, porque eles precisam de login Favela Brás para entrar no portal.

**Iris Nascimento** [29536929499:46]: Ah, sim. Tá. Então, eu mando para eles alguma informação.

**UNKNOWN_SPEAKER** [29536929569:03]: É, sim.

**Iris Nascimento** [29536929582:55]: Mas é só a presença, então, acho que, por enquanto, é tranquilo. A aula extra é a mesma que eu vou preencher, eu acho.

**Tom Ashe** [29536929749:11]: Sim, mas é isso. Aí, no final de fevereiro, vou pedir para o sistema comparar as horas que os professores mandaram com as horas que a gente tem no sistema. E vai ser assim todo mês. E você recebeu a coisa sobre colocar-se alunos projeto, etc, etc.

**Iris Nascimento** [29536930268:41]: Então, não coloquei nenhuma saída porque não tem ninguém para sair, mas eu dei uma olhada lá.

**UNKNOWN_SPEAKER** [29536930394:29]: O Bernardo Luca?

**Iris Nascimento** [29536930416:40]: Já está, como já tinha saído, já está evadido aqui, no histórico.

**Tom Ashe** [29536930505:28]: Interessante. Você recebeu uma mensagem? Acho que você colocou, não? É, eu acho que eu talvez coloquei lá.

**Iris Nascimento** [29536930638:40]: Está aqui, a Bernardo evadido.

**Tom Ashe** [29536930675:40]: Aí eu não mexi, só olhei aqui, mas você recebeu uma mensagem do chat do bot sobre isso que ele ia te mandar? Mandou, vi sim, ele falou ele me explicou então é isso aí qualquer um que sai a gente registra aqui sim aí vai ficar quente quando a gente começa nas escolas né que pode ter geralmente E a questão da matrícula das escolas, como é que ficaria? A gente vai botar aqui nos links ou vai ficar separado?

 Vai ser via Google Forms, né? Aí você me manda a planilha planilha com a lista dos alunos, eu coloco no cloud e vai para o sistema. Então, próximos passos é...

**Iris Nascimento** [29536931886:01]: Será que vai aguentar?

**Tom Ashe** [29536931931:53]: O sistema vai aguentar?

**Tom Ashe** [29536931977:44]: Sim, tranquilo. É só me mandar os...

**Tom Ashe** [29536932057:58]: A planilha.

**Tom Ashe** [29536932080:54]: A planilha dos...

**Iris Nascimento** [29536932150:06]: Tá bom.

**UNKNOWN_SPEAKER** [29536932167:43]: Beleza. Tá, beleza.

**Iris Nascimento** [29536932194:08]: Aí tem aquela questão também das apresentações, tem que incluir depois.

**Tom Ashe** [29536932290:59]: Ah, apresentações e apresentações, tem uma na tela aqui. Deixa eu fazer aqui isso. Isso vai ficar na... Vai ter que ficar pra só aqui mesmo. Mas a gente faz sim. Terceirinho, então?

**UNKNOWN_SPEAKER** [29536932581:33]: Tudo certo.

**Iris Nascimento** [29536932599:18]: Obrigado, Elis.

**UNKNOWN_SPEAKER** [29536932633:37]: Pra você.
