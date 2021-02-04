<h1 align="center">LoR Decks Stats</h1>

<p>
  Script rápido e fácil em <strong>Python</strong> para coletar decks e extrair estatísticas como a quantidade de vezes que um região foi representada e a quantidade de vezes que um campeão apareceu no deck.
</p>

<h2 align="center">Requisitos</h2>

<p>
  Ter instalado o pacote requests.
  Escreva:
  <table>
    <thead><th>pip install requests</th></thead>
  </table>
</p>

<p>
  <strong>Input:</strong> um arquivo .csv com offset de 2 (perdão, usei uma base de dados específica do Mobalytics) apresentando em cada linha decks utilizados pelos jogadores durante o campeonato.
</p>

<p>
  <strong>Output:</strong> dois arquivos .csv, um com a relação das regiões usadas ao longo do campeonato e um com os campeões mais populares do campeonato.
</p>

<h2>Uso</h2>

<p>
  Após instalar o pacote requests, precisa-se de um arquivo <strong>input.csv</strong> exatamente no mesmo diretório e a partir daí escreva:
  <table>
    <thead><th>python main.py</th></thead>
  </table>
</p>
