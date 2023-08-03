# **Simple instruction**

## How to start django project shop backend

1. Before starting you need clone project from githab 

```bash
git clone https://github.com/KO7975/Shop-backend.git
```

2.
```bash
cd backend
```

3. Create a virtual environment for the project:

```bash
python -m venv env
```

4. Activate the virtual environment:

```bash
source env/bin/activate
```

5. Install the project dependencies:

```bash
pip install -r requirements.txt
```

6. For propper work in file .env fill your secretkeys :

   * SECRET_KEY= random generated key
   * EMAIL_HOST_USER= your email adress
   * EMAIL_HOST_PASSWORD= your email host password (not your account password)
   * FACEBOOK_KEY = from facebook generated
   * FACEBOOK_SECRET = from facebook generated
   * GOOGLE_OAUTH2_KEY = from google generated
   * GOOGLE_OAUTH2_SECRET = from google generated

7. Start the development server:

```bash
python manage.py runserver
```

8. You can visit admin page 

```bash
http://127.0.0.1:8000/admin
```
and login with EMAIL: 

```bash
 admin@example.com
```
PASSWORD: 

```bash
 123456
```

9. Use this [url](http://127.0.0.1:8000/schema/swagger-ui/)  into your browser and you will see all api functionality

10. If you have questions please contact me by email: kiosya17@gmail.com or in telegram: @Pirat_17