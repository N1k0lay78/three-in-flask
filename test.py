from requests import get, post, delete

test_get = False
test_post = False
test_delete = True

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
                     'id': int(input('Не используемый ID: '))}).json())
    print(get('http://localhost:5000/api/jobs/').json())

if test_delete:
    print('нет в базе')
    print(delete('http://localhost:5000/api/jobs/999').json())
    print('Успешно удалена')
    print(delete('http://localhost:5000/api/jobs/1').json())
    print(get('http://localhost:5000/api/jobs/').json())