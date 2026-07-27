import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def mostrar():
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
    print(df)
    print(df.dtypes)
    print(df["UBIGEO"].dtype)
    print(df["UBIGEO"].unique()[:20])

mostrar()
