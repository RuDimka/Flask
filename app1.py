from flask import Flask, abort, request
import random

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, World!"


about_me = {
   "name": "Dmitry",
   "surname": "Baryshnikov",
   "email": "d.v.baryshnikovv@gmail.com"
}


@app.route("/about")
def about():
    return about_me



app.config['JSON_AS_ASCII'] = False

# работа по индексам сразу for и if
quotes_about_programming = [
    {
        "id": 1,
        "autor": "Mosher’s Law of Software Engineering",
        "text": "Не волнуйтесь, если что-то не работает. Если бы всё работало, вас бы уволили."
    },
    {
        "id": 2,
        "autor": "Yoggi Berra.",
        "text": " В теории, теория и практика неразделимы. На практике это не так."
    },
    {
        "id": 3,
        "autor": "Brian W. Kernighan",
        "text": "Отладка кода вдвое сложнее, чем его написание. Так что если вы пишете код настолько умно, "
                "насколько можете, то вы по определению недостаточно сообразительны, чтобы его отлаживать."
    },
    {
        "id": 4,
        "autor": "Larry Wall",
        "text": "Многие из вас знакомы с достоинствами программиста. Их всего три, и разумеется это: лень, "
                "нетерпеливость и гордыня."
    },
    {
        "id": 5,
        "autor": "Edsger W. Dijkstra",
        "text": "Помимо математических способностей, жизненно важным качеством программиста является исключительно хорошее владение родным языком."
    },
    {
        "id": 6,
        "autor": "H. L. Mencken",
        "text": "Для каждой сложной задачи существует решение, которое является быстрым, простым и неправильным."
    },
    {
        "id": 7,
        "autor": "Bjarne Stroustrup",
        "text": "Механизмы управления доступом в С++ обеспечивают защиту от несчастного случая, но не от мошенников."
    },
    {
        "id": 8,
        "autor": "Steve McConnell",
        "text": "Тестирование не позволяет обнаружить такие ошибки, как создание не того приложения."
    },
    {
        "id": 9,
        "autor": "Jamie Zawinski",
        "text": "Некоторые люди во время решения некой проблемы думают: «Почему бы мне не использовать регулярные выражения?». После этого у них уже две проблемы…"
    },
    {
        "id": 10,
        "autor": "Richard Stallman",
        "text": "Я не умею делать скриншоты, потому что я обычно работаю на компьютере в текстовом режиме."
    },
]


@app.route("/quotes")
def quotes():
    return quotes_about_programming


about_python = {
    "hystory": "История языка программирования Python началась в конце 1980-х. Гвидо ван Россум задумал Python в 1980-х годах[1], а приступил к его созданию в декабре 1989 года[2]" 
               "в центре математики и информатики в Нидерландах. Язык Python был задуман как потомок языка программирования ABC, способный к обработке исключений и взаимодействию" 
               "с операционной системой Амёба[3]. Ван Россум является основным автором Python и продолжал выполнять центральную роль в принятии решений относительно развития языка" 
               "вплоть до 12 июля 2018 года[4].Версия Python 2.0 была выпущена 16 октября 2000 года и включала в себя много новых крупных функций — таких как полный сборщик мусора и поддержка Unicode. Однако наиболее важным из всех изменений было изменение самого процесса развития языка и переход на более прозрачный процесс его создания[5]."
                "Первая обратно-несовместимая версия Python 3.0 была выпущена 3 декабря 2008[6] года после длительного периода тестирования. Многие её функции были портированы и обратно совместимы с Python 2.6 и Python 2.7[7]."
}


@app.route("/python")
def get_python():
    return about_python



@app.route("/quotes/<int:id>")#хинтинг входящего urla
def get_quotes(id):
    for x in quotes_about_programming:
        if x["id"] == id:
            return x
    abort(404, f"Quote with id={id} not found")


@app.route("/quotes/random")
def get_random():
    return random.choice(quotes_about_programming), 200



@app.route("/quotes", methods=['POST'])
def create_quote():
    new_quote = request.json
    # print(new_quote)
    last_id = quotes_about_programming[-1]["id"]
    new_quote["id"] = last_id + 1
    quotes_about_programming.append(new_quote)
    return new_quote, 201 #201 OK, created


# @app.post("/quotes")
# def create_quote():
#     new_quote = request.json
#     last_id = quotes_about_programming[-1]["id"]
#     new_quote["id"] = last_id + 1
#     quotes_about_programming.append(new_quote)
#     return new_quote, 201


@app.route("/quotes/<int:id>", methods=['PUT'])
def update_quotes(id):
    new_data = request.json
    print(new_data)
    for x in quotes_about_programming:
        if x["id"] == id:
            x.update(new_data)
            return x


@app.route("/quotes/<int:id>", methods=['DELETE'])
def delete(id):
    for x in quotes_about_programming:
        if id == x['id']:
            quotes_about_programming.remove(x)
            return f"Quote with id {id} is deleted.", 200
        print("Цитата удалена")
    abort(404, f"Указанного id= {id}, не существует")


@app.route("/quotes", methods=['DELETE'])
def delete_all_quotes():
    for x in quotes_about_programming:
        quotes_about_programming.clear()
        return f"Quotes all deleted!", 200
    print("Все цитаты удалены")
    abort(404, f"Цитаты отстутсвуют в данном разделе сайта")


@app.route("/quotes/<int:id>", methods=['POST'])
def update_all_quotes(id):
    new_all_date = request.json
    new_all_date = []
    # print(new_all_date)
    # for x in quotes_about_programming:
    quotes_about_programming.update(new_all_date)
    return new_all_date, 201


# @app.route("/quotes/<int:id>", methods=['POST'])
# def get_rating(id):
#     rating_quotes = request.json
#     last_id = quotes_about_programming[-1]["id"]
#     rating_quotes =

print()








if __name__ == "__main__":  # старт сервера
    app.run(debug=True)
