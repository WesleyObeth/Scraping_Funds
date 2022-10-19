# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 13:51:17 2020

@author: wesleyhernandez
"""

# Pacote para mexer com tipos de datas.
from datetime import datetime
# Biblioteca para mexer com DataFrames.
import pandas as pd
# Biblioteca para entrar na API do yahoo finance.
import yfinance as yf
# Biblioteca usada para requisitar uma página de um web site.
import requests
# Pacote para analisar documentos ou tags HTML.
from bs4 import BeautifulSoup


# É definido o caminho do WebSite.
response = requests.get('https://www.fundsexplorer.com.br/ranking')
response

# Analisa o HTML na variável 'response' e o armazena no formato Beautiful Soup.
soup = BeautifulSoup(response.text, 'lxml')
soup

# Definido uma variavel para capturar a tabela.
table = soup.find_all('table')[0]
table


# Tranforma a tabela HTML para DataFrame
fundos = pd.read_html(str(table), decimal = ',', thousands = '.')[0]

# Remplaza a virgula e/ou apercentagem das colunas selecionadas.
for column in fundos.columns[5:12]:
    fundos[column] = fundos[column].str.replace(',' ,'.').str.replace('%', '').astype('float64')
    fundos[column] = fundos[column]
fundos

# Ordena a coluna PatrimônioLíq.
fundos.sort_values('PatrimônioLíq.', ascending = False)

# Concatena a nomenclatura "SA" nos valores do código do fundo
fundos['Códigodo fundo'] = fundos['Códigodo fundo'] + '.SA'
fundos

fundos.to_excel("teste.xlsx", encoding = 'utf8', index = False)

# Incluida uma nova variavel para definir o ticket
tickers = fundos['Códigodo fundo']
tickers

# É configurado o cabeçalho da pagina.
headers = {
    'authority': 'fiis.com.br',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://www.google.com/',
    'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': '_ga=GA1.3.2023460933.1643449330; _gid=GA1.3.1099705220.1643449330; prism_25600870=2a9e4274-06f2-4497-be32-0509ce59c287; _hjSessionUser_1049683=eyJpZCI6ImE5MzZjNjg4LWJjMGEtNWExNS1hYWE3LWM3MTY5MjIxYTRiMyIsImNyZWF0ZWQiOjE2NDM0NDkzMzAyNzIsImV4aXN0aW5nIjp0cnVlfQ==; hotid=eyJjaWQiOiIxNjQzNDQ5MzMxNTM1NTc3NDYwODgyNDI5OTIxMDAwIiwiYmlkIjoiMTY0MzQ0OTMzMTUzNTU3NzQ2MDg4MjQyOTkyMTAwMCIsInNpZCI6ImRkMzQ3Mjg5MjMwZjRlOTg4NWZhN2E5NTliYmJjNzA0In0=; __atuvc=1%7C4; __atssc=google%3B1; XSRF-TOKEN=eyJpdiI6IkRBcFwvY3ZxWU5ad2RYTmJZejdVajB3PT0iLCJ2YWx1ZSI6ImU2bVgwc0hjbUJZSmxcL0VMOGlMKzhWN0RFOVlDYTJKK3hJR2Q5SmtMd2VHdFpJKzd4dXFTMDFoWTNRRWphNHFWIiwibWFjIjoiYTJlNjVmNGY3N2I0MGIyMGE3NmVhYTM1MDE3M2YzMjVkMjFiZWFlYjU0NTY0ZjMxZjVmMjdkN2FiYWU0Nzg4NiJ9; fiis_session=eyJpdiI6IjE2QWY1WUVFd1VPMG1aM1pkTlU0VWc9PSIsInZhbHVlIjoiMHJaSEsrbW9LYjRrZkN4c1ZTYmJ3Q0FrZUc2RGh2SG1WN1ozeWVQbWh1WCtQSytvVFhubis5VWprOHFDWTZnWSIsIm1hYyI6ImJkMjY0Njk5OTdhZWI0MDFjM2MwNWM5MzkyNTA5ZDhjNDgzYmI5ZTFjZjJjYzJkMTIxZGY5OTJlNDI4NjM3MWIifQ%3D%3D; _hjIncludedInSessionSample=1; _hjSession_1049683=eyJpZCI6ImYyNzdlYjQ4LTlkYmUtNDAxYy04NzBkLWQxMjhkNjFjM2RlNyIsImNyZWF0ZWQiOjE2NDM0ODg4MzMyOTEsImluU2FtcGxlIjp0cnVlfQ==; _hjIncludedInPageviewSample=1; _hjAbsoluteSessionInProgress=0; popup=1; slider=1',
}

# É Definido as variaveis de tempo em relacao ao IPO (Oferta Publicia Inicial)
dia_IPO = []
mes_IPO = []
ano_IPO = []

# Função "for" para tratar cada variável.
for t in tickers:
  try:
    # {t[:6]} usado para pegar apenas as primeiras 6 letras da coluna "Códigodo fundo" para cada valor.
    response = requests.get(f'https://fiis.com.br/{t[:6]}/',headers = headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    data_ipo = soup.select('#informations--basic')
    data_ipo_2 = str(data_ipo[0]).split('Registro CVM')[1]
    data_ipo_3 = data_ipo_2[28:].split('<')[0]
    dia_IPO.append(data_ipo_3[0:2])
    mes_IPO.append(data_ipo_3[3:5])
    ano_IPO.append(data_ipo_3[6:10])
  except:
    dia_IPO.append('NA')
    mes_IPO.append('NA')
    ano_IPO.append('NA')
    pass

# Lista os tickets de um fundo.
list(tickers).index('APTO11.SA')

# Define uma data de inicial e data final.
start_date = datetime(2020, 1 ,1)
end = datetime.today()
print(start_date)

# É Criada a função para pegar fundos direto no yahoo finance.
def pega_fundos(name, ano, mes, dia):
  start_date = datetime(ano, mes, dia)
  end = datetime.today()
  ticker_fund = yf.download(name,  start = start_date, end = end)
  print(start_date)
  return ticker_fund

# Transforma as colunas para um determinado teste
pega_fundos(tickers[2], int(ano_IPO[3]),int(mes_IPO[3]), int(dia_IPO[3]))

# É criado um dicionário para armazenar os dados do fundo.
armazena_fundos = {}

i = 0
for ticker in tickers:
  try:
    armazena_fundos[ticker] = pega_fundos(ticker, int(ano_IPO[list(tickers).index(ticker)]),int(mes_IPO[list(tickers).index(ticker)]), int(dia_IPO[list(tickers).index(ticker)]))
  except:
    i = +1
    print(f'Não deu certo para o {ticker}')

# Imprime a variável
armazena_fundos

# formata.
pd.options.display.float_format = '{:,.2f}'.format

# É criada uma nova variável para receber o dicionario "armazena_fundos"
retorno = pd.DataFrame()

for key in armazena_fundos.keys():
  retorno[key] = armazena_fundos[key]['Adj Close'].pct_change()

retorno


# É criado um novo dicionario para armazenar o desconto
desconto = {}

def calcula_desconto(fundos):
  max_price = fundos['Adj Close'].describe()['75%']
  last_price = fundos['Adj Close'].iloc[-1]
  return (last_price - max_price)/max_price

# Função "for" para adicionar valores
for tick in armazena_fundos.keys():
  try:
    desconto[tick] = calcula_desconto(armazena_fundos[tick])
  except:
    desconto[tick] = 0

desconto

# Função para captura a lista de desconto.
def pega_setor(stock):  
    # List comprehension para facilitar a estrutura.
  return [x for x in fundos[tickers == stock]['Setor']]

# É definida uma variável para guardar as informações
funds_info = pd.DataFrame.from_dict(desconto, orient = 'index').reset_index()
funds_info.columns = ['Fundo', 'Desconto']
funds_info['Setor'] = [pega_setor(tick)[0] for tick in funds_info['Fundo']]

# Função dos dividendos media.
def pega_DY_12MMedia(stock):
  return [x for x in fundos[tickers == stock]['DY (12M)Média']]

# Função dos dividendos mês.
def pega_DY_mes(stock):
  return [x for x in fundos[tickers == stock]['DividendYield']]

# Função dos dividendos acumulado.
def pega_DY_12Acumulado(stock):
  return [x for x in fundos[tickers == stock]['DY (12M)Acumulado']]


# Criação de colunas para acrescentar os dividendos.
funds_info['DY_12M_Media'] = [pega_DY_12MMedia(tick)[0] for tick in funds_info['Fundo']]
funds_info['DY_Mes'] = [pega_DY_mes(tick)[0] for tick in funds_info['Fundo']]
funds_info['DY_Acumulativo_12M'] = [pega_DY_12Acumulado(tick)[0] for tick in funds_info['Fundo']]
funds_info

# Criado uma lista para consolidar dados.
lista_fundos = []

for tick in funds_info['Fundo']:
  lista_fundos.append(retorno[tick].std())

funds_info['Risco'] = lista_fundos

# Criado uma lista para consolidar dados.
lista_fundos_vol = []

for tick in funds_info['Fundo']:
  lista_fundos_vol.append(retorno[tick].std()* 252**(0.5))

funds_info['Volatilidade'] = lista_fundos_vol

# Elimina os valores nulos.
funds_info = funds_info.dropna()

# Ordena os valores pela coluna selecionada.
fundos_info_final = funds_info.sort_values('Desconto')
fundos_info_final

# Exportação da base para Excel.
fundos_info_final.to_excel('Oportunidade_Fundos.xlsx', index = False, encoding = "utf8")