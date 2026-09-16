# 💰 Expes — учёт доходов и расходов

Веб-приложение для учёта личных финансов: доходы, расходы, баланс, фильтры и статистика.

- **Бэкенд:** FastAPI + MongoDB (motor) + Redis (кэш)
- **Фронтенд:** Vue 3 + Pinia + Vite

---

## Требования

Перед запуском убедись, что установлены и **запущены** MongoDB и Redis:

| Инструмент | Версия | Проверка |
|-----------|--------|----------|
| Python | 3.11+ | `python3 --version` |
| Node.js | 18+ | `node --version` |
| MongoDB | 6+ | `mongod --version` |
| Redis | 7+ | `redis-cli ping` → `PONG` |
| pipenv | — | `pipenv --version` |

Запуск баз (если не подняты), пример для macOS + Homebrew:

```bash
brew services start mongodb-community   # MongoDB на :27017
brew services start redis               # Redis на :6379
```

---

## Первая установка

```bash
# 1. Бэкенд — зависимости в pipenv-окружение (venv внутри backend/)
cd backend
PIPENV_VENV_IN_PROJECT=1 pipenv install
cp .env.example .env        # при необходимости отредактируй настройки

# 2. Фронтенд — зависимости npm
cd ../frontend
npm install
cp .env.example .env        # адрес бэкенда (по умолчанию http://127.0.0.1:8000)
```

> В `backend/.env` обязательно задай свой `JWT_SECRET`.
> Сгенерировать: `python3 -c "import secrets; print(secrets.token_hex(32))"`

---

## Запуск (нужны два терминала)

### Терминал 1 — бэкенд

```bash
cd backend
PIPENV_VENV_IN_PROJECT=1 pipenv run dev
```

- API: <http://127.0.0.1:8000>
- Документация (Swagger): <http://127.0.0.1:8000/docs>
- Проверка состояния: <http://127.0.0.1:8000/health>

### Терминал 2 — фронтенд

```bash
cd frontend
npm run dev
```

- Приложение: <http://localhost:5173>

Открой **<http://localhost:5173>** в браузере, зарегистрируйся и начинай вести учёт.

---

## Полезные команды

**Бэкенд** (из папки `backend/`, с префиксом `PIPENV_VENV_IN_PROJECT=1`):

```bash
pipenv run dev        # запустить сервер с автоперезагрузкой (uvicorn :8000)
pipenv shell          # войти в виртуальное окружение
pipenv install <pkg>  # добавить зависимость
```

**Фронтенд** (из папки `frontend/`):

```bash
npm run dev      # dev-сервер :5173
npm run build    # production-сборка в dist/
npm run preview  # предпросмотр собранной версии
```

---

## Структура проекта

```
expes/
├── backend/          # FastAPI
│   ├── app/
│   │   ├── main.py            # приложение, CORS, подключения
│   │   ├── core/             # конфиг, безопасность (JWT), кэш
│   │   ├── db/               # подключение Mongo и Redis
│   │   ├── models/           # Pydantic-схемы
│   │   ├── repositories/     # работа с Mongo
│   │   └── api/routes/       # эндпоинты: health, auth, transactions, stats
│   ├── Pipfile               # зависимости pipenv
│   └── .env                  # настройки (не коммитить)
└── frontend/         # Vue 3
    ├── src/
    │   ├── api/              # axios-клиент + вызовы API
    │   ├── stores/           # Pinia (auth, transactions)
    │   ├── router/           # маршруты + защита
    │   ├── views/            # страницы (Login, Register, Home)
    │   └── components/       # SummaryBar, TransactionForm/Item, FilterBar
    └── .env                  # VITE_API_URL
```

---

## Возможные проблемы

| Симптом | Причина / решение |
|---------|-------------------|
| `/health` показывает `"mongo":"down"` | MongoDB не запущена → `brew services start mongodb-community` |
| `/health` показывает `"redis":"down"` | Redis не запущен → `brew services start redis` |
| На фронте ошибки CORS | В `backend/.env` в `CORS_ORIGINS` должен быть адрес фронта (`http://localhost:5173`) |
| Фронт не видит бэкенд | Проверь `VITE_API_URL` в `frontend/.env` и что бэкенд запущен на :8000 |
```
