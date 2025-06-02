import pytest
from app import app, check_phone_number, convert_phone_number

<<<<<<< HEAD
# def test_cookies(client):
#     response = client.get("/cookies")
#     assert response.status_code == 200
#     assert response.headers["Set-Cookie"].startswith("Cats=meow")

#     response = client.get("/cookies")
#     assert response.status_code == 200
#     assert "Set-Cookie" in response.headers
#     assert "Cats=;" in response.headers["Set-Cookie"]

=======
>>>>>>> 2d732f36a24e017833c436988f26a7510ccb5374
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# 1. Проверка отображения всех параметров URL
def test_url_params_displayed(client):
    params = {'name': 'John', 'age': '30', 'city': 'New York'}
    response = client.get('/url_arguments', query_string=params)
    html = response.get_data(as_text=True)
    for key, value in params.items():
        assert key in html and value in html

# 2. Проверка отображения всех заголовков запроса
def test_request_headers_displayed(client):
    headers = {
        'User-Agent': 'TestAgent',
        'Accept-Language': 'en-US',
        'X-Custom-Header': 'TestValue'
    }
    response = client.get('/request_headers', headers=headers)
    html = response.get_data(as_text=True)
    for key, value in headers.items():
        assert key in html and value in html

# 3. Проверка установки и удаления куки
def test_cookie(client):
    client.set_cookie('test-cookie', 'cookie-value')
    response = client.get('/cookie')
    html = response.get_data(as_text=True)
    assert response.status_code == 200
    assert 'test-cookie' in html and 'cookie-value' in html
    assert response.headers["Set-Cookie"].startswith("Test-cookie=123")
    # new response, so page updates and
    # we are not supposed to have cookie anymore
    response = client.get('/cookie')
    assert response.status_code == 200
    assert "Set-Cookie" in response.headers
    assert "Test-cookie=;" in response.headers["Set-Cookie"]

# 4. Проверка отображения формы
def test_form_display(client):
    response = client.get('/form_parameters')
    html = response.get_data(as_text=True)
    assert '<form' in html
    # форма ещё не отправлена
    assert 'topic = ' not in html
    assert 'text = ' not in html

# 5. Проверка обработки данных формы
def test_form_submission(client):
    form_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'message': 'Hello, World!'
    }
    response = client.post('/form_parameters', data=form_data)
    html = response.get_data(as_text=True)
    for value in form_data.values():
        assert value in html

# 6. Проверка валидации номера: один пробел
def test_phone_validation_empty_input(client):
    response = client.post('/phone', data={'phone': ' '})
    html = response.get_data(as_text=True)
    assert 'Недопустимый формат. Неверное количество цифр в номере телефона.' in html
    assert 'invalid-feedback' in html

# 7. Проверка валидации номера: недопустимые символы
def test_phone_validation_invalid_chars(client):
    response = client.post('/phone', data={'phone': '8(abc)123-45-67'})
    html = response.get_data(as_text=True)
    assert 'Недопустимый формат. Указаны недопустимые символы.' in html
    assert 'invalid-feedback' in html

# 8. Проверка валидации номера: недостаточно цифр
def test_phone_validation_short_number(client):
    response = client.post('/phone', data={'phone': '8123456'})
    html = response.get_data(as_text=True)
    assert 'Недопустимый формат. Неверное количество цифр в номере телефона.' in html
    assert 'invalid-feedback' in html

# 9. Проверка валидации номера: слишком много цифр
def test_phone_validation_long_number(client):
    response = client.post('/phone', data={'phone': '8123456789012345'})
    html = response.get_data(as_text=True)
    assert 'Недопустимый формат. Неверное количество цифр в номере телефона.' in html
    assert 'invalid-feedback' in html

# 10. Проверка форматирования номера: различные форматы ввода
@pytest.mark.parametrize('input_phone,expected', [
    ('89123456789', '8-912-345-67-89'),
    ('8 912 345 67 89', '8-912-345-67-89'),
    ('8(912)345-67-89', '8-912-345-67-89'),
    ('+7 912 345-67-89', '8-912-345-67-89'),
    ('8-912-345-67-89', '8-912-345-67-89'),
])
def test_phone_formatting_various_inputs(client, input_phone, expected):
    response = client.post('/phone', data={'phone': input_phone})
    html = response.get_data(as_text=True)
    assert expected in html
    assert 'invalid-feedback' not in html

# 11. Проверка функции validate_phone: корректные номера
def test_validate_phone_correct_numbers():
    valid_numbers = [
        '89123456789',
        '8 912 345 67 89',
        '8(912)345-67-89',
        '+7 912 345-67-89'
    ]
    for number in valid_numbers:
        assert check_phone_number(number) == None

# 12. Проверка функции validate_phone: некорректные номера
def test_validate_phone_incorrect_numbers():
    invalid_numbers = [
        ('abc', 'Недопустимый формат. Указаны недопустимые символы.'),
        ('812345', 'Недопустимый формат. Неверное количество цифр в номере телефона.'),
        ('8123456789012345', 'Недопустимый формат. Неверное количество цифр в номере телефона.')
    ]
    for number, error in invalid_numbers:
        assert error in check_phone_number(number)

# 13. Проверка функции fix_phone_format
def test_fix_phone_format_function():
    test_cases = [
        ('89123456789', '8-912-345-67-89'),
        ('8 912 345 67 89', '8-912-345-67-89'),
        ('8(912)345-67-89', '8-912-345-67-89'),
        ('+7 912 345-67-89', '8-912-345-67-89')
    ]
    for input_phone, expected in test_cases:
        assert convert_phone_number(input_phone) == expected

# 14. Проверка начального состояния страницы валидации телефона
def test_phone_valid_initial_state(client):
    response = client.get('/phone')
    html = response.get_data(as_text=True)
    assert 'value=' in html
    assert 'invalid-feedback' not in html

# 15. Проверка отображения успешного результата валидации
def test_phone_valid_success_display(client):
    response = client.post('/phone', data={'phone': '8 912 345 67 89'})
    html = response.get_data(as_text=True)
    assert '8-912-345-67-89' in html
    assert 'invalid-feedback' not in html
