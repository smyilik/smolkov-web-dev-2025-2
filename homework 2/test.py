import subprocess
import pytest

INTERPRETER = 'python3'

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
    'fact': [
        (5, 120)
    ],
    'show_employee': [
        (['a b c', 10], 'a b c: 10 ₽'),
        ('a b c', 'a b c: 100000 ₽')
    ],
    'sum_and_sub': [
        (1, 2, [3, -1])
    ],
    'process_list': [
        ([1, 2, 3, 4])
    ],
    'my_sum': [
        ([1, 2, 3, 4], 10)
    ]
}

from fact import fact_it, fact_rec
from show_employee import show_employee
from sum_and_sub import sum_and_sub
from process_list import process_list, process_list_gen
from my_sum import my_sum

@pytest.mark.parametrize("input_data, expected", test_data['fact'])
def test_fact_it(input_data, expected):
    assert fact_it(input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['fact'])
def test_fact_rec(input_data, expected):
    assert fact_rec(input_data) == expected

#
@pytest.mark.parametrize("input_data, expected", test_data['show_employee'])
def test_show_employee(input_data, expected):
    assert show_employee(*input_data) == expected

@pytest.mark.parametrize("input_data_1, input_data_2, expected", test_data['sum_and_sub'])
def test_sum_and_sub(input_data_1, input_data_2, expected):
    assert sum_and_sub(input_data_1, input_data_2) == expected

@pytest.mark.parametrize("input_data", test_data['process_list'])
def test_process_list(input_data):
    assert process_list(input_data) == process_list_gen(input_data)

@pytest.mark.parametrize("input_data, expected", test_data['my_sum'])
def test_my_sum(input_data, expected):
    assert my_sum(*input_data) == expected
