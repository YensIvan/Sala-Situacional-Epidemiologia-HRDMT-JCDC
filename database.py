import sqlite3
import pandas as pd

#Nombre de la base de datos
DATABASE = "epidemiologia.db"


def conectar():
    #Conecta con la base de datos
    return sqlite3.connect(DATABASE)


def crear_tabla():

    conexion = conectar()
    cursor = conexion.cursor()

    # Tabla individual
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS INDIVIDUAL(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            ANO INTEGER,     
            SEMANA INTEGER,
            DIAGNOSTIC TEXT,
            TIPO_DX TEXT,
            SUBREGION INTEGER,
            UBIGEO INTEGER,
            LOCALCOD INTEGER,
            LOCALIDAD TEXT,
            APEPAT TEXT,
            APEMAT TEXT,
            NOMBRES TEXT,
            EDAD INTEGER,
            TIPO_EDAD TEXT,
            SEXO TEXT,
            PROTEGIDO TEXT,
            FECHA_INI TEXT,
            FECHA_DEF TEXT,
            FECHA_NOT TEXT,
            FECHA_INV TEXT,
            SUB_REG_NT INTEGER,
            RED INTEGER,
            MICRORED INTEGER,
            E_SALUD INTEGER,
            SEMANA_NOT INTEGER,
            AN_NOTIFIC INTEGER,
            FECHA_ING TEXT,
            FICHA_INV TEXT,
            TIPO_NOTI TEXT,
            CLAVE TEXT,
            VERIFICA INTEGER,
            GESTANTE INTEGER,
            DNI TEXT,
            IDENTIFICADOR TEXT,
            MUESTRA TEXT,
            HC TEXT,
            FECHA_HOS TEXT,
            TIP_ZONA INTEGER,
            COD_PAIS INTEGER,
            NACIONALIDAD INTEGER,
            DIRECCION TEXT,
            ETNIAPROC INTEGER,
            ETNIAS TEXT,
            PROCEDE TEXT,
            OTROPROC TEXT,
            USUARIO TEXT,
            FECHA_MOD TEXT,
            USUARIO_MOD TEXT, 
            TIPO_DOC INTEGER,
            TIPO_VIA INTEGER,
            NUM_PUERTA TEXT,
            AGRUP_RURAL TEXT,
            NOMBRE_AGRUP TEXT,
            MANZANA TEXT, 
            BLOCK TEXT,
            INTERIOR TEXT,
            KILOMETRO TEXT,
            LOTE TEXT,
            REFERENCIA TEXT,
            LATITUD INTEGER,
            LONGITUD INTEGER,
            UBIGEO_DIR INTEGER,
            EESS_UBIGEO TEXT,
            DIRECCION_VERIFICADA TEXT
        )
    """)

    # Tabla semana
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SEMANA(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,    
            FECHA TEXT,
            SEMANA INTEGER
        )
    """)

    # Tabla ubigeo
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS UBIGEO(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,   
            UBIGEO INTEGER,    
            DEPARTAMENTO TEXT,
            PROVINCIA TEXT,
            DISTRITO TEXT  
        )
    """)

    conexion.commit()
    conexion.close()

