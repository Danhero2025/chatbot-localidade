import streamlit as st
import pandas as pd

# Título da aplicação
st.title("🩺 Consulta de Prestadores Hero Seguros")

# Instrução
st.markdown("Digite uma **cidade**, **estado** ou **país** abaixo para verificar se temos prestadores cadastrados (exceto Telemedicina e apenas Brasil).")

# Upload do arquivo Excel
data_file = st.file_uploader("📂 Envie a planilha de base (.xlsx)", type=["xlsx"])

if data_file:
    try:
        df = pd.read_excel(data_file, sheet_name="Assistências e Valores")

        # Entrada do usuário
        consulta = st.text_input("🔍 Localidade para consulta (cidade, estado ou país):")

        if consulta:
            consulta = consulta.strip()

            # Verifica se é fora do Brasil
            resultado_externo = df[
                df['Cidade'].fillna('').str.contains(consulta, case=False, na=False) |
                df['Estado'].fillna('').str.contains(consulta, case=False, na=False) |
                df['País'].fillna('').str.contains(consulta, case=False, na=False)
            ]

            if not resultado_externo['País'].str.lower().isin(["brazil", "brasil"]).any():
                st.warning("Desculpe, esta parte ainda está em desenvolvimento. Até lá, você terá de consultar manualmente.")
            else:
                # Filtra resultados válidos
                resultado = df[
                    (
                        df['Cidade'].fillna('').str.contains(consulta, case=False, na=False) |
                        df['Estado'].fillna('').str.contains(consulta, case=False, na=False) |
                        df['País'].fillna('').str.contains(consulta, case=False, na=False)
                    ) &
                    (df['País'].str.lower().isin(["brazil", "brasil"])) &
                    (df['Serviço'].str.lower() != "telemedicina") &
                    (df['Prestador acionado'].notna())
                ]

                if resultado.empty:
                    st.info("Nenhum prestador encontrado com base na localidade informada.")
                else:
                    st.success(f"Foram encontrados {resultado['Prestador acionado'].nunique()} prestador(es).")
                    for _, row in resultado.drop_duplicates(subset=['Prestador acionado', 'Cidade']).iterrows():
                        st.markdown(f"""
                        ---
                        **Prestador:** {row['Prestador acionado']}  
                        **Serviço:** {row['Serviço']}  
                        **Tipo de Assistência:** {row['Tipo de assistência']}  
                        **Data:** {row['Data de abertura da assistência']}  
                        **Local:** {row['Cidade']} – {row['Estado']} – {row['País']}  
                        """)
    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {str(e)}")
else:
    st.info("Aguardando envio da planilha Excel...")
