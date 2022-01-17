# Finance Management App with Django 💰

First personal project using Django to develop a web app for money management.
The main objective is learn to work with backend

## To-do list:
  - [x] Create login system
  - [x] Create multi bank accounts for same user
  - [ ] Make page responsive for several resolutions
  - [ ] Create graphs in extract
  - [ ] Create a user query interface

## To use:

First clone this repository
After install requirements (I recommend to create a virtual envirionment):

    pip install -r requirements.txt

Create database:

    python manage.py makemigrations && python manage.py migrate
    
Run server:

    python manage.py runserver
    
> The server will run, by default, in port 8000, you can change this, for example to run in port 5000:

    python manage.py runserver 5000
    
    
> For change ip address you need do give permission on [settings.py](finances/settings.py) in ALLOWED_HOSTS.


  
    

    

