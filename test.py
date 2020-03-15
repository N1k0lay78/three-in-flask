from requests import get

print(print(get('http://localhost:5000/api/jobs/').json()))
print(get('http://localhost:5000/api/jobs/1').json())
print(get('http://localhost:5000/api/jobs/100').json())
print(get('http://localhost:5000/api/jobs/c').json())
