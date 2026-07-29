import sqlite3
import streamlit as st
import pandas as pd


# ============================
# CONEXIÓN BASE DE DATOS
# ============================
def mostrar():

    conexion = sqlite3.connect("epidemiologia.db", check_same_thread=False)

    # ============================
    # SELECCIONAR ARCHIVO
    # ============================

    archivo = st.file_uploader(
        "Seleccione un archivo CSV",
        type=["csv"]
    )


    if archivo is not None:

        df = pd.read_csv(archivo,encoding="latin1")

        st.subheader("Vista previa de datos")
        st.dataframe(df)


        # ============================
        # BOTÓN GUARDAR
        # ============================

        if st.button("💾 Actualizar Base de Datos"):

            # Filtrar datos del año seleccionado

            cursor = conexion.cursor()

            # ==================================
            # 1. ELIMINAR REGISTROS DEL AÑO
            # ==================================

            cursor.execute(
                """
                DELETE FROM LOCALIDAD
                """,
            )

            conexion.commit()

            # ==================================
            # 2. INSERTAR NUEVOS REGISTROS
            # ==================================

            df.to_sql(
                "LOCALIDAD",
                conexion,
                if_exists="append",
                index=False
            )

            conexion.commit()

            st.success(
                f"""
                ✅ Actualización realizada correctamente
                Registros insertados:
                    """
            )
    # ============================
    # Consultar la tabla
    # ============================

    consulta = """
    SELECT *
    FROM LOCALIDAD
    """

    datos = pd.read_sql(consulta, conexion)

    st.dataframe(datos)

    conexion.close()