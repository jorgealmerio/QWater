![valuetool icon](/images/icon.png)
# QWater 
Hydraulic design and analysis of water supply networks (using EPANET)

QWater is a plugin that uses GHydraulics Plugin (embedded) from Steffen Macke. It allows to design and analyze water supply networks using EPANET. It allows to write EPANET INP files as well as running an EPANET simulation from QGIS complete with loading the result data. QWater contains a function to calculate economic diameters based on given flowrates. The functions are accessible from the Quantum GIS plugin menu and toolbars.


## Tutorial em Português

### Preparando o Qgis
• Criar um novo projeto Qgis.
• Ajustar o sistema de coordenadas do projeto para Sirgas 2000, na faixa meridiana da área 
onde a rede será projetada (por exemplo para Salvador - EPSG: 31984).
• Criar os shapes para os tipos de elementos que compõem a rede (usando o mesmo sistema 
de coordenadas do projeto):
◦ De pontos: Nos, Reservatórios e bombas (se houverem). 
◦ De linhas: trechos
• Salvar o projeto
• Importar a base planialtimétrica a utilizar
• Relacionar os shapes criados aos tipos de informações do Epanet 
(<Complementos/Qwater/Settings>)
◦ Junctions    = Nós
◦ Pipes    = Trechos
◦ Reservoirs    = Reservatórios
◦ Aproveitar para informar a população atendida inicial e final da rede a traçar
◦ A aba “Pipes” está desabilitadas (para versão futura)
◦ Na aba “Calculations Options”, ajustar a velocidade máxima permitida da rede (por 
defeito = 5 m/s)
◦ Clicar no botão “Select” e escolher a configuração de cálculo “template_d-w_lps.inp”
• Clicar em <Complementos/Qwater/Make epanet> e aceitar todas as mensagens
• Para todos os shapes, salvar e sair do modo de edição
•  Clicar em <Projeto/Opções de Aderência> e clicar no ícone de ferradura.

####Traçando a rede

#####Reservatório
• Selecionar o shape de reservatórios e clicar no botão de edição
• Habilitar o rótulo de camada para apresentar o campo “DC_ID”
• Locar todos os reservatórios (nível fixo), preenchendo o campo “HEAD” com a Cota do 
Terreno. Abrir a tabela para verificar que todos os reservatórios tenham cota.
• Alterar a apresentação do rótulo para ==> 'Nó: ' || "DC_ID"  ||  '\n Cota= ' || "HEAD" 
• Salvar o shape e sair do modo de edição
#####Nós
• Selecionar o shape de nós e clicar no botão de edição
• Habilitar o rótulo de camada para apresentar o campo “DC_ID”
• Locar todos os nós
• Preencher o campo “ELEVATION” com a Cota do Terreno. Abrir a tabela para verificar que 
todos os nós tenham cota.
• Alterar a apresentação do rótulo para ==> 'Nó: ' || "DC_ID"  ||  '\n Cota= ' || "ELEVATION"
• Salvar o shape e sair do modo de edição
#####Trechos
• Selecionar o shape de trechos e clicar no botão de edição
• Habilitar o rótulo de camada para apresentar o campo “DC_ID”
• Traçar todos os trechos conforme a direção do fluxo prevista (de montante para jusante). Um
trecho e composto por uma polilinha que inicia no nó de montante e finaliza no nó de 
jusante. Observação: Botão direito para finalizar. Tecla Esc para cancelar a edição em curso.
• Calcular o comprimento dos trechos da rede.
◦ Clicar no botão da calculadora (ábaco).
◦ Clicar em “Atualiza um campo existente” e selecionar o campo “LENGTH”.
◦ Em “Geometria” selecionar a função “$length” e clicar em OK. Abrir a tabela para 
verificar que tenha preenchido o campo “LENGTH” com o comprimento de cada trecho 
em metros.
◦ Clicar no botão OK.
• Atribuir um diâmetro preliminar aos trechos.
◦ Clicar no botão da calculadora (ábaco).
◦ Clicar em “Atualiza um campo existente” e selecionar o campo “DIAMETER”.
◦ Na área de edição da calculadora digitar 100 (diâmetro interno 100 mm).
◦ Clicar no botão OK. Verificar que tenha preenchido em cada trecho o campo 
“DIAMETER” com o valor provisório (igual a 100 mm).
• Completar informações de rugosidade, coeficiente de perda pontual e status dos trechos
◦ Atualizar o campo “ROUGHNESS” (rugosidade do tubo, em função do material, por 
exemplo 0,1 mm) com a calculadora.
◦ Atualizar o campo “MINORLOSS” (coef de perda pontual, se não for considerar adotar 
igual a 0) com a calculadora
◦ Atualizar o campo “STATUS” (tubo aberto = ‘OPEN’ ou fechado = ‘CLOSE’) com a 
calculadora.
• Salvar o shape e sair do modo de edição.
####Calculando a demanda
• Clicar em <Complementos/Qwater/Calc Flow>. Deve aparecer a mensagem “Demanda nos 
nós calculada com sucesso”. Esta rotina calcula a vazão unitária a partir da demanda 
distribuída alocando em cada nó, o produto da vazão unitária vezes a metade da extensão 
dos trechos conectados ao nó.
• Salvar o shape de nós e sair do modo de edição.
####Simulação preliminar da rede
• Clicar em <Complementos/Qwater/Run Epanet Simulation> e aguardar a apresentação da 
mensagem. Se a mensagem indicar a ocorrência de erros, analisar as indicações dos erros na 
aba “Report”. 
• Se a simulação foi bem-sucedida, salvar os shapes e sair do modo de edição.
####Otimização dos diâmetros da rede
• Clicar em <Complementos/Qwater/Calculate economics diameter> e confirme a mensagem 
de substituir os valores do campo “DIAMETER”.
• Salvar os shapes e sair do modo de edição.
####Simulação da rede com os diâmetros otimizados
• Clicar em <Complementos/Qwater/Run Epanet Simulation> e aguardar a apresentação da 
mensagem.
• Se a simulação foi bem-sucedida, salvar os shapes e sair do modo de edição.
####Ajustes finais
• Salvar o projeto
• Salvar o projeto (sugestão nome anterior mais result, pe: Rede_result.qgs).
• Clicar em <Complementos/Qwater/Load default Stiles>.
• Analisar os resultados e proceder ao ajuste fino de altitude do reservatório, diâmetros de 
trechos.
• Rodar a rede novamente (<Complementos/Qwater/Run Epanet Simulation>)
• Salvar os shapes e sair do modo de edição.
• Salvar o projeto.
• Exportar a rede projetada para o formato dxf. Adotar uma escala compatível.

