# ecommerce

## Setup

The first thing to do is to clone the repository:

```shell script
$ git clone https://github.com/1986webdeveloper/ecommerce.git
$ cd ecommerce
```

Create a virtual environment to install dependencies in and activate it:

Install python 3 and virtual environment 

Make virtualenv for ecommerce :


```shell script
$ virtualenv venv -p python3
``` 
 
Activate virtual environment : 


```shell script
$ source venv/bin/activate
```

Then install the dependencies:

```shell script
(venv)$ pip install -r requirements.txt
```

Once `pip` has finished downloading the dependencies:

Make database in postgresql and update database settings in settings.py file.


Apply Migrations:

```shell script
(venv)$ python manage.py migrate
```

Run server :
```shell script
(venv)$ python manage.py runserver
```

And navigate to `http://127.0.0.1:8000/`.