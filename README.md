# E-Commerce

## Product Management System - E-commerce

##Features
- Import data in CSV/Xlsx/Google spreadsheet format
- Export data in CSV/Xlsx format.
- Update product info according to requirement.
- Maintain data effectively.

This is simple product management system where we can Import data from CSV/Xlsx/Google-spreed-sheet and export data in CSV/Xlsx format.

## Column requirements in CSV/Xlsx/Google spreadsheet to upload file:

- Product_name
- Description
- Category
- Brand
- Color
- Price(only 2 digits are allowed after decimal e.g = $250.89)
- Size
- Type

##Steps for Installation.

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

7. After creating database apply migrations using below command

```shell script
(venv)$ python manage.py migrate
```

8. Run project on server using below command:
```shell script
(venv)$ python manage.py runserver
```

And navigate to `http://127.0.0.1:8000/`.