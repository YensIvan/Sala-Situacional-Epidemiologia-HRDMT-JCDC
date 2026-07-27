import streamlit as st

st.set_page_config(
    page_title="Sistema Epidemiológico",
    page_icon="🏥",
    layout="wide"
)


# ==========================
# MENÚ LATERAL
# ==========================

st.sidebar.title("🏥 Menú Principal")

opcion = st.sidebar.radio(
    "Seleccione una opción",
    [
        "📂 Cargar Individual",
        "📂 Cargar Semana",
        "📂 Cargar Ubigeo",
        "📊 Sala Situacional Dengue",
        "📊 Sala Situacional Leptospirosis",
        "📊 Sala Situacional Leishmaniasis",
    ]
)

# ==========================
# CAMBIAR DE PAGINA
# ==========================

if opcion == "📂 Cargar Individual":

    import cargar_individual
    cargar_individual.mostrar()

elif opcion == "📂 Cargar Semana":

    import cargar_semana
    cargar_semana.mostrar()

elif opcion == "📂 Cargar Ubigeo":

    import cargar_ubigeo
    cargar_ubigeo.mostrar()

elif opcion == "📊 Sala Situacional Dengue":

    import graficos
    graficos.mostrar()