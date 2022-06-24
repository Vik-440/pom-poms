# Є функція яка виокристовує бібліотеки для звернення в інтернет, якщо так
# можна виразитись. Ви повинні, зробити mock на requests так, щоб функія
# працювала. Для прикладу нехай response.text поверне GoodJob. в іделаі,
# я хочу щоб це було реалізовано у вигляді fixture.

import requests


def monthly_schedule(self, month):
    response = requests.get("http://company.com/{self.last}/{month}")
    if response.ok:
        return response.text
    else:
        return 'Bad Response!'
