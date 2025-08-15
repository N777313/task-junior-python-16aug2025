 cat docker-compose.yml
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: app
      POSTGRES_DB: appdb
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app -d appdb"]
      interval: 3s
      timeout: 3s
      retries: 10
    volumes:
      - pgdata_task7:/var/lib/postgresql/data

  app:
    build: .
    depends_on:
      db:
        condition: service_healthy
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: app
      POSTGRES_DB: appdb
      POSTGRES_HOST: db
      POSTGRES_PORT: 5432
    command: ["python", "main.py", "--help"]
    working_dir: /app
    volumes:
      - .:/app

volumes:
  pgdata_task7:



# Answer:

Спасибо, теперь всё видно. У тебя почти всё настроено правильно в `docker-compose.yml`, и ты уже указываешь `POSTGRES_DB: appdb`, что отлично. Но несмотря на это, в логах всё равно видно:

```
FATAL:  database "appdb" does not exist
```

---

### 🔍 Почему так происходит?

PostgreSQL **создаёт базу `appdb` только при первом запуске**, если **данных ещё нет** в `pgdata_task7`.

Но если том `pgdata_task7` уже существует (даже пустой), контейнер не запустит инициализацию — а значит, база `appdb` не будет создана.

---

### ✅ Решение: удалить старый volume, чтобы заново инициализировать базу

#### 📌 Шаги:

1. **Останови контейнеры**:

   ```bash
   docker-compose down
   ```

2. **Удаление volume, чтобы сбросить базу**:
   ⚠️ Это удалит все данные в контейнере PostgreSQL.

   ```bash
   docker volume rm <projectname>_pgdata_task7
   ```

   Или, если не уверен в имени:

   ```bash
   docker volume ls
   docker volume rm имя_тома
   ```

3. **Запусти снова**:

   ```bash
   docker-compose up --build
   ```

Теперь база `appdb` будет создана автоматически, потому что переменные `POSTGRES_DB`, `POSTGRES_USER`, и `POSTGRES_PASSWORD` указаны корректно.

---

### 🧪 Проверка

Можно протестировать, работает ли всё, так:

```bash
docker-compose run --rm app python main.py init
```

Это создаст таблицу `products` и добавит 10 тестовых продуктов.

---

### 🔐 Рекомендации на будущее

* Добавь SQL-скрипты для инициализации при первом запуске, если хочешь больше контроля (таблицы, пользователи и т.д.).
* Добавь проверку подключения (как выше в `connect()`), чтобы избежать ошибки при старте приложения, если БД ещё не готова.

---

Хочешь, я сгенерирую `create-db.sql` и обновлю `docker-compose.yml` с нужными volume для SQL-инициализации?
