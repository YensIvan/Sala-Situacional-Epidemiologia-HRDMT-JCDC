import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def mostrar():
    
    st.set_page_config(
        page_title="Hospitalizados Dengue",
        page_icon="🛏️",
        layout="wide"
    )

    st.title("🛏️ Hospitalizados Dengue")

    # CONEXIÓN BASE DATOS
    conexion = sqlite3.connect("epidemiologia.db", check_same_thread=False)

    # OBTERNER DATOS
    df = pd.read_sql(
        "SELECT * FROM HOSPITALIZADOS WHERE ingreso_anio=2026",
        conexion
    )
    

    df_ubigeo = pd.read_sql_query(
        """
        SELECT
            UBIGEO,
            DEPARTAMENTO,
            PROVINCIA,
            DISTRITO
        FROM UBIGEO
        """,
        conexion
    )

    df_localidades = pd.read_sql_query(
        """
        SELECT
            LOCALCOD,
            LOCALIDAD
        FROM LOCALIDAD
        """,
        conexion
    )

    # ==========================A PARTIR DE AQUI SE MUESTRAN LOS GRAFICOS==========================
    
    if df.empty:
        st.warning(
            "No existen datos registrados"
        )
    else:

        # Primera fila
        fila1 = st.container()

        # ==========================
        # INDICADORES
        # ==========================
        with fila1:

            col1, col2, col3= st.columns(3)

            with col1:
                st.metric(
                    "Total registros",
                    len(df)
                )

            with col2:
                st.metric(
                    "Casos confirmados",
                    len(df[df["resultado_final"] == "positivo"])
                )

            with col3:
                st.metric(
                    "Casos descartados",
                    len(df[df["resultado_final"] == "negativo"])
                )

        # ====================================================
        # ======= GRAFICO DE COLUMNA TOTAL POR ANIOS =========
        # ====================================================
 
        # Lista con datos históricos fijos
        datos = [
            {"ANO": 2023, "TOTAL": 272},
            {"ANO": 2024, "TOTAL": 237},
            {"ANO": 2025, "TOTAL": 125},
        ]

        # Obtener el año más reciente de la base
        ultimo_anio = df["ingreso_anio"].max()
        df_confirmados = df[df["resultado_final"] == "positivo"]

        # Contar los casos del último año
        total_actual = len(df_confirmados[df_confirmados["ingreso_anio"] == ultimo_anio])
    
        # Agregar el año actual
        datos.append({
            "ANO": ultimo_anio,
            "TOTAL": total_actual
        })

        # Obtener la ultima semana de la base
        ultima_semana = ultimo_anio = df["ingreso_semana_epi"].max()

        # Convertir a DataFrame
        df_grafico = pd.DataFrame(datos)

        fig = px.bar(
            df_grafico,
            x="ANO",
            y="TOTAL",
            title="Nro de casos captados en el HRDMT-JCDC 2021-2026"
        )

        # Agregar etiqueta con fondo amarillo
        for _, fila in df_grafico.iterrows():
            fig.add_annotation(
                x=fila["ANO"],
                y=fila["TOTAL"],
                text=f"<b>{fila['TOTAL']}</b>",
                showarrow=False,
                bgcolor="yellow",
                bordercolor="black",
                borderwidth=1,
                borderpad=4,
                yshift=15,
                font=dict(
                    size=18,
                    color="black"
                )
            )
        fig.update_layout(
            xaxis_title="Anio",
            yaxis_title="Nro de casos",
            height=500,
            title=f"Nro de casos hospitalizados en el HRDMT-JCDC 2021-2026 SE {ultima_semana} "
            )
        
        st.plotly_chart(fig, width="stretch", key="grafico_anual")


        # ====================================================
        # =========== GRAFICO DE COLUMNA POR SEMANA ==========
        # ====================================================


        df_grafico = (
            df.groupby("ingreso_semana_epi")
            .size()
            .reset_index(name="CANTIDAD")
            .sort_values("ingreso_semana_epi")
        )

        fig = px.bar(
            df_grafico,
            x="ingreso_semana_epi",
            y="CANTIDAD",
            text="CANTIDAD",
            title="Nro de hospitalizados por Semana Epidemiológica HRDMT-JCDC 2026"
        )


        fig.update_traces(
            textposition="outside"
            )

        fig.update_xaxes(
            tickmode="linear",
            dtick=1,
            tickangle=0
            )

        fig.update_layout(
            xaxis_title="Semana Epidemiológica",
            yaxis_title="Nro de casos",
            height=500
            )

        st.plotly_chart(fig, width="stretch", key="grafico_por_semana")
        
        # ====================================================
        # ========= GRAFICO DE COLUMNA POR RESULTADO =========
        # ====================================================

        df_grafico = ( 
          df.groupby(["ingreso_semana_epi", "resultado_final"]) 
          .size() 
          .reset_index(name="CASOS") 
          ) 
        fig = px.bar( 
            df_grafico, 
            x="ingreso_semana_epi", 
            y="CASOS",
            text="CASOS",
            barmode="stack", 
            color="resultado_final", 
            color_discrete_map={ 
                "positivo": "#BB0C0A", # Rojo 
                "negativo": "#04910B", # Verde 
                "indeterminado": "#E09303" # Naranja 
            }, 
            title="Nro de casos hospitalizados por Semana Epidemiológica HRDMT-JCDC 2026" 
        )
        
        fig.update_traces(
            textposition="outside"
            )

        fig.update_xaxes(
            tickmode="linear",
            dtick=1,
            tickangle=0
            )   

        fig.update_layout(
            xaxis_title="Semana Epidemiológica",
            yaxis_title="Nro de casos",
            height=500
            )

        st.plotly_chart(fig, width="stretch")
                                                
        # ====================================================
        # =================== GRAFICO CIRCULAR =============== 
        # ====================================================

        # Ultima fila
        fila4 = st.container()

        with fila4:

            col1, col2, col3= st.columns(3)

            with col1:
                
                # Contar registros por resultado
                resultado = df["resultado_final"].value_counts().reset_index()
                resultado.columns = ["resultado_final", "TOTAL"]

                # Crear gráfico de pastel
                fig = px.pie(
                    resultado,
                    names="resultado_final",
                    values="TOTAL",
                    color="resultado_final",
                    color_discrete_map={ 
                        "positivo": "#BB0C0A", # Rojo 
                        "negativo": "#04910B", # Verde 
                        "indeterminado": "#E09303" # Naranja 
                    }, 
                    title="Casos de dengue según resultado",
                    hole=0.4   # 0 = pastel, 0.4 = dona
                )

                fig.update_traces(
                    textinfo="percent+label",
                    textposition="inside"
                )

                st.plotly_chart(fig, width="stretch", key="grafico1")

            with col2:
            
                # Contar registros por resultado
                resultado = df["diagnostic_evo"].value_counts().reset_index()
                resultado.columns = ["diagnostic_evo", "TOTAL"]

                # Crear gráfico de pastel
                fig1 = px.pie(
                    resultado,
                    names="diagnostic_evo",
                    values="TOTAL",
                    color="diagnostic_evo",
                    color_discrete_map={ 
                        "A97.0": "#D40804", # Rojo 
                        "A97.1": "#8D0804", # Verde 
                        "A97.2": "#440101" # Naranja 
                    }, 
                    title="Casos de dengue según diagnostico",
                    hole=0.4   # 0 = pastel, 0.4 = dona
                )

                fig1.update_traces(
                    textinfo="percent+label",
                    textposition="inside"
                )

                st.plotly_chart(fig1, width="stretch", key="grafico2")

            with col3:
               
                # Contar registros por resultado
                resultado = df["sexo"].value_counts().reset_index()
                resultado.columns = ["sexo", "TOTAL"]

                # Crear gráfico de pastel
                fig1 = px.pie(
                    resultado,
                    names="sexo",
                    values="TOTAL",
                    color="sexo",
                    color_discrete_map={ 
                        "M": "#1104CA", # Rojo 
                        "F": "#990574", # Verde 
                    }, 
                    title="Casos de dengue por sexo",
                    hole=0.4   # 0 = pastel, 0.4 = dona
                )

                fig1.update_traces(
                    textinfo="percent+label",
                    textposition="inside"
                )

                st.plotly_chart(fig1, width="stretch", key="grafico3")
            

        # ====================================================
        # ======================== TABLA 1 ===================== 
        # ====================================================

        consulta = """
        SELECT
            infeccion_departamento AS DEPARTAMENTO,
            infeccion_provincia AS PROVINCIA,
            infeccion_distrito AS DISTRITO,
            COUNT(*) AS HOSPITALIZADOS
        FROM HOSPITALIZADOS WHERE ingreso_anio=2026
        GROUP BY
            infeccion_departamento,
            infeccion_provincia,
            infeccion_distrito
        ORDER BY
            HOSPITALIZADOS DESC,
            DEPARTAMENTO,
            PROVINCIA,
            DISTRITO;
        """

        df_tabla = pd.read_sql_query(consulta, conexion)

        st.subheader("🏥 Hospitalizados por lugar de infección")
        st.dataframe(df_tabla, width="stretch", hide_index=True)


        conexion.close()