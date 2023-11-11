# Astute backend
## Description
This is a backend for astute project. It is written in python using django framework. It is a REST API service to get 
information about locations and goods in the shop and create websocket connections to create routes for customers in shops 
and get information about their location in the shop.

## How to run

1) Run postgres, if you don't have it you can run it by:
```bash
docker run --name astute_db -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=root -e POSTGRES_DB=astute_db -d postgres:13.3
```
2) Run migrations by
```bash
python manage.py migrate
```
3) Run server with:
```bash
python manage.py runserver 8000
```

## Docs

You can find docs here (data preparation step architecture diagram here):
https://docs.google.com/document/d/1FWAimK3DmMpwVTPNKVr7HqskpLD-hsbV9DyeLAWkj4k/edit?usp=sharing

## Contacts
If you have problems with running this project or you have some questions you can contact us by email:
cotnikoarkady@gmail.com