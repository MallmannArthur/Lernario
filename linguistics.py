# linguistics.py
import spacy
from typing import List
from collections import namedtuple

# Define uma estrutura de dados simples para o token processado
TokenInfo = namedtuple("TokenInfo", ["text", "lemma", "is_word"])

try:
    # Carrega o modelo de alemão uma única vez
    nlp = spacy.load("de_core_news_sm")
    print("Modelo de linguagem (alemão) carregado.")
except OSError:
    print("Modelo 'de_core_news_sm' não encontrado.")
    print("Por favor, execute: python -m spacy download de_core_news_sm")
    exit()

def process_text(text: str) -> List[TokenInfo]:
    """
    Processa um texto usando spaCy, retornando uma lista de TokenInfo.
    """
    doc = nlp(text)
    processed_tokens = []
    for token in doc:
        is_word = token.is_alpha and not token.is_stop
        processed_tokens.append(
            TokenInfo(text=token.text_with_ws, lemma=token.lemma_.lower(), is_word=is_word)
        )
    return processed_tokens