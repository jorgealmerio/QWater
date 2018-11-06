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
    ◦ Na aba “Pipes” são definidas as características das tubulações utlizadas: 
      DN, Diâmetro, Rugosidade, Pressão de serviço e etc
    ◦ Na aba “Calculations Options”, ajustar a velocidade máxima permitida da rede (por 
      defeito = 5 m/s) marque também a opção de calcular a extensão dos tubos <Calculate pipe lenth>    
    ◦ Clicar no botão “Select” e escolher a configuração de cálculo “template_d-w_lps.inp”
    • Clicar em <Complementos/Qwater/Make epanet> e aceitar todas as mensagens
    • Para todos os shapes, salvar e sair do modo de edição
    •  Clicar em <Projeto/Opções de Aderência> e clicar no ícone com um imã.
 
 ### Traçando a rede
 
 #### Reservatório 
    • Selecionar o shape de reservatórios e clicar no botão de edição
    • Habilitar o rótulo de camada para apresentar o campo “DC_ID”
    • Locar todos os reservatórios (nível fixo), preenchendo o campo “HEAD” com a Cota do 
      Terreno. Abrir a tabela para verificar que todos os reservatórios tenham cota.
    • Alterar a apresentação do rótulo para ==> 'Nó: ' || "DC_ID"  ||  '\n Cota= ' || "HEAD" 
    • Salvar o shape e sair do modo de edição
#### Nós
    • Selecionar o shape de nós e clicar no botão de edição
    • Habilitar o rótulo de camada para apresentar o campo “DC_ID”
    • Locar todos os nós
    • Preencher o campo “ELEVATION” com a Cota do Terreno. Abrir a tabela para verificar que 
    todos os nós tenham cota.
    • Alterar a apresentação do rótulo para ==> 'Nó: ' || "DC_ID"  ||  '\n Cota= ' || "ELEVATION"
    • Salvar o shape e sair do modo de edição
#### Trechos
    • Selecionar o shape de trechos e clicar no botão de edição
    • Habilitar o rótulo de camada para apresentar o campo “DC_ID”
    • Traçar todos os trechos conforme a direção do fluxo prevista (de montante para jusante). Um
      trecho e composto por uma polilinha que inicia no nó de montante e finaliza no nó de 
      jusante. Observação: Botão direito para finalizar. Tecla Esc para cancelar a edição em curso.
    • Preencha os dados das tabelas de atributo com valores padrão de forma automática 
      clicando em <Plugins / Qwater / Fill up Fields>
    • Salvar o shape e sair do modo de edição.

### Calculando a demanda

    • Clicar em <Complementos/Qwater/Calc Flow>. Deve aparecer a mensagem “Demanda nos 
      nós calculada com sucesso”. Esta rotina calcula a vazão unitária a partir da demanda 
      distribuída alocando em cada nó, o produto da vazão unitária vezes a metade da extensão 
      dos trechos conectados ao nó.
    • (Opcional) Também é possível calcular a vazão utilizando um layer de polígonos como Zonas Hidráulicas:
        • Crie um layer de polígono e crie um polígono delimitando cada zona hidráulica de interesse 
          (nesse caso, zonas com uma Demanda específica)
        • Salve o polígono
        • Defina o layer de polígonos como Zona Hidráulica em <Plugins/ Qwater / Settings / Hydraulic Zone layer>
        • Rode <Plugins / Qwater / Make model> e aceite as mensagens de confirmação para 
          criar os campos necessários na tabela de atributos
        • Preencha o campo 'DEMAND' para cada zona hidráulica
        • Click <Plugins / Qwater / Calc Flow>
    • Salvar o shape de nós e sair do modo de edição.

### Simulação preliminar da rede

    • Clicar em <Complementos/Qwater/Run Epanet Simulation> e aguardar a apresentação da 
      mensagem. Se a mensagem indicar a ocorrência de erros, analisar as indicações dos erros na 
      aba “Report”. 
    • Se a simulação foi bem-sucedida, salvar os shapes e sair do modo de edição.
    
### Otimização dos diâmetros da rede

    • Clicar em <Complementos/Qwater/Calculate economics diameter> e confirme a mensagem 
      de substituir os valores do campo “DIAMETER”.
    • Salvar os shapes e sair do modo de edição.
      Simulação da rede com os diâmetros otimizados
    • Clicar em <Complementos/Qwater/Run Epanet Simulation> e aguardar a apresentação da 
      mensagem.
    • Se a simulação foi bem-sucedida, salvar os shapes e sair do modo de edição.
    
### Ajustes finais
    
    • Salvar o projeto
    • Salvar o projeto (sugestão nome anterior mais result, pe: Rede_result.qgs).
    • Clicar em <Complementos/Qwater/Load default Stiles>.
    • Analisar os resultados e proceder ao ajuste fino de altitude do reservatório, diâmetros de 
      trechos.
    • Rodar a rede novamente (<Complementos/Qwater/Run Epanet Simulation>)
    • Salvar os shapes e sair do modo de edição.
    • Salvar o projeto.
    • Exportar a rede projetada para o formato dxf. Adotar uma escala compatível.

