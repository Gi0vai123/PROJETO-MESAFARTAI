
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Painel de Doações", page_icon="🥫")

st.title("Painel de Doações de Alimentos")
st.caption("Exemplo de: session_state, colunas, sidebar, formulário, métricas e gráfico")

if "doacoes" not in st.session_state:
    st.session_state.doacoes = []

st.sidebar.header("Configurações")
meta = st.sidebar.slider("Meta de arrecadação (kg)", min_value=50, max_value=500, value=200, step=10)

if st.sidebar.button("Zerar painel"):
    st.session_state.doacoes = []

st.subheader("Registrar nova doação")
col1, col2 = st.columns(2)

with col1:
    doador = st.text_input("Nome do doador")
    categoria = st.selectbox("Categoria", ["Arroz", "Feijão", "Macarrão", "Óleo", "Enlatados", "Outros"])

with col2:
    quantidade = st.number_input("Quantidade (kg)", min_value=1, max_value=25, value=5)

if st.button("Registrar doação", type="primary"):
    if doador.strip() == "":
        st.warning("Informe o nome do doador.")
    else:
        total_antes = sum(d["Kg"] for d in st.session_state.doacoes)

        st.session_state.doacoes.append({
            "Hora": datetime.now().strftime("%H:%M:%S"),
            "Doador": doador.strip(),
            "Categoria": categoria,
            "Kg": quantidade,
        })

        st.success(f"Obrigado, {doador.strip()}! Doação de {quantidade} kg registrada.")

        if total_antes < meta <= total_antes + quantidade:
            st.balloons()

total = sum(d["Kg"] for d in st.session_state.doacoes)
qtd_doacoes = len(st.session_state.doacoes)
faltam = max(meta - total, 0)

st.divider()
m1, m2, m3 = st.columns(3)
m1.metric("Total arrecadado", f"{total} kg")
m2.metric("Nº de doações", qtd_doacoes)
m3.metric("Faltam para a meta", f"{faltam} kg")

st.progress(min(total / meta, 1.0), text=f"{min(total / meta, 1.0):.0%} da meta de {meta} kg")

if st.session_state.doacoes:
    df = pd.DataFrame(st.session_state.doacoes)

    st.subheader("Doações por categoria")
    st.bar_chart(df.groupby("Categoria")["Kg"].sum())

    st.subheader("Histórico")
    st.dataframe(df, width="stretch", hide_index=True)
else:
    st.info("Nenhuma doação registrada ainda. Use o formulário acima!")
