# Бот для отримання транзакцій з bscscan.com

#### Варінти покращення функціоналу:
- Додати отримувати інформацію про переказ токенів
- Додати сповіщення в момент коли транзакція була створена і виконана

#### Коротко про структуру проекту:
- `app/present/bot/` - код бота
- `app/infra` - код для роботи з інфраструктурою (база даних, адаптер до bscscan.com)
- `app/core` - код для роботи з бізнес логікою

#### Про підхід до розробки:
Були використані принципи SOLID, частково Clean Architecture

#### Використані технології
- Python 3.11
- poetry
- docker
- docker-compose
- pytest
- postgresql
- sqlalchemy
- alembic
- aiogram
- make

## Запуск
Створити `.env` файл з наступними змінними:

```
TG_BOT_TOKEN=exampleToken

DB_USER=exampleUser
DB_PASSWORD=examplePassword
DB_NAME=exampleDbName
DB_PORT=5432 # обов'язково 5432
DB_HOST=exampleHost

BSCSCAN_API_KEY=exampleApiKey
```

Запустити докер контейнери:

`docker-compose up`


## Розробка
Встановити залежності:

`poetry install --with=dev`

Створити `.env.dev` файл з наступними змінними:

```
TG_BOT_TOKEN=exampleToken

DB_USER=exampleUser
DB_PASSWORD=examplePassword
DB_NAME=exampleDbName
DB_PORT=54321
DB_HOST=localhost # обов'язково localhost

BSCSCAN_API_KEY=exampleApiKey
DEBUG=True # або False
```

Запустити дев-докер контейнери:

`make dev-docker`

Запустити бота:

`make dev-bot`

## Тестування
Встановтити залежності для тестів:

`poetry install --with=test`

Запустити тести:

`make tests`
