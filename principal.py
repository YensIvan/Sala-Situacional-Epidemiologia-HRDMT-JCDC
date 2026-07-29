import streamlit as st

st.set_page_config(
    page_title="Sistema Epidemiológico",
    page_icon="🦉",
    layout="wide"
)


# ==========================
# MENÚ LATERAL
# ==========================

st.sidebar.title("🦉 Menú Principal")

opcion = st.sidebar.radio(
    "Seleccione una opción",
    [
        "📊 Sala Situacional Dengue",
        "🏥 Hospitalizados Dengue",
        "📂 Cargar Individual",
        "📂 Cargar Hospitalizados",
        "📂 Cargar Semana",
        "📂 Cargar Ubigeo",
        "📂 Cargar Localidad",
    ]
)

# ==========================
# CAMBIAR DE PAGINA
# ==========================

if opcion == "📂 Cargar Individual":

    import cargar_individual
    cargar_individual.mostrar()

elif opcion == "📂 Cargar Hospitalizados":

    import cargar_hospitalizados
    cargar_hospitalizados.mostrar()

elif opcion == "📂 Cargar Semana":

    import cargar_semana
    cargar_semana.mostrar()

elif opcion == "📂 Cargar Ubigeo":

    import cargar_ubigeo
    cargar_ubigeo.mostrar()

elif opcion == "📂 Cargar Localidad":

    import cargar_localidad
    cargar_localidad.mostrar()

elif opcion == "📊 Sala Situacional Dengue":

    import graficos
    graficos.mostrar()

elif opcion == "🏥 Hospitalizados Dengue":

    import graficosHospi
    graficosHospi.mostrar()
