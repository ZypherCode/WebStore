import sqlite3
from random import randint

from faker import Faker

# 1. Подключаемся к базе данных (создается файл, если его нет)
conn = sqlite3.connect('db/store.db')
cursor = conn.cursor()
Faker = Faker()

for _ in range(3000):
    all_ = randint(100, 1000)
    bought = randint(0, all_)
    stock = all_ - bought
    price = randint(37, 10672)
    all_marks = randint(0, bought) + 1
    good = randint(1, all_marks)
    bad = all_marks - good
    showed = randint(50, 618) + bought
    clicked = randint(bought, showed)

    cursor.execute('''INSERT INTO "main"."products"
    ("title", "tags", "content", "image", "stock", "price", "good_marks", "bad_marks", "showed", "clicked", "bought", "created_date", "is_private", "user_id")
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''', (Faker.text(60), 'test', Faker.text(300), 'img', stock, price, good, bad, showed, clicked, bought, Faker.date_time(), 0, 1))


conn.commit() # Сохраняем изменения