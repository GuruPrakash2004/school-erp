# School ERP

Multi-tenant School ERP SaaS. I'm (the owner) learning backend development, so explain choices simply.

## Stack
- Python + FastAPI (backend, NOT started yet)
- PostgreSQL 17 + pgvector, run via Docker (`pgvector/pgvector:pg17`)

## Layout
- `docker-compose.yml` – Postgres container, named volume `pgdata`
- `.env` – DB credentials (git-ignored, never commit)
- `db/schema.sql` – tables; `db/seed.sql` – sample data (1 school)

## Rules
- Tables: schools, teachers, classes, subjects, teaching_assignments, students, parents, student_guardians, marks. Do NOT add tables that aren't listed.
- Every table except `schools` has `school_id NOT NULL` with a foreign key to `schools(id)` (multi-tenancy).
- Use foreign keys and NOT NULL; `marks.score` has CHECK between 0 and 100.
- Cross-tenant safety: every table that is referenced by a child has `UNIQUE (id, school_id)`, and every child table references it with a composite FK `FOREIGN KEY (x_id, school_id) REFERENCES x (id, school_id)` (not a plain `x_id REFERENCES x(id)`). Apply this to any new child table/column, and edit `schema.sql` itself (no standalone ALTERs).
- Password lives in `.env`, which is in `.gitignore`.
- No Python code until asked.

## Notes
- Host port is `5433` (5432 was already taken on this machine); inside Docker it is still 5432.

## Commands
- Start: `docker compose up -d`
- Load: `docker compose exec -T db psql -U school_admin -d school_erp < db/schema.sql` (same for `db/seed.sql`)
