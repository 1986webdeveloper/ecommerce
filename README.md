## Product Management System 

## Features:
- Import data from CSV/Xlsx/Google spreadsheet format
- Export data in CSV/Xlsx format.
- Update product info according to requirement.
- Maintain data effectively.

This is simple product management system where we can Import data from CSV/Xlsx/Google-spreed-sheet and export data in CSV/Xlsx format.

## The following column fields are mandatory in CSV/Xlsx/Google spreadsheet to upload a file

- Product Name
- Description
- Category
- Brand
- Color
- Price(only two digits are allowed after decimal e.g = 250.89)
- Size
- Type

## Steps for installation:

1. Clone this project from repository using below command.

```shell script
$ git clone https://github.com/1986webdeveloper/ecommerce.git
$ cd ecommerce
```

2. Create virtual environment to install dependencies.

```shell script
$ virtualenv venv -p python3
``` 

3. Activate virtual environment.

```shell script
$ source venv/bin/activate
```

4. Install all the dependencies using below command.

```shell script
(venv)$ pip install -r requirements.txt
```

5. Setup PostgreSQL
    - Install the postgresql database in your local computer from the official [site link](https://www.postgresql.org/download/).
    
6. Create a new database using the postgresql command line

```shell script
$ CREATE DATABASE import_export
```

7. Change username and password for database in .env file according to your postgres configuration.
    - e.g  If your postgres username is 'ABC' and password is 'XYZ', then update .env file as
```
      DB_NAME=import_export
      DB_USER=postgres
      DB_PASSWORD=root
      DB_HOST=localhost
      DB_PORT=5432
```

8. Add other required setting in .env as following

```
      SECRET_KEY=(^dqz%gp6pcb3o6+@*=)xek6gka-*+komd(3frdhpl@k)wc001
      CLIENT_ID=XXXXXXX #google sheet client id 
      CLIENT_SECRET=XXXX #google sheet client secret
      DJANGO_DEBUG=True
```

9. After creating database apply migrations using below command

```shell script
(venv)$ python manage.py migrate
```

9. Run project on server using below command:
```shell script
(venv)$ python manage.py runserver
```

And navigate to `http://127.0.0.1:8000/`.