# Simple Blog API project

A simple REST API based social network in Django where Users can sign up and create text posts, as well as view, like, and unlike other
Users’ posts.

# Run the server

## Local

./manage runserver localhost:8999

## Docker

docker build -t tradecore-api -f DockerFile .
docker run -p 8999:8999 tradecore-api

# API Documentation

To see the list of the endpoints available, go to:
http://localhost:8999/api-docs/

# Running tests

./manage.py test

# Production Notes

- Make sure that the .env file with the real credentials, passwords, etc, is not uploaded to Github.

# Admin

Username/Email: tradecore@tradecore.com
Password: Tradecore2021
