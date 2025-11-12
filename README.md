

Start:

docker compose up --build

Open Swagger: http://localhost:8000/docs

Services

api — FastAPI (Uvicorn)

worker — Celery worker (queues: emails, stats)

beat — Celery beat (щоденні job-и)

mongo — MongoDB 7

redis — Redis 7

Manual (local, without Docker)

python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload

Паралельно запустіть Redis та Mongo локально або в Docker.

API

POST /api/auth/register/ — реєстрація (створює юзера, тригерить Celery welcome task)

POST /api/auth/login/ — логін, повертає {access, refresh}

GET /api/auth/profile/ — профіль; заголовок: Authorization: Bearer <access>

POST /api/articles/ — створити статтю (авторизація обов'язкова)

GET /api/articles/ — список з фільтрами ?search=&tag=

GET /api/articles/{id}/ — деталі

PUT /api/articles/{id}/ — оновити (лише автор)

DELETE /api/articles/{id}/ — видалити (лише автор)

Celery tasks

send_welcome_email(user_id, email, name) — імітація відправки листа → запис у emails_log в Mongo.

daily_articles_stats() — раз на добу лог статистики в stats_log.

Notes

Alembic не використовується (MongoDB).

У проді додайте Nginx/HTTPS, CI/CD, тести — опущено за умовою.


---

## 7) GitHub Actions (мінімальний build)

`.github/workflows/docker.yml`
```yaml
name: Build Docker
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      - name: Build
        uses: docker/build-push-action@v6
        with:
          context: .
          push: false
          tags: articlehub:ci

8) Корисні запити для швидкого тесту

Реєстрація

POST http://localhost:8000/api/auth/register/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "string123",
  "name": "John Doe"
}

Логін → скопіюйте access

POST http://localhost:8000/api/auth/login/
Content-Type: application/json

{ "email": "user@example.com", "password": "string123" }

Профіль

GET http://localhost:8000/api/auth/profile/
Authorization: Bearer <ACCESS>

Створити статтю

POST http://localhost:8000/api/articles/
Authorization: Bearer <ACCESS>
Content-Type: application/json

{ "title": "My first article", "content": "Some text", "tags": ["python", "django"] }

Пошук/фільтр

GET http://localhost:8000/api/articles/?search=my&tag=python
Authorization: Bearer <ACCESS>

9) Подальші поліпшення (опційно)

Додати is_public/visibility, пагінацію, сортування.

Розділити доступи (ролі), refresh endpoint.

Валідація довжин/обмежень, індекси по title, tags.

Centralized logging (JSON) + OpenTelemetry.

Unit‑тести (pytest, httpx, respx) та інтеграційні тести в docker-compose.

Production: Nginx reverse proxy, Let's Encrypt, AWS EC2/ECS/EKS, MongoDB Atlas.