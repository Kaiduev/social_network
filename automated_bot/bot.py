import json
import random

import requests
from decouple import config
from faker import Faker
from sqlalchemy import create_engine, MetaData, Table

fake = Faker()


class Utils:

    @staticmethod
    def clear_database():
        print("---Cleaning up existing data---")
        table_names = ["blog_like", "blog_post", "accounts_user"]
        database_url = config('DATABASE_URL')
        engine = create_engine(database_url)
        metadata = MetaData()
        connection = engine.connect()
        for table_name in table_names:
            table = Table(table_name, metadata)
            delete_statement = table.delete()
            connection.execute(delete_statement)
            connection.commit()
            print(f"---All data has been deleted from the '{table_name}' table---")
        connection.close()
        with open("generated_users.json", "w", encoding="utf-8") as json_file:
            json.dump([], json_file, ensure_ascii=False, indent=4)
        with open("generated_posts.json", "w", encoding="utf-8") as json_file:
            json.dump([], json_file, ensure_ascii=False, indent=4)


class Bot:

    def __init__(self, path_to_config_file):
        self.base_url = "http://localhost/api/"
        with open(path_to_config_file, 'r') as f:
            self.config = json.load(f)

    def _login(self, email, password):
        data = {
            "email": email,
            "password": password
        }
        resp = requests.post(url=self.base_url + "token/", data=data)
        if resp.status_code == 200:
            access_token = resp.json().get('access')
            return {"access": f"JWT {access_token}"}
        return {"access": None}

    def _generate_number_of_users(self):
        number_of_users = self.config.get('number_of_users', 0)
        generated_users = list()
        for i in range(number_of_users):
            password = fake.password()
            data = {
                "email": fake.email(),
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "birth_date": fake.date(),
                "bio": fake.text(),
                "password": password,
                "confirm_password": password,
            }
            try:
                resp = requests.post(url=self.base_url + "sign-up/", data=data)
                if resp.status_code == 201:
                    access_token = self._login(email=data.get("email"), password=data.get("password"))
                    data.update(access_token)
                    generated_users.append(data)
            except Exception as e:
                print(e)
        with open("generated_users.json", "w", encoding="utf-8") as json_file:
            json.dump(generated_users, json_file, ensure_ascii=False, indent=4)
        print(f"Generated numbers of users: {number_of_users}")

    def _generate_max_posts_per_user(self):
        max_posts_per_user = self.config.get('max_posts_per_user', 0)
        generated_posts = list()
        with open("generated_users.json", "r", encoding="utf-8") as json_file:
            generated_users = json.load(json_file)
        for generated_user in generated_users:
            for i in range(max_posts_per_user):
                access_token = generated_user.get("access")
                data = {
                    "title": fake.sentence(),
                    "image": fake.image_url(),
                    "description": fake.text(),

                }
                resp = requests.post(
                    url=self.base_url + "posts/",
                    data=data, headers={"Authorization": access_token}
                )
                if resp.status_code == 201:
                    generated_posts.append(resp.json())
            with open("generated_posts.json", "w", encoding="utf-8") as json_file:
                json.dump(generated_posts, json_file, ensure_ascii=False, indent=4)
        print(f"Generated max posts per user: {max_posts_per_user}")

    def _generate_max_likes_per_user(self):
        max_likes_per_user = self.config.get('max_likes_per_user', 0)
        with open("generated_users.json", "r", encoding="utf-8") as json_file:
            generated_users = json.load(json_file)
        with open("generated_posts.json", "r", encoding="utf-8") as json_file:
            generated_posts = json.load(json_file)
        for generated_user in generated_users:
            access_token = generated_user.get("access")
            randomly_selected_posts = random.sample(generated_posts, max_likes_per_user)
            for randomly_selected_post in randomly_selected_posts:
                requests.post(
                    url=self.base_url + f'posts/{randomly_selected_post.get("id")}/like/',
                    headers={"Authorization": access_token}
                )
        print(f"Generated max likes per user: {max_likes_per_user}")

    def run(self):
        Utils.clear_database()
        print("---- Start Generating ----")
        self._generate_number_of_users()
        self._generate_max_posts_per_user()
        self._generate_max_likes_per_user()
        print("---- End Generating ----")


bot = Bot("config.json")
bot.run()
