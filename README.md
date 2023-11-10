# Astute backend
## How to run

1) Run postgres, if you don't have it you can run it by:
```bash
docker run --name astute_db -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=ot -e POSTGRES_DB=astute_db -d postgres:13.3
```
2) Run migrations by
```bash
python manage.py migrate
```
3) Run server with:
```bash
python manage.py runserver 8000
```
