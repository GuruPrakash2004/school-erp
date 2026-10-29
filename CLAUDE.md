# School ERP

Multi-tenant School ERP SaaS. I'm (the owner) learning backend development, so explain choices simply.

## Stack
- Python + FastAPI (backend, `app/`)
- React + TypeScript + Vite + Axios (frontend, `web/`, plain CSS, no UI library yet)
- PostgreSQL 17 + pgvector, run via Docker (`pgvector/pgvector:pg17`)

## Layout
- `docker-compose.yml` – Postgres container, named volume `pgdata`
- `.env` – DB credentials (git-ignored, never commit)
- `db/schema.sql` – tables; `db/seed.sql` – sample data (1 school)

## Rules
- Tables: schools, teachers, classes, subjects, teaching_assignments, students, parents, student_guardians, marks, users. Do NOT add tables that aren't listed.
- `users` (login accounts): email unique per school; `role` is 'teacher' or 'parent' with matching `teacher_id`/`parent_id` (the other NULL), both via composite FKs.
- Every table except `schools` has `school_id NOT NULL` with a foreign key to `schools(id)` (multi-tenancy).
- Use foreign keys and NOT NULL; `marks.score` has CHECK between 0 and 100.
- Cross-tenant safety: every table that is referenced by a child has `UNIQUE (id, school_id)`, and every child table references it with a composite FK `FOREIGN KEY (x_id, school_id) REFERENCES x (id, school_id)` (not a plain `x_id REFERENCES x(id)`). Apply this to any new child table/column, and edit `schema.sql` itself (no standalone ALTERs).
- Password lives in `.env`, which is in `.gitignore`.
- Python is now allowed. Env/deps managed with `uv` (`uv add`, `uv run`).

## Backend layers (`app/modules/<module>/{schemas,repository,service,router}.py`)
- `router.py`: HTTP only. Parse request, call ONE service function, return. No logic, no permission checks, no SQL.
- `service.py`: business and permission rules (e.g. `can_view_student`). Calls repositories. No SQL.
- `repository.py`: SQL / SQLAlchemy only (ORM models live here). EVERY query filters by `school_id`; `school_id` comes from the current user, never from the request.
- `schemas.py`: Pydantic v2 request/response models.
- Shared: `app/main.py` (app + routers under `/api/v1`), `app/db.py` (engine, session), `app/core/deps.py` (`get_current_user`, DB dependency).
- `get_current_user` (in `deps.py`) reads the `Authorization: Bearer <JWT>` header; missing/invalid/expired token -> 401. `CurrentUser.id` is the teacher/parent profile id, `school_id` comes from the token.

## Frontend (`web/`)
- Dev server must be `http://localhost:5173` (strictPort); backend CORS allows only that origin.
- All HTTP goes through the single Axios instance in `web/src/api.ts` (adds `Authorization: Bearer <token>` from localStorage `access_token`).
- Pages: `Login` (school_id, email, password) and `Marks` (401 -> back to login, 403 -> "Not allowed").
- Run: `cd web && npm run dev`

## Auth
- `POST /api/v1/auth/login` body `{school_id, email, password}` -> `{access_token, token_type}`. Email is only unique per school, so `school_id` is part of login.
- JWT: PyJWT, HS256, 30-minute expiry, `SECRET_KEY` in `.env`. Claims: `sub` (users.id), `school_id`, `role`, `profile_id`.
- Passwords: Argon2 via pwdlib (`app/core/security.py`). Login failure always says "Invalid email or password" (never reveal whether the email exists).
- Do not edit the academics module for auth changes.

## Dev test users (school_id 1, DEV ONLY – never reuse these passwords)
| role | email | password | profile |
|---|---|---|---|
| teacher | anita.rao@greenfield.edu | AnitaPass123! | teacher 1 (teaches 10-A) |
| teacher | vikram.shah@greenfield.edu | VikramPass123! | teacher 2 (teaches 10-B) |
| parent | sunita.mehta@example.com | SunitaPass123! | parent 1 (child: student 1) |
| parent | rajesh.nair@example.com | RajeshPass123! | parent 2 (child: student 2) |

## Notes
- Host port is `5433` (5432 was already taken on this machine); inside Docker it is still 5432.

## Commands
- Run API: `uv run uvicorn app.main:app --reload`
- Start: `docker compose up -d`
- Load: `docker compose exec -T db psql -U school_admin -d school_erp < db/schema.sql` (same for `db/seed.sql`)
