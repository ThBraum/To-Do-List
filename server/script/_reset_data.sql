BEGIN;

SET session_replication_role = 'replica';

TRUNCATE TABLE public.todo_items RESTART IDENTITY CASCADE;

SET session_replication_role = 'origin';

INSERT INTO
    public.todo_items (
        title,
        description,
        completed,
        created_at
    )
VALUES (
        'Estudar FastAPI',
        'Ler a documentação e fazer exemplos.',
        false,
        CURRENT_TIMESTAMP
    ),
    (
        'Implementar CRUD',
        'Criar endpoints REST para ToDo',
        false,
        CURRENT_TIMESTAMP
    ),
    (
        'Finalizar Projeto',
        'Fazer testes e revisar tudo.',
        true,
        CURRENT_TIMESTAMP
    );

CREATE OR REPLACE FUNCTION _reinicia_sequences() RETURNS VOID AS
$$
DECLARE
    query_row RECORD;
BEGIN
    FOR query_row IN
        SELECT
            FORMAT(
                'SELECT setval(pg_get_serial_sequence(''"%s"'', ''%s''), coalesce(max(%s),0) + 1, false) FROM "%s";',
                tablename, idname, idname, tablename
            ) AS query_row
        FROM
            (
                SELECT
                    tablename,
                    (
                        SELECT a.attname
                        FROM
                            pg_index i
                            JOIN pg_attribute a ON a.attrelid = i.indrelid
                                AND a.attnum = ANY (i.indkey)
                        WHERE i.indrelid = tablename::REGCLASS AND i.indisprimary
                    ) AS idname
                FROM
                    pg_catalog.pg_tables
                WHERE schemaname = 'public' AND tablename != 'alembic_version'
            ) _
    LOOP
        EXECUTE query_row.query_row;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

SELECT _reinicia_sequences ();

COMMIT;