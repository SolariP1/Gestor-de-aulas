import mysql.connector
from mysql.connector import Error

def conectar():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='db_escola'
        )
        if conn.is_connected():
            return conn
        else:
            print("Falha na conexão.")
            return None
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

def close_connection(conn):
    if conn and conn.is_connected():
        conn.close()
        print("Conexão encerrada.")

def selectCidades():
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT cid_codigo, cid_nome FROM tbl_cidade")
            cidades = cursor.fetchall()
            return cidades
        except Exception as e:
            print(f"Erro ao buscar cidades: {e}")
            return []
        finally:
            cursor.close()
            close_connection(conn)
    return []

def selectCurso():
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT cur_codigo, cur_nome FROM tbl_curso")
            cursos = cursor.fetchall()
            return cursos
        except Exception as e:
            print(f"Erro ao buscar cursos: {e}")
            return []
        finally:
            cursor.close()
            close_connection(conn)
    return []