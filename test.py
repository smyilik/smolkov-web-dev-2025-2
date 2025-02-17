import subprocess
import pytest

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
        (['10', '5'], ['15', '5', '50'])
    ],
    'division': [
        (['3', '5'], ['0', '0.6']),
        (['1', '0'], ['Error! Division by 0.']),
        (['2', '1'], ['2', '2.0'])
    ],
    'loops': [
        (['3'], ['0', '1', '4']),
        (['1'], ['0'])
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
        (['2', 'Harry', '37.21', 'Berry', '37.21'], ['Error! Second score not found.'])
    ],
    'lists': [
        (['4', 'append 1', 'append 2', 'insert 1 3', 'print'], ['[1, 3, 2]']),
        (['12', 'insert 0 5', 'insert 1 10', 'insert 0 6', 'print', 'remove 6', 'append 9', 'append 1', 'sort', 'print', 'pop', 'reverse', 'print'],
            ['[6, 5, 10]', '[1, 5, 9, 10]', '[9, 5, 1]'])
    ],
    'swap_case': [
        (['Www.MosPolytech.ru'], ['wWW.mOSpOLYTECH.RU']),
        (['Pythonist 2'], ['pYTHONIST 2'])
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
