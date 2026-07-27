import sqlite3
import streamlit as st
import pandas as pd


# ============================
# CONEXIÓN BASE DE DATOS
# ============================
def mostrar():

    conexion = sqlite3.connect("epidemiologia.db", check_same_thread=False)

    # ============================
    # SELECCIONAR AÑO
    # ============================

    ano = st.selectbox(
        "Seleccione el año a cargar",
        #[ 2021, 2022, 2023, 2024, 2025, 2026]
        [ 2026]
    )

    # ============================
    # SELECCIONAR ARCHIVO
    # ============================

    archivo = st.file_uploader(
        "Seleccione un archivo CSV",
        type=["csv"]
    )


    if archivo is not None:

        df = pd.read_csv(archivo)

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
                DELETE FROM INDIVIDUAL
                WHERE ANO = ?
                 """,
                (str(ano),)
            )

            conexion.commit()

            # ==================================
            # 2. INSERTAR NUEVOS REGISTROS
            # ==================================

            df.to_sql(
                "INDIVIDUAL",
                conexion,
                if_exists="append",
                index=False
            )

            conexion.commit()

            st.success(
                f"""
                ✅ Actualización realizada correctamente
                Año actualizado: {ano}
                Registros insertados:
                    """
            )
    

            cursor.execute("""
            UPDATE INDIVIDUAL
            SET SEMANA = (
                SELECT SEMANA
                FROM SEMANA
                WHERE SEMANA.FECHA = INDIVIDUAL.FECHA_NOT
            )
            WHERE EXISTS (
                SELECT 1
                FROM SEMANA
                WHERE SEMANA.FECHA = INDIVIDUAL.FECHA_NOT
            )
            """)

            conexion.commit()
            st.success(
                f"""
                Semana actualizadas con exito"""
            )

    # ============================
    # Consultar la tabla
    # ============================

    consulta = """
    SELECT *
    FROM INDIVIDUAL
    """

    datos = pd.read_sql(consulta, conexion)

    st.dataframe(datos)

    conexion.close()