-- 1. Deleta a tabela do banco destino pro caso dela já existir (pra não correr o risco de inserir dados em formatação errada)
DROP TABLE IF EXISTS {BANCO_DESTINO}.{NOME_TABELA};

-- 2. Cria uma tabela nova com o mesmo nome e copia do banco origem a formatação
CREATE TABLE {BANCO_DESTINO}.{NOME_TABELA} LIKE {BANCO_ORIGEM}.{NOME_TABELA};

-- TRUNCATE TABLE {BANCO_DESTINO}.{NOME_TABELA};

-- 3. Copia os dados para a nova tabela
INSERT INTO {BANCO_DESTINO}.{NOME_TABELA}
SELECT * FROM {BANCO_ORIGEM}.{NOME_TABELA};