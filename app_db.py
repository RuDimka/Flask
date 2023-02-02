import random
import sqlite3
from flask import Flask, abort, request
from flask import g  #импортируем все ф-ции, методы библиотеки Flask
from pathlib import Path

BASE_DIR = Path(__file__).parent #путь к файлу родительской директории
DATABASE = BASE_DIR / "test.db"

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# Сериализация: list --> str
@app.route("/quotes")# Если метод не указан он всегда GET
def get_all_quotes():
    # Подключение в БД
    connection = get_db()
    cursor = connection.cursor()
    select_quotes = "SELECT * from quotes"
    cursor.execute(select_quotes)
    quotes_db = cursor.fetchall() #возврат списка всех строк
    cursor.close()
    quotes = []
    keys = ["id", "author", "text", "rating"]
    for quote_db in quotes_db:
        quote = dict(zip(keys, quote_db))#объединяет ключ значение в виде словаря
        quotes.append(quote)
    print(quotes)
    return quotes


@app.route("/quotes/<int:id>")
def get_quote(id):
    connection = get_db()
    cursor = connection.cursor()
    select_quotes = f"SELECT * FROM quotes WHERE id={id};"
    # select_quotes = "SELECT * FROM quotes WHERE id=2;"
    cursor.execute(select_quotes)
    quote_db = cursor.fetchone()
    # print("quote_db = ", quote_db)
    cursor.close()
    if quote_db is None:
        abort(404, f"Quote with id={id} not found")
    keys = ["id", "author", "text"]
    quote = dict(zip(keys, quote_db))
    return quote


@app.route("/quotes", methods=['POST'])
def create_quote():
    quote_data = request.json #Запрашиваем из Postman json и сохраняем в qoute_data словарь
    # print(quote_data)
    connection = get_db()
    cursor = connection.cursor()
    create_quote = "INSERT INTO quotes (author, text, rating) VALUES (?, ?, ?)" # Если не знаем имена и параметры столбцов указываем ?. Количество вопросов == количество столбцов
    cursor.execute(create_quote, (quote_data["author"], quote_data["text"], quote_data["rating"]))
    connection.commit() #При методе POST всегда прописываем commit для фиксации транзакции в БД
    cursor.close()
    return {}, 201


@app.route("/quotes/<int:quote_id>", methods=['PUT'])
def edit_quote(quote_id):
    quote_data = request.json
    print(quote_data)
    connection = get_db()
    cursor = connection.cursor()
    new_quote_data = (quote_data["author"], quote_data["text"], quote_data["rating"])#Сохранено в кортеже
    update_quote = "UPDATE quotes SET author=?, text=?, rating=? WHERE id=?"# Обновленные цитаты устанавливаются значения автор, текст, id
    cursor.execute(update_quote, (*new_quote_data, quote_id))
    connection.commit()
    print("cursor.rowcount = ", cursor.rowcount)
    cursor.close()
    if cursor.rowcount == 0:
        abort(404, f"Указанного id= {quote_id}, не существует")
    return {}, 200


@app.route("/quotes/filter")
def get_quotes_filter():
    args = request.args
    print(args)
    # TODO: закончить реализацию
    return {}


@app.route("/quotes/<int:id>", methods=['DELETE'])
def delete(id):
    for quote in quotes:
        if id == quote['id']:
            quotes.remove(quote)
            return f"Quote with id {id} is deleted.", 200
    abort(404, f"Указанного id= {id}, не существует")


# @app.route("quote/<int:rating/>")
# def get_rating(rating):
#     connection = get_db()
#     cursor = connection.cursor()
#     select_quotes = f"SELECT * FROM quotes WHERE rating={rating}:"
#     cursor.execute(select_quotes)
#     quote_db = cursor.fetchone()
#     cursor.close()
#     if quote_db is None:
#         abort(404, f"Quotes with rating={rating} not found")
#     return {}, 201


# @app.route("/quotes/<int:rating>", methods=['DELETE'])
# def delete_by_rating(rating):
#     for quote in quotes:
#         if rating == quote['rating']:
#             quotes.remove(quote)
#             return f"Quote with rating {rating} is delete!", 200
#     abort(404, f"Цитат с указанным rating={rating}, не существует")


if __name__ == "__main__":
    app.run(debug=True)
