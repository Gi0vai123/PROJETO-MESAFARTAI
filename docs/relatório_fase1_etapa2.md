# Relatório de Execução – Fase 1 / Etapa 2 (AC-3)

**Projeto:** MESAFARTAI – Logística e Inteligência Assistiva no Combate à Fome
**Módulo:** `src/nlu.py` – Motor NLU (TF-IDF + Random Forest) com Trava de Threshold

---

## 1. Quantas árvores foram utilizadas no motor NLU?

Foram utilizadas **80 árvores** de decisão no Random Forest, definidas pelo parâmetro `n_estimators=80`:

```python
self.classifier = RandomForestClassifier(n_estimators=80, random_state=42)
```

## 2. Qual o valor de threshold utilizado no limiar de confiança?

O threshold utilizado foi **0.60 (60%)**, definido em `MotorNLU(limiar_threshold=0.60)`.
Se a maior probabilidade prevista for menor que 0.60, ou se a intenção prevista for `fora_de_escopo`, o sistema aciona o **fallback** e pede para o usuário reformular a mensagem.

## 3. Resultado da primeira execução

Comando executado: `python src/nlu.py`

```text
 [NLU] Modelo Random Forest e Vetorizador TF-IDF treinados com sucesso!

--- BATERIA DE TESTES DE ESTRESSE NLU ---

Entrada: 'Tenho 30 kg de banana para doar'
Intenção: cadastrar_doacao | Confiança: 0.93
Retorno: Intenção 'cadastrar_doacao' identificada com 92.5% de confiança.

Entrada: 'Nossa instituição precisa de mantimentos'
Intenção: fallback | Confiança: 0.41
Retorno: Desculpe, não consegui entender com clareza o seu pedido.
Você pode refazer a mensagem informando se deseja **doar alimentos** ou **solicitar doações para uma ONG**?

Entrada: 'Qual é a receita de bolo de cenoura?'
Intenção: fallback | Confiança: 0.49
Retorno: Desculpe, não consegui entender com clareza o seu pedido.
Você pode refazer a mensagem informando se deseja **doar alimentos** ou **solicitar doações para uma ONG**?

Entrada: 'coisa comida doar la'
Intenção: fallback | Confiança: 0.42
Retorno: Desculpe, não consegui entender com clareza o seu pedido.
Você pode refazer a mensagem informando se deseja **doar alimentos** ou **solicitar doações para uma ONG**?
```

**Análise dos resultados:**

| Entrada | Intenção | Confiança | Avaliação |
|---|---|---|---|
| Tenho 30 kg de banana para doar | cadastrar_doacao | 0.93 | Correto (frase idêntica ao treino) |
| Nossa instituição precisa de mantimentos | fallback | 0.41 | Falso negativo: deveria ser `solicitar_alimentos`, mas as palavras "instituição" e "mantimentos" não existem no treino |
| Qual é a receita de bolo de cenoura? | fallback | 0.49 | Correto: fora de escopo bloqueado pela trava |
| coisa comida doar la | fallback | 0.42 | Correto: frase confusa bloqueada pela trava |

A trava de threshold (< 0.60) funcionou: as mensagens incertas e fora de escopo foram barradas, e o sistema não arriscou uma classificação errada.

## 4. Como melhorar os resultados e aumentar o grau de confiança?

- **Aumentar e diversificar a base de treino:** hoje são só 21 frases (4 a 8 por intenção). Incluir sinônimos e variações ("instituição", "mantimentos", "entidade", "cesta básica", "quero ajudar") resolveria casos como o falso negativo do teste 2.
- **Balancear as classes:** `cadastrar_doacao` tem 8 exemplos e `consultar_status`/`fora_de_escopo` têm 4. Equilibrar a quantidade evita que o modelo puxe para a classe maior.
- **Pré-processamento do texto:** converter para minúsculas, remover acentos e stopwords ("de", "para", "o") e aplicar stemming/lematização, para que "doar", "doação" e "doações" sejam tratados como o mesmo termo.
- **Ajustar os hiperparâmetros:** aumentar `n_estimators` (ex.: 200 a 300), testar `max_depth` e `min_samples_leaf`, e usar `GridSearchCV` com validação cruzada.
- **Ajustar o vetorizador:** testar `ngram_range=(1, 3)` ou n-gramas de caracteres (`analyzer="char_wb"`), que lidam melhor com erros de digitação.
- **Calibrar o threshold com dados reais:** medir precisão e recall em um conjunto de validação para escolher o melhor limiar, em vez de fixar 0.60.
- **Comparar com outros modelos ou embeddings:** testar SVM, Regressão Logística ou embeddings de frases (ex.: BERTimbau) para capturar o significado, e não só as palavras exatas.

## 5. Por que o Random Forest foi o melhor método de Machine Learning para essa fase?

- **Funciona bem com poucos dados:** é um ensemble de várias árvores, então generaliza melhor que uma árvore sozinha em uma base pequena como a nossa.
- **Menos overfitting:** cada árvore é treinada com amostras e atributos aleatórios (bagging), e o resultado é a votação de todas, o que reduz a variância.
- **Fornece probabilidades (`predict_proba`):** a confiança é a proporção de árvores que votaram em cada classe. É exatamente esse valor que a **trava de threshold** usa para decidir o fallback.
- **Lida bem com dados esparsos e de alta dimensão**, como a matriz TF-IDF.
- **É simples, rápido e reproduzível:** treina em segundos, quase não exige ajuste de hiperparâmetros e o `random_state=42` garante o mesmo resultado em toda execução, o que é ideal para um MVP acadêmico.
- **É mais interpretável** que redes neurais, já que permite analisar a importância das palavras (features) na decisão.
