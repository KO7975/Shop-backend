# **Simple instruction**

## How to start django project backend

### - before starting you need grab project from githab (git pull https://github.com/Dream-team-by-team-challenge/online_shop.git)

### - than you need to install requirements

#### - chack python installed or not (python --version   or   python3 --version)
####    if not visit site and dounload end install it https://www.python.org/downloads/
#### - upgrate installer (python -m pip install --upgrade pip)
#### - install requirements (pip install -r requirements.txt)

### - go to the backend dir where manage.py file stored

### - create file .env and inside it set :
####    * SECRET_KEY= random generated key
####    * EMAIL_HOST_USER= your email adress
####    * EMAIL_HOST_PASSWORD= your email host password (not your account password)


### - now you can start project with command  (python manage.py runserver)

### - if all done right You will see "Starting development server at http://127.0.0.1:8000/"

### - You can visit admin page http://127.0.0.1:8000/admin and login with EMAIL: admin@example.com, PASSWORD: 123456

### - tape this http://127.0.0.1:8000/auth/schema/swagger-ui/ url into your browser and you will see all api functionality

### - if you have questions please contact me by email: kiosya17@gmail.com or in telegram: @Pirat_17