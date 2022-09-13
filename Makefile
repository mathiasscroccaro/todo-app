test_backend:
	sudo docker-compose run --rm todo_backend python3 manage.py test

run_backed:
	sudo docker-compose run --rm -p 8000:8000 todo_backend python3 manage.py runserver 0.0.0.0:8000

migrate_backend:
	sudo docker-compose run --rm todo_backend python3 manage.py makemigrations todolist
	sudo docker-compose run --rm todo_backend python3 manage.py migrate

su_create_backend:
	sudo docker-compose run --rm todo_backend python3 manage.py createsuperuser
