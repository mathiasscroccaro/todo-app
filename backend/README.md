# If your DB models were changed

```bash
docker-compose run --rm todo_api python3 manage.py makemigrations todolist
docker-compose run --rm todo_api python3 manage.py migrate
```

# How to test

`docker-compose run --rm todo_api python3 manage.py test`

# How to run

`docker-compose up`
