# Astute backend
## Description
This is a backend for astute project. It is written in python using django framework. It is a REST API service to get 
information about locations and goods in the shop and create websocket connections to create routes for customers in shops 
and get information about their location in the shop.

## How to run
0) Download latest reid model from https://drive.google.com/drive/folders/1B5TvAcy3l6usqY_hgWtUmWa4Il-hJAgL
and add it to settings.py at REID_WEIGHTS_PATH variable

1) Run postgres, if you don't have it you can run it by:
```bash
docker run --name astute_db -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=root -e POSTGRES_DB=astute_db -d postgres:13.3
```

2) Create virtual environment and install requirements:
```bash
poetry install
```

2) Run migrations by
```bash
python manage.py migrate
```
*) If you want to use examples from data preparation step you can add initial data from examples dir (sql directory).

3) Run server with:
```bash
python manage.py runserver 8000
```

## Docs

You can find docs here (data preparation step architecture diagram here):
https://docs.google.com/document/d/1FWAimK3DmMpwVTPNKVr7HqskpLD-hsbV9DyeLAWkj4k/edit?usp=sharing

## Little report about reid models
![отчёт_по_моделям.png](resources%2F%D0%BE%D1%82%D1%87%D1%91%D1%82_%D0%BF%D0%BE_%D0%BC%D0%BE%D0%B4%D0%B5%D0%BB%D1%8F%D0%BC.png)

## Contacts
If you have problems with running this project or you have some questions you can contact us by email:
cotnikoarkady@gmail.com