# database.py
import sqlite3
from pathlib import Path

DB_FILE = "lingq_clone.db"
SCHEMA_FILE = "schema.sql"

def get_db_connection():
    """Retorna uma conexão com o banco de dados."""
    return sqlite3.connect(DB_FILE)

def init_db():
    """Inicializa o banco de dados criando as tabelas a partir do schema.sql."""
    if Path(DB_FILE).exists():
        print("Banco de dados já existe.")
        return

    print("Criando banco de dados...")
    try:
        with open(SCHEMA_FILE, 'r') as f:
            sql_script = f.read()
        
        with get_db_connection() as conn:
            conn.executescript(sql_script)
            conn.commit()
        print("Banco de dados inicializado com sucesso.")
    except FileNotFoundError:
        print(f"ERRO: Arquivo de schema '{SCHEMA_FILE}' não encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro ao inicializar o banco de dados: {e}")

def add_book(title: str) -> int | None:
    """Adiciona um novo livro e retorna seu ID."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO books (title) VALUES (?)", (title,))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            print(f"Livro com título '{title}' já existe.")
            cursor.execute("SELECT id FROM books WHERE title = ?", (title,))
            return cursor.fetchone()[0]

def add_lesson(book_id: int, lesson_number: int, content: str):
    """Adiciona uma nova lição ao banco de dados."""
    with get_db_connection() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO lessons (book_id, lesson_number, content) VALUES (?, ?, ?)",
            (book_id, lesson_number, content)
        )
        conn.commit()

def add_vocabulary(lemmas: set[str]):
    """Adiciona uma lista de novos lemas ao vocabulário com status 'NEW'."""
    new_lemmas = [(lemma,) for lemma in lemmas]
    with get_db_connection() as conn:
        # INSERT OR IGNORE garante que lemas já existentes não causem erro
        conn.executemany("INSERT OR IGNORE INTO vocabulary (lemma) VALUES (?)", new_lemmas)
        conn.commit()

def get_all_word_statuses() -> dict[str, str]:
    """Busca todos os lemas e seus status, retornando um dicionário."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT lemma, status FROM vocabulary")
        return dict(cursor.fetchall())

def get_lesson_content(lesson_id: int) -> str | None:
    """Retorna o texto de uma lição específica."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT content FROM lessons WHERE id = ?", (lesson_id,))
        result = cursor.fetchone()
        return result[0] if result else None

def update_word_status(lemma: str, new_status: str):
    """Atualiza o status de uma palavra no vocabulário."""
    with get_db_connection() as conn:
        conn.execute("UPDATE vocabulary SET status = ? WHERE lemma = ?", (new_status, lemma))
        conn.commit()