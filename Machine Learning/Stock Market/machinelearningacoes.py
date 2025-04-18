# -*- coding: utf-8 -*-
"""MachineLearningAcoes.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/165u0Q47l6VV3uRJHjU3Gt2FzEwhh9bQA

##  Machine Learning - Previsão de ações

<p> Criando um modelo preditivo completo para prever o preço de ações
    
<p> Para visualizar o código de uma determinada ação ou criptomoeda basta acessar o site https://br.financas.yahoo.com/

Importar bibliotecas
"""

# Commented out IPython magic to ensure Python compatibility.
#importando a biblioteca do YahooFinance para baixar cotações
#Caso não tenha instalado ainda esse pacote, basta digitar !pip3 install yfinance
import yfinance as yF

# Imports para manipulação de dados
#import numpy as np
import pandas as pd

# Imports para visualização
import matplotlib.pyplot as plt
# %matplotlib inline


# Importando os pacotes para o modelo preditivo
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import MinMaxScaler
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score



#formatando valores com duas casas decimais
pd.options.display.float_format = '{:.2f}'.format

import warnings
warnings.filterwarnings("ignore")

# Carrega o dataset
Cotacoes = yF.Ticker("ITUB3.SA")

# Opções de períodos 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y e ytd.
dados = Cotacoes.history(period="5y")
dados.head()

# Retirar o indice do campo data
dados.reset_index(inplace=True)
dados.head()

dados.tail()

dados.drop(dados.tail(1).index,inplace=True)
dados.tail()

# Vamos excluir as colunas que não serão utilizadas e renomear os campos
dados.drop('Dividends', axis=1, inplace=True)
dados.drop('Stock Splits', axis=1, inplace=True)
dados.columns = ['Data','Abertura','Maximo','Minimo','Fechamento','Volume']
dados.head()

# Vamos observar o nosso range de dados
print('Menor data: ', dados['Data'].min())
print('Maior data:', dados['Data'].max())

# Vamos observar os dados referente a ultima data do nosso conjunto de dados
display(dados.loc[dados.index.max()])

# Tipos de Dados
dados.dtypes

# Volume de dados
dados.shape

# Sumário estatístico
dados.describe()

# Plot
plt.plot(dados["Fechamento"])
plt.title("Preço Diário de Fechamento das Ações", size = 14)
plt.show()

dados.head()

# Criando novos campos de Média Movel com 5 Dias, 14 Dias e 21 Dias
dados['mm5d'] = dados['Fechamento'].rolling(5).mean()
dados['mm14d'] = dados['Fechamento'].rolling(14).mean()
dados['mm21d'] = dados['Fechamento'].rolling(21).mean()

dados.head(30)

dados.dropna(inplace=True)

dados.shape

qtd_linhas = len(dados)
qtd_linhas_treino = qtd_linhas - 400
qtd_linhas_teste = qtd_linhas - 20

qtd_linhas_validacao = qtd_linhas_treino - qtd_linhas_teste

info = (
    f"linhas treino = 0:{qtd_linhas_treino}"
    f" linhas teste = 0:{qtd_linhas_treino}:{qtd_linhas_teste}"
    f" linhas validacao = 0:{qtd_linhas_teste}:{qtd_linhas}"

)

info

# Separando variaveis PREDITORAS e variavel ALVO
preditoras = dados.drop(['Data', 'Fechamento','Volume'], axis=1)
target = dados['Fechamento']

preditoras.head()

preditoras.tail()

# Normalizando os dados
scaler = MinMaxScaler().fit(preditoras)
preditoras_normalizadas = scaler.transform(preditoras)

# Verificando a normalização realizada
print('Preditoras: ', preditoras_normalizadas.shape)
print(preditoras_normalizadas)

# Separando dados para treino e teste
X_Train = preditoras_normalizadas[:qtd_linhas_treino]
X_test = preditoras_normalizadas[qtd_linhas_treino:qtd_linhas_teste]

Y_Train = target[:qtd_linhas_treino]
Y_test = target[qtd_linhas_treino:qtd_linhas_teste]

print(len(X_Train), len(Y_Train))
print(len(X_test), len(Y_test))

# Treinamento usando regressão linear
lr = linear_model.LinearRegression()
lr.fit(X_Train, Y_Train )
predicao = lr.predict(X_test)
cd = r2_score(Y_test, predicao)

f'Coeficiente de determinação:{cd * 100:.2f}'

#Lembrete: Coeficiente de determinação determina a aproximação da linha de regressão.
# Quanto mais próximo de 1 melhor.

# Treinamento usando rede neural
rn = MLPRegressor(max_iter = 2000)
rn.fit(X_Train, Y_Train )
predicao = rn.predict(X_test)
cd = rn.score(X_test,Y_test)

f'Coeficiente de determinação:{cd * 100:.2f}'

#Lembrete: Coeficiente de determinação determina a aproximação da linha de regressão.
# Quanto mais próximo de 1 melhor.

# Executando a previsão
previsao = preditoras_normalizadas[qtd_linhas_teste:qtd_linhas]
data_pregao_full = dados['Data']
data_pregao = data_pregao_full[qtd_linhas_teste:qtd_linhas]

res_full = dados['Fechamento']
res = res_full[qtd_linhas_teste:qtd_linhas]

pred = lr.predict(previsao)

df = pd.DataFrame({'Data_Pregão':data_pregao, 'Real': res, 'Previsão':pred})

df.set_index('Data_Pregão', inplace = True)

df

"""Previsão para o dia seguinte"""

# Pega o último pregão disponível
dados_hoje = yF.download("ITUB3.SA", period="1d")

# Renomeia as colunas para manter consistência (igual foi feito no dataframe principal)
dados_hoje = dados_hoje.rename(columns={
    'Open': 'Abertura',
    'High': 'Maximo',
    'Low': 'Minimo',
    'Close': 'Fechamento',  # Aqui está a correção principal
    'Volume': 'Volume'
})
# Verifica se temos dados válidos


if dados_hoje.empty:
    print("Não foi possível obter dados do último pregão.")
else:
    try:
        # Calcula médias móveis com os últimos dados históricos
        # USANDO A COLUNA 'Fechamento' que foi renomeada no dataframe principal
        ultimos_5d = dados['Fechamento'].iloc[-5:].mean()
        ultimos_14d = dados['Fechamento'].iloc[-14:].mean()
        ultimos_21d = dados['Fechamento'].iloc[-21:].mean()

        # Prepara os dados para amanhã
        dados_amanha = pd.DataFrame({
            'Abertura': [float(dados_hoje['Abertura'].iloc[-1])],
            'Maximo': [float(dados_hoje['Maximo'].iloc[-1])],
            'Minimo': [float(dados_hoje['Minimo'].iloc[-1])],
            'mm5d': [ultimos_5d],
            'mm14d': [ultimos_14d],
            'mm21d': [ultimos_21d]
        })

        # Normaliza e prevê
        X_amanha = scaler.transform(dados_amanha)
        previsao_amanha_lr = float(lr.predict(X_amanha)[0])
        previsao_amanha_rn = float(rn.predict(X_amanha)[0])

        # Exibe resultados
        print("\n" + "="*50)
        print(f"PREVISÃO PARA O PRÓXIMO PREGÃO:")
        print(f"- Data do último pregão: {dados_hoje.index[-1].strftime('%d/%m/%Y')}")
        print(f"- Preço de fechamento hoje: R$ {float(dados_hoje['Fechamento'].iloc[-1]):.2f}")
        print(f"- Previsão (Regressão Linear): R$ {previsao_amanha_lr:.2f}")
        print(f"- Previsão (Rede Neural): R$ {previsao_amanha_rn:.2f}")
        print("="*50 + "\n")

    except Exception as e:
        print(f"Erro ao gerar previsão: {str(e)}")

# Configurações do gráfico
plt.figure(figsize=(16, 8))
plt.title('Preço das Ações - Histórico e Previsão', fontsize=16, pad=20)

# Plot dos dados históricos
plt.plot(df.index, df['Real'],
         label='Valor Real (Histórico)',
         color='blue',
         marker='o',
         linestyle='-',
         linewidth=1.5,
         markersize=5)

# Plot das previsões (validação)
plt.plot(df.index, df['Previsão'],
         label='Previsão (Validação)',
         color='red',
         marker='o',
         linestyle='--',
         linewidth=1.5,
         markersize=5)

# Adicionando a previsão para amanhã
ultima_data = df.index[-1]
proxima_data = ultima_data + pd.Timedelta(days=1)

plt.scatter(proxima_data, previsao_amanha_lr,
            label=f'Previsão Amanhã (Linear): R$ {previsao_amanha_lr:.2f}',
            color='green',
            marker='*',
            s=200)

plt.scatter(proxima_data, previsao_amanha_rn,
            label=f'Previsão Amanhã (Rede Neural): R$ {previsao_amanha_rn:.2f}',
            color='purple',
            marker='X',
            s=200)

# Formatação do gráfico
plt.xlabel('Data do Pregão', fontsize=12)
plt.ylabel('Preço de Fechamento (R$)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.xticks(rotation=45)
plt.legend(fontsize=10, loc='upper left')

# Adiciona anotações
plt.annotate(f'Último pregão: {dados_hoje.index[-1].strftime("%d/%m/%Y")}\n'
            f'Fechamento: R$ {float(dados_hoje["Fechamento"].iloc[-1]):.2f}',
            xy=(0.02, 0.95),
            xycoords='axes fraction',
            bbox=dict(boxstyle='round', fc='white', ec='gray', alpha=0.8))

# Ajusta os limites do eixo X para incluir a previsão
plt.xlim([df.index[0], proxima_data + pd.Timedelta(days=1)])

plt.tight_layout()
plt.show()

# Gerando o Gráfico
plt.figure(figsize = (16,8))
plt.title('Preço das Ações')
plt.plot(df['Real'], label = 'Real', color = 'blue', marker = 'o')
plt.plot(df['Previsão'], label = 'Previsão', color = 'red', marker = 'o')
plt.xlabel('Data Pregão')
plt.ylabel('Preço Fechamento')
leg = plt.legend()

