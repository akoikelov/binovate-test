# Binovate Test Application

1. Used framework libs: Django, django-rest-framework, django-rest-swagger
2. Database: PostgreSQL
3. Additional tools: Docker, docker-compose


How to run locally:

1. Run `docker-compose up` in project folder
2. Application is available under `localhost:5000` address
3. Admin site: `localhost:5000/admin`
4. Admin creds: admin1234 / admin
5. Additional users:
 - test1 / test1 
 - test2 / test2 

6. Swagger UI is under root page: `localhost:5000`
7. For authentication go to `http://localhost:5000/v1/auth/login/`