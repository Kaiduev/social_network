# Social Network

## First you need to install a docker to your machine:

[Docker](https://www.docker.com)

## To start the project, use this command:

``docker-compose up --build``

## Here is the API documentation:

[localhost/swagger](localhost/swagger)

## Before starting the bot, you need to create and activate venv after install requirements from [requirements.txt]() file:
``python -m venv venv``<br/>
``source venv/bin/activate``<br/>
``pip install -r requirements``
## To start the bot, go to the automated_bot directory and run:
``python bot.py``
## You can also change the input values in [config.json]() file:
``
{
  "number_of_users": 5,
  "max_posts_per_user": 5,
  "max_likes_per_user": 5 
}
``

