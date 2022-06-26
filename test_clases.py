from collections import namedtuple
from mock import patch
import itertools

import pytest
from _Test_1._test_1 import set_data
from _Test_1.step_two import monthly_schedule

Task = namedtuple('Centaur', ['name', 'size', 'status', 'money'])
Task.__new__.__defaults__ = ("Peter", "400", "animal", "$3")


def test_defaults():
    t1 = Task()
    t2 = Task("Peter", "400", "animal", "$3")
    assert t1 == t2


def test_member_access():
    t = Task('Max', 80)
    assert t.name == 'Max'
    assert t.size == 80
    assert (t.status, t.money) == ("animal", "$3")


def test_asdict():
    t_task = Task('Mark', 90, 'people', 500)
    t_dict = t_task._asdict()
    expected = {'name': 'Mark',
                'size': 90,
                'status': 'people',
                'money': 500}
    assert t_dict == expected


def test_replace():
    t_before = Task('Mark', 90, 'people', False)
    t_after = t_before._replace(name='Stab', size=100)
    t_expected = Task('Stab', 100, 'people', False)
    assert t_after == t_expected


def test_defaults_ex():
    t1 = set_data("Peter", "400", "fabulous animal", "$ 3'000")
    t2 = "Peter has size 400 in stutus fabulous animal and has $ 3'000 money"
    assert t1 == t2


def test_get_employee(requests_mock):
    test_id = 'random-id'
    requests_mock.get(f'{__BASE_URL}/employee/{test_id}', json={
        'name': 'awesome-mock'})
    resp = get_employee('random-id')
    assert resp == {'name': 'awesome-mock'}


# def test_absent_employee(requests_mock):
#     test_id = 'does_not_exist'
#     requests_mock.get(f'{__BASE_URL}/employee/{test_id}', status_code=404)
#     with pytest.raises(HTTPError):
#         resp = get_employee(test_id)


def test_m_s(requests_mock):
    smg = 'GoodJob'
    requests_mock.get(f'http://company.com/{self.last}/{month}')
    assert 

# def monthly_schedule(self, month):
#     response = requests.get("http://company.com/{self.last}/{month}")
#     if response.ok:
#         return response.text
#     else:
#         return 'Bad Response!'

# >>> def test_simple(requests_mock):
# ...    requests_mock.get('http://test.com', text='data')
# ...    assert 'data' == requests.get('http://test.com').text