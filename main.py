# main.py
import argparse
import core
import database
from colorama import init, Fore, Style

# Inicializa colorama para funcionar no Windows também
init(autoreset=True)

COLOR_MAP = {
    'NEW': Fore.BLUE,
    'KNOWN': Fore.GREEN, # Ou Style.RESET_ALL para não ter cor
    'DIFFICULT': Fore.YELLOW,
    None: Style.RESET_ALL # Para pontuação e espaços
}

def handle_initdb():
    database.init_db()

def handle_import(args):
    core.import_book(args.filepath)

def handle_read(args):
    lesson_id = args.lesson_id
    render_data, error = core.get_renderable_lesson(lesson_id)
    
    if error:
        print(f"Erro: {error}")
        return

    print("--- Início da Lição ---")
    text_to_lemma_map = {
        text.strip().lower(): lemma 
        for text, status, lemma in render_data if status is not None
    }
    # Imprime o texto colorido
    for text, status, lemma in render_data:
        color = COLOR_MAP.get(status, Fore.WHITE)
        print(f"{color}{text}", end="")
    print("\n--- Fim da Lição ---\n")

    # Loop de interação simples
    while True:
        action = input("Digite uma palavra para marcar como 'difícil', ou 'q' para sair: ").strip().lower()
        if action == 'q':
            break
        if action:
            # Simplificação: pedimos ao usuário o lema (forma base)
            # Uma UI gráfica faria isso automaticamente
            lemma_to_lookup = text_to_lemma_map.get(action)

            core.lookup_word(lemma_to_lookup)

        if lemma_to_lookup:
            core.lookup_word(lemma_to_lookup)
            print(f"'{action}' (lema: {lemma_to_lookup}) marcado. Reabra a lição para ver a mudança.")
        elif action:
            print(f"Palavra '{action}' não encontrada no texto da lição.")


def main():
    parser = argparse.ArgumentParser(description="Um clone do LingQ para o terminal.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Comando 'initdb'
    parser_initdb = subparsers.add_parser('initdb', help="Inicializa o banco de dados.")
    parser_initdb.set_defaults(func=handle_initdb)

    # Comando 'import'
    parser_import = subparsers.add_parser('import', help="Importa um livro de um arquivo .txt.")
    parser_import.add_argument('filepath', type=str, help="Caminho para o arquivo de texto.")
    parser_import.set_defaults(func=handle_import)

    # Comando 'read'
    parser_read = subparsers.add_parser('read', help="Lê uma lição.")
    parser_read.add_argument('lesson_id', type=int, help="O ID da lição para ler.")
    parser_read.set_defaults(func=handle_read)
    
    args = parser.parse_args()
    if hasattr(args, 'func'):
        # Chama a função associada ao subcomando
        args.func(args) if 'filepath' in args or 'lesson_id' in args else args.func()

if __name__ == "__main__":
    main()