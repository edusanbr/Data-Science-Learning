# Machine Learning (Estudo Baseado em Tutorial)
📌 Contexto do Projeto
Este projeto foi desenvolvido como parte dos meus estudos em Machine Learning aplicado ao mercado financeiro, seguindo como base um tutorial online. O código foi implementado, analisado e adaptado para fins de aprendizagem pessoal, com o objetivo de entender na prática:

-  Como aplicar modelos de ML em séries temporais financeiras
-  Os desafios de previsão de preços de ativos
-  Técnicas de pré-processamento para dados financeiros
-  Comparação entre diferentes abordagens (Regressão Linear vs Redes Neurais)

🔍 Origem do Material Base
O código inicial foi adaptado do tutorial disponível em:
(insira aqui o link do vídeo/tutorial que você utilizou)

🛠️ Tecnologias Utilizadas
Python 3

-  Bibliotecas Principais:
-  yfinance - Coleta de dados do mercado
-  pandas - Manipulação de dados
-  scikit-learn - Modelos de ML (Regressão Linear e MLP)
-  matplotlib - Visualização dos resultados

📈 Metodologia
-  Coleta de Dados: 5 anos históricos de ITUB3.SA via Yahoo Finance
-  Pré-processamento:
-  Cálculo de médias móveis (5, 14 e 21 dias)
-  Normalização dos dados (MinMaxScaler)

Modelagem:
-  Regressão Linear (baseline)
-  Rede Neural MLP (Multilayer Perceptron)

Validação:
-  Divisão em conjuntos de treino/teste
-  Métrica: Coeficiente de Determinação (R²)

📊 Resultados Obtidos
-  Modelo	R² Score	Observações
-  Regressão Linear	99.84%	Melhor performance
-  Rede Neural (MLP)	94.01%	Sensível a parâmetros
-  
💡 Principais Aprendizados
-  Séries Temporais Financeiras são desafiadoras devido à alta volatilidade
-  Feature Engineering (como médias móveis) é crucial para melhorar previsões
-  Modelos Simples podem ter performance superior em alguns cenários
-  A importância da validação cuidadosa para evitar overfitting

🚀 Melhorias Implementadas
-  Adicionei visualizações mais completas dos resultados
-  Implementei previsão para o próximo dia útil
-  Adicionei tratamento de erros robusto
-  Documentação detalhada do código
