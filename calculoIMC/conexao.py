import sqlite3 as bd

def conectarBanco():
    try:
        conn = bd.connect('imc.db')
        cursor = conn.cursor()
        
        criarTabela = """
        CREATE TABLE IF NOT EXISTS tb01_pessoa(
            tb01_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            tb01_nome TEXT NOT NULL,
            tb01_idade INTEGER NOT NULL, 
            tb01_peso DECIMAL NOT NULL,
            tb01_altura DECIMAL NOT NULL,
            tb01_classificacao TEXT NOT NULL
        );
        """
        cursor.execute(criarTabela)
        conn.commit()
        print("SUCESSO")

    except Exception as e:
        print("Deu erro: " + str(e))
    finally:
        conn.close()

