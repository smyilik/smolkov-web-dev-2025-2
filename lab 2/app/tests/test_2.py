# from contextlib import contextmanager
# from flask import template_rendered
# from unittest.mock import patch

import pytest
from app import app, check_phone_number, convert_phone_number

# @pytest.fixture
# def client():
#     with app.test_client() as client:
#         yield client

# # 1. Проверка отображения параметров URL
# def test_args_page_parameters_displayed(client):
#     response = client.get('/url_arguments?param1=value1&param2=value2')
#     html = response.get_data(as_text=True)
#     assert 'param1' in html and 'value1' in html
#     assert 'param2' in html and 'value2' in html

# # 2. Проверка отображения заголовков запроса
# def test_headers_page_headers_displayed(client):
#     response = client.get('/request_headers', headers={'Custom-Header': 'TestValue'})
#     html = response.get_data(as_text=True)
#     assert 'Custom-Header' in html and 'TestValue' in html

# # 3. Проверка отображения куки
# def test_cookies_page_cookies_displayed(client):
#     client.set_cookie('mycookie', 'cookievalue')
#     response = client.get('/cookie')
#     html = response.get_data(as_text=True)
#     assert 'mycookie' in html and 'cookievalue' in html

# # 4. Проверка отображения формы (GET-запрос)
# def test_form_page_get(client):
#     response = client.get('/form_parameters')
#     html = response.get_data(as_text=True)
#     # Форма должна присутствовать, а таблица с данными – отсутствовать, т.к. форма не отправлена.
#     assert '<form' in html
#     assert 'topic' not in html

# # 5. Проверка передачи данных формы (POST-запрос)
# def test_form_page_post(client):
#     data = {'topic': 'Test Theme', 'text': 'Test Text'}
#     response = client.post('/form_parameters', data=data)
#     html = response.get_data(as_text=True)
#     assert 'Test Theme' in html
#     assert 'Test Text' in html
#     # Таблица с отправленными данными должна быть видна
#     assert '<li' in html
# #
# #
# #
# # 6. Проверка валидации номера: недопустимые символы
# def test_phone_valid_invalid_symbol(client):
#     data = {'phone': '12345a78901'}  # содержит букву "a"
#     response = client.post('/phone_valid', data=data)
#     html = response.get_data(as_text=True)
#     assert "Недопустимый ввод. В номере телефона встречаются недопустимые символы." in html

# # 7. Проверка валидации номера: неверное количество цифр (меньше 11)
# def test_phone_valid_wrong_digit_count(client):
#     data = {'phone': '1234567890'}  # 10 цифр
#     response = client.post('/phone_valid', data=data)
#     html = response.get_data(as_text=True)
#     assert "Неверное количество цифр" in html

# # 8. Проверка корректного ввода номера: валидный номер с форматированием
# def test_phone_valid_correct_number(client):
#     phone_input = '8 912-345-67-89'
#     data = {'phone': phone_input}
#     response = client.post('/phone_valid', data=data)
#     html = response.get_data(as_text=True)
#     # Ошибки отсутствуют, поэтому не должно быть класса is-invalid
#     assert "is-invalid" not in html
#     # Ожидаемый отформатированный номер
#     assert '8-912-345-67-89' in html

# # 9. Проверка наличия класса Bootstrap is-invalid при ошибке валидации
# def test_phone_valid_bootstrap_class_on_error(client):
#     data = {'phone': '1234'}  # недостаточное количество цифр
#     response = client.post('/phone_valid', data=data)
#     html = response.get_data(as_text=True)
#     assert 'is-invalid' in html

# # 10. Тестирование функции fix_phone_format напрямую
# def test_fix_phone_format_function():
#     input_phone = '89123456789'
#     formatted = fix_phone_format(input_phone)
#     assert formatted == '8-912-345-67-89'

# # 11. Тестирование функции validate_phone: недопустимые символы
# def test_validate_phone_invalid_symbols():
#     error = validate_phone('12345a78901')
#     expected = "Недопустимый ввод. В номере телефона встречаются недопустимые символы."
#     assert error == expected

# # 12. Тестирование функции validate_phone: неверное количество цифр
# def test_validate_phone_wrong_digit_count():
#     error = validate_phone('1234567890')  # 10 цифр
#     assert "Неверное количество цифр" in error

# # 13. Тестирование функции validate_phone: корректный номер
# def test_validate_phone_valid():
#     error = validate_phone('89123456789')
#     assert error is None

# # 14. Проверка страницы phone_valid с использованием разрешённых символов (пробелы, скобки, тире, точка, +)
# def test_phone_valid_allowed_characters(client):
#     phone_input = '+8 (912) 345.67-89'
#     data = {'phone': phone_input}
#     response = client.post('/phone_valid', data=data)
#     html = response.get_data(as_text=True)
#     # В случае корректного ввода не должно быть ошибки и класс is-invalid отсутствует
#     assert "is-invalid" not in html
#     # Ожидаемый формат номера (извлечены все цифры)
#     expected = '8-912-345-67-89'
#     assert expected in html

# # 15. Проверка GET-запроса для страницы валидации номера: форма отображается без ошибок
# def test_phone_valid_get_request(client):
#     response = client.get('/phone_valid')
#     html = response.get_data(as_text=True)
#     # Отсутствует сообщение об ошибке (div с invalid-feedback)
#     assert 'invalid-feedback' not in html
#     # Поле ввода должно быть пустым
#     assert 'value=""' in html


# def test_cookies(client):
#     response = client.get("/cookies")
#     assert response.status_code == 200
#     assert response.headers["Set-Cookie"].startswith("Cats=meow")

#     response = client.get("/cookies")
#     assert response.status_code == 200
#     assert "Set-Cookie" in response.headers
#     assert "Cats=;" in response.headers["Set-Cookie"]

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
    assert 'test-cookie' in html and 'cookie-value' in html

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