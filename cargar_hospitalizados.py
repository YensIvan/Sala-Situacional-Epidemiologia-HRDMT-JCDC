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
        "Seleccione un archivo de Excel",
        type=["xlsx", "xls"]
    )


    if archivo is not None:

        df = pd.read_excel(archivo)

        # Crear columna adicional
        df["RESULTADO_FINAL"] = ""

        df["RESULTADO_FINAL"] = df["resultado_muestra1_elisa_ns1"]
        df.loc[
            (df["resultado_muestra2_igm"] == "positivo") |
            (df["resultado_muestra3_pcr"] == "positivo"),
            "RESULTADO_FINAL"
        ] = "positivo"




        st.subheader("Vista previa de datos")
        st.dataframe(df, width="stretch")


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
                DELETE FROM HOSPITALIZADOS
                """,
            )

            conexion.commit()

            # ==================================
            # 2. INSERTAR NUEVOS REGISTROS
            # ==================================

            df.to_sql(
                "HOSPITALIZADOS",
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

            cursor.execute("""
                UPDATE HOSPITALIZADOS
                 SET ingreso_semana_epi = (
                    SELECT SEMANA
                    FROM SEMANA
                    WHERE SEMANA.FECHA = HOSPITALIZADOS.fecha_ing_ipress
            )
             WHERE EXISTS (
                SELECT 1
                FROM SEMANA
                WHERE SEMANA.FECHA = HOSPITALIZADOS.fecha_ing_ipress
            )
            """)
        
            conexion.commit()
            st.success(
                f"""
                Hospitalizados actualizadas con exito"""
            )
                    
    # ============================
    # Consultar la tabla
    # ============================

    consulta = """
    SELECT *
    FROM HOSPITALIZADOS
    """

    datos = pd.read_sql(consulta, conexion)

    st.dataframe(datos)

    conexion.close()