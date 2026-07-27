import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def mostrar():
    
    st.set_page_config(
        page_title="Gráficos Epidemiológicos",
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

        # ==========================
        # COLUMNAS APILADAS
        # ==========================

        df_grafico = ( 
          df.groupby(["SEMANA", "TIPO_DX"]) 
          .size() 
          .reset_index(name="CASOS") 
          ) 
        fig = px.bar( 
            df_grafico, 
            x="SEMANA", 
            y="CASOS", 
            color="TIPO_DX", 
            barmode="stack", 
            color_discrete_map={ 
                "C": "#BB0C0A", # Rojo 
                "D": "#04910B", # Verde 
                "P": "#E09303" # Naranja 
            }, 
            title="Casos por Semana EpidemiológicaFF" 
        ) 
        st.plotly_chart(fig, use_container_width=True)
                                                                                                                                                                                                   
        # ==========================
        # AVANCE EPIDMEIOLOGICO
        # ==========================

        # Semana epidemiológica actual
        semana_actual = 28

        # Total semanas del año
        total_semanas = 52

        # Porcentaje de avance
        avance = (semana_actual / total_semanas) * 100

        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=avance,
                title={"text": f"Avance Semana Epidemiológica {semana_actual}"},
                number={
                    "suffix": "%"
                },
                gauge={
                    "axis": {
                        "range": [0, 100]
                    }
                }
            )
        )

        fig.update_layout(
            height=350
        )

        st.plotly_chart(fig, use_container_width=True)

        # ==========================
        # GRÁFICO POR SEMANA
        # ==========================

        df_confirmados = df[df["TIPO_DX"] == "C"]

        cantidad = (
            df_confirmados.groupby("SEMANA")
            .size()
            .reset_index(name="CANTIDAD")
            .sort_values("SEMANA")
        )

        fig = px.bar(
            cantidad,
            x="SEMANA",
            y="CANTIDAD",
            text="CANTIDAD",
            title="Nro de casos Confirmados por Semana Epidemiológica"
        )

        fig.update_traces(textposition="outside")

        fig.update_xaxes(
            tickmode="linear",
            dtick=1,
            tickangle=0
        )

        fig.update_layout(
            xaxis_title="Semana Epidemiológica",
            yaxis_title="Cantidad",
            height=500
        )

        st.plotly_chart(fig, use_container_width=True)

        # ==========================
        # GRÁFICO POR SEMANA
        # ==========================
        # Contar casos por sexo
        # Casos por sexo
        sexo = (
            df_confirmados.groupby("SEXO")
            .size()
            .reset_index(name="CANTIDAD")
        )

        # Total de casos
        total = sexo["CANTIDAD"].sum()

        # Gráfico
        fig = px.pie(
            sexo,
            names="SEXO",
            values="CANTIDAD",
            hole=0.5,
            title="Distribución de casos por sexo"
        )

        fig.update_traces(
            textinfo="label+percent",
            hovertemplate="<b>%{label}</b><br>Casos: %{value}<br>Porcentaje: %{percent}<extra></extra>"
        )

        # Mostrar total en el centro
        fig.add_annotation(
            text=f"<b>Total</b><br>{total}",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=20)
        )

        fig.update_layout(
            template="plotly_white",
            showlegend=True
        )

        st.plotly_chart(fig, use_container_width=True)


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

        st.plotly_chart(fig, use_container_width=True)


        conexion.close()