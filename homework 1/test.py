import subprocess
import pytest
from is_leap import is_leap
from matrix_mult import matrix_mult

INTERPRETER = 'python'

def run_script(filename, input_data=None):
    proc = subprocess.run(
        [INTERPRETER, filename],
        input='\n'.join(input_data if input_data else []),
        capture_output=True,
        text=True,
        check=False
    )
    return proc.stdout.strip()

test_data = {
    'python_if_else': [
        (['1'], ['Weird']),
        (['4'], ['Not Weird']),
        (['3'], ['Weird']),
        (['6'], ['Weird']),
        (['22'], ['Not Weird'])
    ],
    'arithmetic_operators': [
        (['1', '2'], ['3', '-1', '2']),
        (['10', '5'], ['15', '5', '50']),
        (['-17', '13'], ['-4', '-30', '-221'])
    ],
    'division': [
        (['3', '5'], ['0', '0.6']),
        (['1', '0'], ['Error! Division by 0.']),
        (['2', '1'], ['2', '2.0'])
    ],
    'loops': [
        (['3'], ['0', '1', '4']),
        (['1'], ['0']),
        (['10'], ['0', '1', '4', '9', '16', '25', '36', '49', '64', '81'])
    ],
    'print_function': [
        (['5'], ['12345'])
    ],
    'second_score': [
        (['5', '2 3 6 6 5'], ['5']),
        (['1', '2'], ['Error! Second score not found.'])
    ],
    'nested_list': [
        (['5', 'Harry', '37.21', 'Berry', '37.21', 'Tina', '37.2', 'Akriti', '36.6', 'Harsh', '39'], ['Berry', 'Harry']),
        (['2', 'Harry', '37.21', 'Berry', '37.21'], ['Error! Second score not found.']),
        (['6', 'Alice', '45.5', 'Bob', '36.0', 'Charlie', '45.5', 'David', '40.0', 'Eva', '36.0', 'Frank', '42.0'], ['Frank'])
    ],
    'lists': [
        (['4', 'append 1', 'append 2', 'insert 1 3', 'print'], ['[1, 3, 2]']),
        (['7', 'append 5', 'append 10', 'insert 1 7', 'pop', 'append 15', 'sort', 'print'], ['[5, 7, 15]']),
        (['12', 'insert 0 5', 'insert 1 10', 'insert 0 6', 'print', 'remove 6', 'append 9', 'append 1', 'sort', 'print', 'pop', 'reverse', 'print'],
            ['[6, 5, 10]', '[1, 5, 9, 10]', '[9, 5, 1]'])
    ],
    'swap_case': [
        (['Www.MosPolytech.ru'], ['wWW.mOSpOLYTECH.RU']),
        (['Pythonist 2'], ['pYTHONIST 2']),
        (['WhAtS uP dUdE?'], ['wHaTs Up DuDe?'])
    ],
    'split_and_join': [
        (['this is a string   '], ['this-is-a-string']),
        (['Pythonist 2'], ['Pythonist-2']),
        (['Hello World! I am a computer!'], ['Hello-World!-I-am-a-computer!'])
    ],
    'max_word': [
        (['сосредоточенности'])
    ],
    'price_sum': [
        (['6842.84 5891.06 6810.9'])
    ],
    'anagram': [
        (['aboba', 'bbaao'], ['YES']),
        (['-,.?', '?-.,'], ['YES']),
        (['frank', 'Frank'], ['NO']),
        (['Hello,', 'Hello'], ['NO'])
    ],
    'metro': [
        (['5', '1 3', '2 4', '3 5', '4 6', '5 7', '5'], ['2']),
        (['3', '10 20', '15 25', '20 30', '20'], ['2']),
        (['4', '1 10', '2 9', '3 8', '4 7', '5'], ['4']),
        (['2', '5 10', '15 20', '12'], ['0']),
        (['10', '1 10', '2 9', '3 8', '4 7', '5 6', '6 15', '7 14', '8 13', '9 12', '10 11', '10'], ['5'])
    ],
    'minion_game': [
        (['BANANA'], ['Стюарт 12']),
        (['HELLO'], ['Стюарт 10']),
        (['ABOBA'], ['Кевин 9']),
        (['APPLE'], ['Стюарт 9']),
        (['AAAA'], ['Кевин 10'])
    ],
    'is_leap': [
        (1900, False),
        (2016, True),
        (2000, True),
        (2001, False)
    ],
    'happiness': [
        (['3 2', '1 5 3', '3 1', '5 7'], ['1']),
        (['5 3', '1 5 7 2 3 0', '3 1 10', '5 7 11'], ['0']),
        (['5 3', '10 20 30 40 50', '10 30 50', '20 40'], ['1'])
    ],
    'pirate_ship': [
        (['1000 5', 'a,1001,777', 'b,300,300', 'c,200,250', 'd,600,100', 'e,400,200'],
         ['c 200 250', 'b 300 300', 'a 1001 777', 'e 400 200', 'd 600 100']),
        (['800 6', 'artifact1,300,1500', 'artifact2,200,800', 'artifact3,100,300', 'artifact4,150,600', 'artifact5,250,1000', 'artifact6,50,200'], 
         ['artifact1 300 1500', 'artifact6 50 200', 'artifact5 250 1000', 'artifact4 150 600', 'artifact2 200 800', 'artifact3 100 300']),
        (['100 4', 'Золото,50,500', 'Серебро,30,300', 'Драгоценные Камни,20,400', 'Пряности,40,200'],
         ['Драгоценные Камни 20 400', 'Серебро 30 300', 'Золото 50 500', 'Пряности 40 200'])
    ],
    'matrix_mult': [
        (3, ['1 2 3', '4 5 6', '7 8 9', '9 8 7', '6 5 4', '3 2 1'], ['30 24 18', '84 69 54', '138 114 90']),
        (3, ['1 4 3', '2 1 5', '3 2 1', '1 0 0', '0 1 0', '0 0 1'], ['1 4 3', '2 1 5', '3 2 1']),
        (2, ['4 2', '9 0', '3 1', '-3 4'], ['6 12', '27 9']),
        (5, ['1 2 3 4 5', '6 7 8 9 10', '11 12 13 14 15', '16 17 18 19 20', '21 22 23 24 25',
            '5 4 3 2 1', '10 9 8 7 6', '15 14 13 12 11', '20 19 18 17 16', '25 24 23 22 21'],
            ['275 260 245 230 215', '650 610 570 530 490', '1025 960 895 830 765', '1400 1310 1220 1130 1040', '1775 1660 1545 1430 1315'])
    ]
}

def test_hello():
    assert run_script('hello.py').split('\n') == ['Hello, world!']

@pytest.mark.parametrize("input_data, expected", test_data['python_if_else'])
def test_python_if_else(input_data, expected):
    assert run_script('python_if_else.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['arithmetic_operators'])
def test_arithmetic_operators(input_data, expected):
    assert run_script('arithmetic_operators.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['division'])
def test_division(input_data, expected):
    assert run_script('division.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['loops'])
def test_loops(input_data, expected):
    assert run_script('loops.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['print_function'])
def test_print_function(input_data, expected):
    assert run_script('print_function.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['second_score'])
def test_second_score(input_data, expected):
    assert run_script('second_score.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['nested_list'])
def test_nested_list(input_data, expected):
    assert run_script('nested_list.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['lists'])
def test_lists(input_data, expected):
    assert run_script('lists.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['swap_case'])
def test_swap_case(input_data, expected):
    assert run_script('swap_case.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['split_and_join'])
def test_split_and_join(input_data, expected):
    assert run_script('split_and_join.py', input_data).split('\n') == expected

@pytest.mark.parametrize("expected", test_data['max_word'])
def test_max_word(expected):
    assert run_script('max_word.py').split('\n') == expected

@pytest.mark.parametrize("expected", test_data['price_sum'])
def test_price_sum(expected):
    assert run_script('price_sum.py').split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['anagram'])
def test_anagram(input_data, expected):
    assert run_script('anagram.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['metro'])
def test_metro(input_data, expected):
    assert run_script('metro.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['minion_game'])
def test_minion_game(input_data, expected):
    assert run_script('minion_game.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['is_leap'])
def test_is_leap(input_data, expected):
    assert is_leap(input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['happiness'])
def test_happiness(input_data, expected):
    assert run_script('happiness.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['pirate_ship'])
def test_pirate_ship(input_data, expected):
    assert run_script('pirate_ship.py', input_data).split('\n') == expected

@pytest.mark.parametrize("n, lines, expected", test_data['matrix_mult'])
def test_matrix_mult(n, lines, expected):
    assert matrix_mult(n, *lines) == expected
