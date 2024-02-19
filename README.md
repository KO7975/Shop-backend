# **Simple instruction**


1. Before starting you need clone project from githab 

```bash
git clone https://github.com/KO7975/Shop-backend.git
```

## How to start django project shop backend in Docker container

1. Go to the directory with the Dockerfile and Create Docker image
```bash
docker build -t shop .
```

2. Run docker container 
```bash
docker run -d -p 8000:8000 --name PINI shop
```

## Alternative start app on local machine

1. 
```bash
cd backend
```

2. Create a virtual environment for the project:

```bash
python -m venv env
```

3. Activate the virtual environment:

```bash
source env/bin/activate
```

4. Install the project dependencies:

```bash
pip install -r requirements.txt
```

5. For propper work in file .env fill your secretkeys 
   (remember when in production keep this values in secret):

   * SECRET_KEY= random generated key
   * EMAIL_HOST_USER= your email adress
   * EMAIL_HOST_PASSWORD= your email host password (not your account password)
   * FACEBOOK_KEY = from facebook generated
   * FACEBOOK_SECRET = from facebook generated
   * GOOGLE_OAUTH2_KEY = from google generated
   * GOOGLE_OAUTH2_SECRET = from google generated

6. Start the development server:

```bash
python manage.py runserver
```

7. You can visit admin page 

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

8. Use this [url](http://127.0.0.1:8000/)  into your browser

9. If you have questions please contact me by email: kiosya17@gmail.com or in telegram: @Pirat_17
