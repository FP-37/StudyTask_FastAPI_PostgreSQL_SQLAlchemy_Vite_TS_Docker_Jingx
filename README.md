# StudyTask\_FastAPI\_PostgreSQL\_SQLAlchemy\_Vite\_TS\_Docker\_Jingx

A full-stack educational project showcasing knowledge of REST APIs, layered architecture, microservices, FastAPI, PostgreSQL, SQLite, SQLAlchemy, Vite, TypeScript, MUI, Pydantic, Docker, and Nginx.



**Вариант 7 — База данных автобусных маршрутов**



Учебный проект по курсу **«Проектирование архитектуры мобильных и веб-приложений»** 

Проект собран в микросервисной архитектуре и поднимается одной командой через `docker compose`.



---



## 1) Постановка задачи



**База данных автобусных маршрутов** со следующими полями:

- номер маршрутов
- номер парка
- время начала движения  
- время окончания движения  
- длина маршрута



---



## 2) Требования, закрываемые проектом



- **REST API (FastAPI)**: добавление / изменение / удаление / получение объектов + **пагинация**.
- **ORM** для работы с БД (SQLAlchemy).
- Полная валидация входных данных.
- **React-клиент (Vite + TypeScript)**: отображение и удаление, а также:
- добавление объекта
- изменение объекта
- бесконечный скроллинг
- роутинг
- **JWT**: аутентификация, регистрация, авторизация; объекты доступны пользователю, который их создал.
- **Микросервисная архитектура**: отдельный сервис для auth (регистрация/аутентификация), отдельный сервис для
предметной области (buslines), отдельный сервис для React-клиента
- данные хранятся в **отдельных контейнерах PostgreSQL**



---



## 3) Состав сервиса и порты



В репозитории используется `docker-compose.yml`, который поднимает следующие контейнеры:



### Базы данных

- **postgres_auth** — PostgreSQL для сервиса аутентификации
- host: `localhost`, port: **5433** → container: 5432  
- БД/пользователь: `auth_db` / `auth_user`
- **postgres_buslines** — PostgreSQL для сервиса автобусных маршрутов  
- host: `localhost`, port: **5434** → container: 5432  
- БД/пользователь: `buslines_db` / `bus_user`



Для обеих БД настроены `healthcheck`, поэтому backend-сервисы стартуют только после готовности PostgreSQL.



### Backend

- **auth_service** — сервис регистрации/логина и выдачи JWT  
- порт: **8001**
- Swagger UI: `http://localhost:8001/docs`
- **buslines_service** — CRUD сервис автобусных маршрутов  
- порт: **8000**

- Swagger UI: `http://localhost:8000/docs`



### Frontend

- **frontend** — React (Vite/TS), собирается в контейнере и отдаётся как статические файлы  

- host: `http://localhost:5173` (порт 5173 проброшен на 80 внутри контейнера)



---



## 4) Быстрый старт



### Требования

- Docker Engine / Docker Desktop

- Docker Compose (команда `docker compose`)



### Запуск

Из корня репозитория:



```bash

docker compose up --build

```

### Открыть:

- Frontend: http://localhost:5173
- Auth API (Swagger): http://localhost:8001/docs
- BusLines API (Swagger): http://localhost:8000/docs

#### Остановка

```bash

docker compose down

```
#### Сброс данных (удалить тома PostgreSQL)
```bash

docker compose down -v

```
## 5) Конфигурация
### Backend переменные окружения
#### Для auth_service:
- **JWT_SECRET_KEY**
- **DATABASE_URL**=postgresql+psycopg2://auth_user:auth_pass@postgres_auth:5432/auth_db
#### Для buslines_service:
- JWT_SECRET_KEY
- DATABASE_URL=postgresql+psycopg2://bus_user:bus_pass@postgres_buslines:5432/buslines_db
- Frontend build args (заданы в docker-compose)
#### Во время сборки фронтенда задаются адреса API:
- **VITE_AUTH_URL**=http://127.0.0.1:8001
- **VITE_BUSLINES_URL**=http://127.0.0.1:8000
При замене портов или домена — обновить их в docker-compose.yml и пересобрать контейнеры.
## 6) Типовой сценарий использования
- Открыть **auth_service** и зарегистрироваться/войти.
- Получить **JWT** (access token).
- Работать с **buslines_service**, передавая токен в заголовке
- На клиенте (**frontend**) выполнить **CRUD** для маршрутов и получать списки частями.
## 7) Структура репозитория
- **auth_service/** — микросервис аутентификации/регистрации (JWT)
- **buslines_service/** — микросервис предметной области (маршруты)
- **frontend/** — React/Vite/TypeScript клиент
- **shared/** — общий код/утилиты для сервисов
- **docker-compose.yml** — единая точка запуска всей системы
## 8) Troubleshooting
**Полная пересборка**

```bash

docker compose down -v

docker compose up --build

```

