import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def mostrar():
    
    st.set_page_config(
        page_title="Sala Situacional Dengue",
        page_icon="📊",
        layout="wide"
    )

    st.title("📊 Sala Situacional de Dengue")

    # CONEXIÓN BASE DATOS
    conexion = sqlite3.connect("epidemiologia.db", check_same_thread=False)

    # OBTERNER DATOS
    df = pd.read_sql(
        "SELECT * FROM INDIVIDUAL WHERE DIAGNOSTIC IN ('A97.0', 'A97.1', 'A97.2')",
        conexion
    )
    
    df["LATITUD"] = (
        pd.to_numeric(
            df["LATITUD"].astype(str).str.replace(",", ""),
            errors="coerce"
        )
    )
    df["LONGITUD"] = (
        pd.to_numeric(
            df["LONGITUD"].astype(str).str.replace(",", ""),
            errors="coerce"
        )
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

            col1, col2, col3, col4= st.columns(4)

            with col1:
                st.metric(
                    "Total registros",
                    len(df)
                )

            with col2:
                st.metric(
                    "Casos confirmados",
                    len(df[df["TIPO_DX"] == "C"])
                )

            with col3:
                st.metric(
                    "Casos descartados",
                    len(df[df["TIPO_DX"] == "D"])
                )

            with col4:
                st.metric(
                    "Casos probables",
                    len(df[df["TIPO_DX"] == "P"])
                )
        # ====================================================
        # ======= GRAFICO DE COLUMNA TOTAL POR ANIOS =========
        # ====================================================
 
        # Lista con datos históricos fijos
        datos = [
            {"ANO": 2021, "TOTAL": 629},
            {"ANO": 2022, "TOTAL": 689},
            {"ANO": 2023, "TOTAL": 579},
            {"ANO": 2024, "TOTAL": 608},
            {"ANO": 2025, "TOTAL": 220},
        ]

        # Obtener el año más reciente de la base
        ultimo_anio = df["ANO"].max()
        df_confirmados = df[df["TIPO_DX"] == "C"]

        # Contar los casos del último año
        total_actual = len(df_confirmados[df_confirmados["ANO"] == ultimo_anio])
    
        # Agregar el año actual
        datos.append({
            "ANO": ultimo_anio,
            "TOTAL": total_actual
        })

        # Obtener la ultima semana de la base
        ultima_semana = ultimo_anio = df["SEMANA"].max()

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
            title=f"Nro de casos captados en el HRDMT-JCDC 2021-2026 SE {ultima_semana} "
            )
        
        st.plotly_chart(fig, width="stretch", key="grafico_anual")

        # ====================================================
        # =========== GRAFICO DE COLUMNA POR SEMANA ==========
        # ====================================================

        df_confirmados = df[df["TIPO_DX"] == "C"]

        df_grafico = (
            df_confirmados.groupby("SEMANA")
            .size()
            .reset_index(name="CANTIDAD")
            .sort_values("SEMANA")
        )

        fig = px.bar(
            df_grafico,
            x="SEMANA",
            y="CANTIDAD",
            text="CANTIDAD",
            title="Nro de casos por Semana Epidemiológica HRDMT-JCDC 2026"
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
          df.groupby(["SEMANA", "TIPO_DX"]) 
          .size() 
          .reset_index(name="CASOS") 
          ) 
        fig = px.bar( 
            df_grafico, 
            x="SEMANA", 
            y="CASOS",
            text="CASOS",
            barmode="stack", 
            color="TIPO_DX", 
            color_discrete_map={ 
                "C": "#BB0C0A", # Rojo 
                "D": "#04910B", # Verde 
                "P": "#E09303" # Naranja 
            }, 
            title="Nro de casos notificados por Semana Epidemiológica HRDMT-JCDC 2026" 
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
                resultado = df["TIPO_DX"].value_counts().reset_index()
                resultado.columns = ["TIPO_DX", "TOTAL"]

                # Crear gráfico de pastel
                fig = px.pie(
                    resultado,
                    names="TIPO_DX",
                    values="TOTAL",
                    color="TIPO_DX",
                    color_discrete_map={ 
                        "C": "#BB0C0A", # Rojo 
                        "D": "#04910B", # Verde 
                        "P": "#E09303" # Naranja 
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
                resultado = df["DIAGNOSTIC"].value_counts().reset_index()
                resultado.columns = ["DIAGNOSTIC", "TOTAL"]

                # Crear gráfico de pastel
                fig1 = px.pie(
                    resultado,
                    names="DIAGNOSTIC",
                    values="TOTAL",
                    color="DIAGNOSTIC",
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
                resultado = df["SEXO"].value_counts().reset_index()
                resultado.columns = ["SEXO", "TOTAL"]

                # Crear gráfico de pastel
                fig1 = px.pie(
                    resultado,
                    names="SEXO",
                    values="TOTAL",
                    color="SEXO",
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

        df_confirmados = df[df["TIPO_DX"] == "C"]

        # Agrupar los casos por UBIGEO
        df_resumen = (
            df_confirmados
            .groupby("UBIGEO")
            .size()
            .reset_index(name="TOTAL_CASOS")
        )

        # Vincular con la tabla UBIGEO
        df_resumen = df_resumen.merge(
            df_ubigeo[
                ["UBIGEO", "DEPARTAMENTO", "PROVINCIA", "DISTRITO"]
            ],
            on="UBIGEO",
            how="left"
        )

        # Ordenar las columnas
        df_resumen = df_resumen[
            [
                "UBIGEO",
                "DEPARTAMENTO",
                "PROVINCIA",
                "DISTRITO",
                "TOTAL_CASOS"
            ]
        ]

        # Ordenar por cantidad de casos
        df_resumen = df_resumen.sort_values(
            "TOTAL_CASOS",
            ascending=False
        )

        # Mostrar tabla
        st.subheader(
            "Nro de casos confirmados por Distrito HRDMT-JCDC 2026"
        )

        st.dataframe(
            df_resumen,
            width="stretch",
            hide_index=True
        )

        
        # ======================================================
        # ======================== TABLA 2 ===================== 
        # ======================================================

        df_resumen = (
            df
            .groupby("UBIGEO")
            .agg(
                CONFIRMADOS=("TIPO_DX", lambda x: (x == "C").sum()),
                DESCARTADOS=("TIPO_DX", lambda x: (x == "D").sum()),
                PROBABLES=("TIPO_DX", lambda x: (x == "P").sum()),
                TOTAL_CASOS=("TIPO_DX", "count")
            )
            .reset_index()
        )

        # Vincular con la tabla UBIGEO
        df_resumen = df_resumen.merge(
            df_ubigeo[
                ["UBIGEO", "DEPARTAMENTO", "PROVINCIA", "DISTRITO"]
            ],
            on="UBIGEO",
            how="left"
        )

        # Ordenar las columnas
        df_resumen = df_resumen[
            [
                "UBIGEO",
                "DEPARTAMENTO",
                "PROVINCIA",
                "DISTRITO",
                "CONFIRMADOS",
                "DESCARTADOS",
                "PROBABLES",
                "TOTAL_CASOS"
            ]
        ]

        # Ordenar por total de casos
        df_resumen = df_resumen.sort_values(
            "TOTAL_CASOS",
            ascending=False
        )

        # Mostrar tabla
        st.subheader(
            "Nro de casos captados por HRDMT JCDC por procedencia"
        )

        st.dataframe(
            df_resumen,
            width="stretch",
            hide_index=True
        )

        # ======================================================
        # ======================== TABLA 3 ===================== 
        # ======================================================

        # Filtrar solo casos confirmados
        df_confirmados = df[df["TIPO_DX"] == "C"]

        # Tabla dinámica: una columna por diagnóstico
        df_resumen = pd.pivot_table(
            df_confirmados,
            index="UBIGEO",
            columns="DIAGNOSTIC",
            values="TIPO_DX",
            aggfunc="count",
            fill_value=0
        ).reset_index()

        # Agregar columna TOTAL_CASOS
        columnas_diagnosticos = [col for col in df_resumen.columns if col != "UBIGEO"]
        df_resumen["TOTAL_CASOS"] = df_resumen[columnas_diagnosticos].sum(axis=1)

        # Vincular con la tabla UBIGEO
        df_resumen = df_resumen.merge(
            df_ubigeo[
                ["UBIGEO", "DEPARTAMENTO", "PROVINCIA", "DISTRITO"]
            ],
            on="UBIGEO",
            how="left"
        )

        # Reordenar columnas
        df_resumen = df_resumen[
            [
            "UBIGEO",
            "DEPARTAMENTO",
            "PROVINCIA",
            "DISTRITO"
            ] + columnas_diagnosticos + [
            "TOTAL_CASOS"
            ]
        ]

        # Ordenar por total de casos
        df_resumen = df_resumen.sort_values(
            "TOTAL_CASOS",
            ascending=False
        )

        # Mostrar tabla
        st.subheader("N° de casos confirmados por distrito y diagnóstico")

        st.dataframe(
            df_resumen,
            width="stretch",
            hide_index=True
        )


        # ======================================================
        # ================ PIRAMIDE POBLACIONAL=================
        # ======================================================

        # ================ 1. AGRUPAR DATOS=================
        import numpy as np

        # Solo casos confirmados
        df_confirmados = df[df["TIPO_DX"] == "C"].copy()

        # Grupos de edad
        # Límites de los grupos de edad
        bins = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,np.inf]

        # Etiquetas
        labels = [
            "0-4",
            "5-9",
            "10-14",
            "15-19",
            "20-24",
            "25-29",
            "30-34",
            "35-39",
            "40-44",
            "45-49",
            "50-54",
            "55-59",
            "60-64",
            ">=65"
        ]

        # Crear la variable de grupos de edad
        df_confirmados["GRUPO_EDAD"] = pd.cut(
            df_confirmados["EDAD"],
            bins=bins,
            labels=labels,
            right=False,
            include_lowest=True
        )

        # ========= 2. RESUMIR POR SEXO Y EDAD ========
        tabla = (
            df_confirmados
            .groupby(["GRUPO_EDAD", "SEXO"], observed=False)
            .size()
            .unstack(fill_value=0)
        )

        tabla = tabla.rename(columns={
            "M":"Masculino",
            "F":"Femenino"
        })

        # Valores negativos para hombres
        tabla["Masculino"] = -tabla["Masculino"]


        # ================ 3. GRAFICAR=================
        import plotly.graph_objects as go

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                y=tabla.index,
                x=tabla["Masculino"],
                orientation="h",
                name="Masculino",
                marker_color="#0a0dcf",
                text=tabla["Masculino"].abs(),   # Mostrar valores positivos
                textposition="outside"
            )
        )

        fig.add_trace(
            go.Bar(
                y=tabla.index,
                x=tabla["Femenino"],
                orientation="h",
                name="Femenino",
                marker_color="#f31383",
                text=tabla["Femenino"],
                textposition="outside"
            )
        )

        fig.update_layout(
            title="Pirámide poblacional de casos confirmados",
            barmode="relative",
            height=650,
            xaxis_title="Número de casos",
            yaxis_title="Grupo de edad",
            bargap=0.05,
            template="plotly_white"
        )

        # Mostrar valores positivos en el eje X
        fig.update_xaxes(
            tickformat=","
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )


        # ==========================
        # MAPA DE CALOR
        # ==========================

        # Filtrar casos confirmados y descartados
        df_mapa = df[df["TIPO_DX"].isin(["C"])].copy()

       # Convertir coordenadas
        df_mapa["LATITUD"] = pd.to_numeric(df_mapa["LATITUD"], errors="coerce")
        df_mapa["LONGITUD"] = pd.to_numeric(df_mapa["LONGITUD"], errors="coerce")

        # Eliminar coordenadas vacías
        df_mapa = df_mapa.dropna(subset=["LATITUD", "LONGITUD"])

        # Crear mapa de calor
        fig = px.density_map(
            df_mapa,
            lat="LATITUD",
            lon="LONGITUD",
            radius=25,
            zoom=10,
            height=800,
            title="Mapa de calor de casos confirmados",
            color_continuous_scale="Turbo"
        )

        fig.update_layout(
            template="plotly_white"
        )

        st.plotly_chart(fig, width="stretch")


        # ==========================
        # MAPA DE PUNTOS
        # ==========================

        # Filtrar casos confirmados y descartados
        df_mapa = df[df["TIPO_DX"].isin(["C", "D"])].copy()

        # Convertir coordenadas
        df_mapa["LATITUD"] = pd.to_numeric(df_mapa["LATITUD"], errors="coerce")
        df_mapa["LONGITUD"] = pd.to_numeric(df_mapa["LONGITUD"], errors="coerce")

        # Eliminar coordenadas vacías
        df_mapa = df_mapa.dropna(subset=["LATITUD", "LONGITUD"])

        # Mapa de puntos
        fig = px.scatter_map(
            df_mapa,
            lat="LATITUD",
            lon="LONGITUD",
            color="TIPO_DX",
            color_discrete_map={
                "C": "red",
                "D": "blue"
            },
            hover_name="DNI",
            hover_data={
                "NOMBRES": True,
                "DIAGNOSTIC": True,
                "TIPO_DX": True,
                "LATITUD": False,
                "LONGITUD": False
            },
            zoom=10,
            height=800,
            title="Casos confirmados y descartados"
        )

        fig.update_layout(
            template="plotly_white",
            legend_title="Tipo de diagnóstico"
        )

        st.plotly_chart(fig, width="stretch")

        # ==========================
        # LOCALIDAD
        # ==========================

        consulta = """
        SELECT
            l.LOCALCOD,
            l.LOCALIDAD,
            COUNT(i.LOCALCOD) AS CASOS
        FROM LOCALIDAD l
        LEFT JOIN INDIVIDUAL i
            ON l.LOCALCOD = i.LOCALCOD
            AND i.TIPO_DX = 'C'
            AND i.UBIGEO = 120301
        GROUP BY l.LOCALCOD, l.LOCALIDAD
        ORDER BY CASOS DESC;
        """

        df_localidad = pd.read_sql_query(consulta, conexion)

        fig = px.bar(
            df_localidad,
            x="CASOS",
            y="LOCALIDAD",
            orientation="h",
            text="CASOS",
            title="Casos confirmados de dengue por localidad - Distrito de Chanchamayo"
        )

        fig.update_traces(
            marker_color="#058B41",
            textposition="outside"
        )

        fig.update_layout(
            xaxis_title="Número de casos",
            yaxis_title="Localidad",
            height=max(700, len(df_localidad) * 22)
        )

        fig.update_yaxes(categoryorder="total ascending")

        st.plotly_chart(fig, width="stretch")



        conexion.close()