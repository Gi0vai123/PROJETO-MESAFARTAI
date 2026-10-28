3. ESCOPO GERAL DO PROJETO & REQUISITOS TÉCNICOS 
O ecossistema do MESAFARTAI é composto por 4 grandes pilares tecnológicos desenvolvidos 
100% em Python: 
1. Interface Conversacional (Front-End - Streamlit): 
o Chat interativo para cadastro de doações e consultas de ONGs. 
o Alternância de perfil na barra lateral ([Sou Doador | Sou ONG]). 
2. Motor de NLU & Trava de Segurança (Back-End - Scikit-Learn / Spacy): 
o Classificação 
de 
intenções 
consultar_status, fora_de_escopo). 
(cadastrar_doacao, 
solicitar_alimentos, 
o Mecanismo de Threshold (ex: < 0.60) com resposta de Fallback amigável quando 
a frase for ambígua. 
3. Extração de Entidades (Regex): 
o Captura automática de quantidades (kg, caixas, unidades), tipos de alimentos e 
prazos de validade (hoje, amanhã, 18h). 
4. Matchmaking Logístico & Banco de Dados (KNN + SQLite3): 
o Algoritmo KNN para calcular o match perfeito entre a oferta do doador e a ONG 
receptora mais próxima. 
o Banco de dados SQLite3 para persistência de doadores, receptores, doações e 
histórico de coletas.


- O público-alvo (Doadores vs. ONGs).

Passo 3: Identidade Visual e Criação do Logotipo via IA 
1. O grupo deve formular um prompt criativo e utilizar um gerador de imagem por IA  
para criar o logotipo do sistema. 
2. Requisito do Logo: Deve unir conceitos de alimento/acolhimento e tecnologia/IA 
assistiva. 
3. Salvar a imagem gerada em assets/logo_mesafartai.png. 
4. Registrar o prompt exato utilizado dentro do arquivo docs/escopo_projeto.md.
