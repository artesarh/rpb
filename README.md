## Welcome to reporting app

## Things you need to know

1. It runs on sqlite database
2. The database is backed up with a backup script that is set to run
   on a schedule controlled by a celery task scheduler
3. the django admin panel has been setup for quick changes to database
4. for everything else advice that you use the api to insert and retrieve
   from the database. The api contains some logic to make this easier than raw sql.
5. the app can be secured with JWT tokens, they currently have a 10 year timeout
   but you can use the front end to regenerate them or configure them for more precise
   access control.
6. there are 2 main databases

- default: this is the app database that stores user/session/jwt tokens
- api_db: this is the reporting database that stores the report information

There is also a pre-setup space for a reference database (lookups).

## How to navigate the app

This tries to follow some best practices while keeping it relatively simple:

- project/ : this is the main django project dir and contains the config settings,
  the root url for the endpoints, the web server config, the celery and task scheduler.

The settings folder has been split into base/dev/prod. Currently this isn't used a lot
as there is limited testing in the app.

wsgi.py : this file is going to be the entry point to the app
routers.py : this is the database router that controls where the models are migrated to

- frontend/ : this is a small app that controls some basic front end features,
  like generating tokens, accessing the admin panel, navigating to the docs.

- api/ : this is the reporting database app. it contains models, serializers (DTOs),
  and endpoints to access it via API.
  The recommendation here is to use the urls.py file to see how the endpoints are structured
  and then following the links in urls.py to navigate the project.

Endpoints are in api/views/
models in api/models/
DTOs in api/serializers/

- celery/ : this is the file system broker fo celery tasks

- db/ : storage for database and local backups

- scripts/ : random maintenaince scripts

- requirements/ : split into base/dev/prod so use prod in the pip install command
  when running in devops pipeline

- staticfiles/ : this folder stores the collection of static files that either django can
  server via whitenoise or can be served by the web server if using one.
  likely we will not be using a web server initially.
