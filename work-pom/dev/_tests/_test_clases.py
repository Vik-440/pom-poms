from collections import namedtuple

import pytest # noqa: F401, E261
# from _Test_1._test_1 import set_data

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


# def test_defaults_ex():
#     t1 = set_data("Peter", "400", "fabulous animal", "$ 3'000")
#     t2 = "Peter has size 400 in stutus fabulous animal and has $ 3'000 money"
#     assert t1 == t2
