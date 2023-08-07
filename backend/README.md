# backend

## Environment Setup

---

### Virtual Environment

We recommend using [virtual environments](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment) to manage our environment and dependencies.

To create a virtual environment, run `python3 -m venv env`. This will create the virtual environment in the `./env` directory.

To activate the virtual environment, run `source env/bin/activate`. You can confirm you’re in the virtual environment by checking the location of your Python interpreter, `which python`, which should point to the `./env` directory.

If you want to leave your virtual environment, run `deactivate`.

### Installing Dependencies

To install all the dependencies, run `python3 -m pip install -r requirements.txt`.

Make sure to update this everytime a new package is installed. You can do this by doing `pip freeze > requirements.txt`

### Environment Variables

Secrets need to be stored as environment variables. To do this, create a `.env` file, and ask the current lead engineer for the latest values.

### Starting the Server and Database

Run docker-compose. Specify the `--build` flag so that it rebuilds the image and your latest changes are reflected.

```
docker-compose up --build -d
```

Exec into the server container, then run the initial django migrations

```
$ docker exec -it backend-server-1 sh

################ INSIDE CONTAINER ################
/app # python manage.py migrate

# verify that migrations ran succesfully
/app # python manage.py showmigrations
admin
 [X] 0001_initial
 [X] 0002_logentry_remove_auto_add
 [X] 0003_logentry_add_action_flag_choices
auth
 [X] 0001_initial
 [X] 0002_alter_permission_name_max_length
 [X] 0003_alter_user_email_max_length
 [X] 0004_alter_user_username_opts
 [X] 0005_alter_user_last_login_null
 [X] 0006_require_contenttypes_0002
 [X] 0007_alter_validators_add_error_messages
 [X] 0008_alter_user_username_max_length
 [X] 0009_alter_user_last_name_max_length
 [X] 0010_alter_group_name_max_length
 [X] 0011_update_proxy_permissions
 [X] 0012_alter_user_first_name_max_length
contenttypes
 [X] 0001_initial
 [X] 0002_remove_content_type_name
sessions
 [X] 0001_initial
```

## Developer Notes

---

### Database

The database schema notes can be found [here](https://docs.google.com/document/d/1-SlmfU0e92863UKGlA0pu6Gk3kdn6AjJeSBMwFx_WaY/edit?usp=sharing).

To completely erase the database data, `docker volume rm backend_pgdata`.

If for any reason you need to "delete" a migration record, delete it from the `django_migrations` table.

### pgvector

We use pgvector's Docker image for our postgresql deployment:
https://github.com/pgvector/pgvector#docker

https://github.com/pgvector/pgvector#indexing
By default, pgvector performs exact nearest neighbor search, which provides perfect recall.

We can add an index to use approximate nearest neighbor search, which trades some recall for performance. Unlike typical indexes, we will see different results for queries after adding an approximate index.

Note: Let's only add an index when the query latency starts to degrade.

### Django REST Framework

- Serializers provide serialization and deserialization, allowing parsed data to be converted back into complex types
- When deserializing data, you always need to call `is_valid()` before attempting to access the validated data, or save an object instance
- Calling `.save()` on a serializer will either create a new instance, or update an existing instance
-

## Deployment

### Startup Scripts

```
python manage.py populate_db
```
