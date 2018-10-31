headers = {
    'Content-Type': 'application/json',
}

data = '{\n"password": "password",\n "type": "normal",\n"username": "test-username"\n}'

response = requests.post('http://localhost:8000/api/v1/auth', headers=headers, data=data)
