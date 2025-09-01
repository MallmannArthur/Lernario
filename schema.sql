-- schema.sql

-- Guarda cada palavra base (lema) e o status de aprendizado do usuário.
CREATE TABLE IF NOT EXISTS vocabulary (
    lemma TEXT PRIMARY KEY,
    status TEXT NOT NULL DEFAULT 'NEW' CHECK(status IN ('NEW', 'KNOWN', 'DIFFICULT')),
    seen_count INTEGER NOT NULL DEFAULT 0
);

-- Guarda os metadados dos livros importados.
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL UNIQUE
);

-- Guarda o conteúdo de cada lição (capítulo) de um livro.
CREATE TABLE IF NOT EXISTS lessons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    lesson_number INTEGER NOT NULL,
    content TEXT NOT NULL,
    FOREIGN KEY(book_id) REFERENCES books(id),
    UNIQUE(book_id, lesson_number)
);