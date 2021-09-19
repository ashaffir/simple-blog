# Simple Blog API project

A simple REST API based social network in Django where Users can sign up and create text posts, as well as view, like, and unlike other
Users’ posts.

# Run local server

1. Setup cirtual environment
   python3 -m venv venv
   . venv/bin/activate

2. Install dependencies
   pip install -r requirements.txt

3. ./manage.py runserver localhost:8999

# Docker

docker build -t tradecore-api -f DockerFile .
docker run -p 8999:8999 tradecore-api

# API Documentation

To see the list of the endpoints available, go to:
http://localhost:8999/api-docs/

# Running tests

./manage.py test

# Production Notes

- Add .env file with the real credentials, passwords, etc, to .gitignore so it is not uploaded to Github.

# Admin (if using the DB in the repository)

Username/Email: tradecore@tradecore.com
Password: Tradecore2021
