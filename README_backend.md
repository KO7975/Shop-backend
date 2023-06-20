# **Simple instruction**

## How to start django project backend

   1. Before starting you need grab project from githab (git pull https://github.com/Dream-team-by-team-challenge/online_shop.git)

   2. Than you need to install requirements

      - chack python installed or not (python --version   or   python3 --version) if not visit site and download and install it https://www.python.org/downloads/
      - upgrate installer (python -m pip install --upgrade pip)
      - install requirements (pip install -r requirements.txt)

   3. Go to the backend dir where manage.py file stored

   4. Create file .env and inside it set :

      * SECRET_KEY= random generated key
      * EMAIL_HOST_USER= your email adress
      * EMAIL_HOST_PASSWORD= your email host password (not your account password)
      * FACEBOOK_KEY = from facebook generated
      * FACEBOOK_SECRET = from facebook generated
      * GOOGLE_OAUTH2_KEY = from google generated
      * GOOGLE_OAUTH2_SECRET = from google generated

   5. Now you can start project with command  (python manage.py runserver)

   6. If all done right You will see "Starting development server at http://127.0.0.1:8000/"

   7. You can visit admin page http://127.0.0.1:8000/admin and login with EMAIL: admin@example.com, PASSWORD: 123456

   8. Tape this http://127.0.0.1:8000/auth/schema/swagger-ui/ url into your browser and you will see all api functionality

   9. If you have questions please contact me by email: kiosya17@gmail.com or in telegram: @Pirat_17