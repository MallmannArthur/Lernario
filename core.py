# core.py
from pathlib import Path
import database
import linguistics

def import_book(filepath: str):
    """
    Importa um livro de um arquivo de texto, processa e salva no DB.
    """
    p = Path(filepath)
    if not p.exists():
        print(f"Erro: Arquivo '{filepath}' não encontrado.")
        return

    book_title = p.stem
    print(f"Importando livro: {book_title}")

    book_id = database.add_book(book_title)
    if not book_id:
        return

    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()

    # Simplificação do MVP: um arquivo = uma lição
    database.add_lesson(book_id, lesson_number=1, content=content)
    
    tokens = linguistics.process_text(content)
    # Pega todos os lemas únicos que são palavras
    unique_lemmas = {token.lemma for token in tokens if token.is_word}
    
    database.add_vocabulary(unique_lemmas)
    print(f"Importação concluída. {len(unique_lemmas)} lemas únicos adicionados ao vocabulário.")

def get_renderable_lesson(lesson_id: int):
    """
    Prepara uma lição para ser exibida, associando cada palavra ao seu status.
    Retorna uma lista de tuplas (texto_da_palavra, status, lema).
    """
    content = database.get_lesson_content(lesson_id)
    if not content:
        return None, "Lição não encontrada."

    all_statuses = database.get_all_word_statuses()
    processed_tokens = linguistics.process_text(content)

    renderable_list = []
    for token in processed_tokens:
        status = None
        if token.is_word:
            status = all_statuses.get(token.lemma, 'NEW')
        
        # Lógica para passar de 'NEW' para 'KNOWN' na primeira visualização
        if status == 'NEW':
            database.update_word_status(token.lemma, 'KNOWN')
            status = 'NEW' # Ainda exibe como 'NEW' nesta primeira vez
            
        renderable_list.append((token.text, status, token.lemma))
        
    return renderable_list, None

def lookup_word(lemma: str):
    """Marca uma palavra como 'difícil'."""
    print(f"Marcando '{lemma}' como difícil.")
    database.update_word_status(lemma, 'DIFFICULT')