from requests import get, post, delete, put
from flask import Flask


test = False
if test:
    test_get = False
    test_post = False
    test_delete = False
    test_put = True

    if test_get:
        print(print(get('http://localhost:5000/api/jobs/').json()))
        print(get('http://localhost:5000/api/jobs/1').json())
        print(get('http://localhost:5000/api/jobs/100').json())
        print(get('http://localhost:5000/api/jobs/c').json())

    if test_post:
        print('пустой запрос')
        print(post('http://localhost:5000/api/jobs').json())
        print('не полный запрос')
        print(post('http://localhost:5000/api/jobs',
                   json={'job': 'Заголовок'}).json())
        print('желаемый id уже занят')
        print(post('http://localhost:5000/api/jobs',
                   json={'job': 'Заголовок',
                         'team_leader': 1,
                         'work_size': 1,
                         'collaborators': "все",
                         'is_finished': True,
                   'id': 1}).json())
        print('правильный запрос')
        print(post('http://localhost:5000/api/jobs',
                   json={'job': 'Заголовок',
                         'team_leader': 1,
                         'work_size': 1,
                         'collaborators': "все",
                         'is_finished': True,
                         'id': 10}).json())
        print(get('http://localhost:5000/api/jobs/').json())

    if test_delete:
        print('нет в базе')
        print(delete('http://localhost:5000/api/jobs/999').json())
        print('Успешно удалена')
        print(delete('http://localhost:5000/api/jobs/1').json())
        print(get('http://localhost:5000/api/jobs/').json())

    if test_put:
        print('нет в базе')
        print(put('http://localhost:5000/api/jobs/999').json())
        print('Успешно изменена')
        print(put('http://localhost:5000/api/jobs/10',
                   json={'job': 'нет загаловка',}).json())
        print(get('http://localhost:5000/api/jobs/').json())


app = Flask(__name__)


@app.route("/")
def index():
    return "Привет от приложения Flask"


if __name__ == '__main__':
    app.run()