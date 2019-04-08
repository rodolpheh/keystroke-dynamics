# -*- coding: utf-8 -*-

import sample_recorder
import trainer

# CLI style imports
from PyInquirer import prompt
from examples import custom_style_2


def program_menu():
    items = ["Sample recorder", "Trainer"]
    options = [
        {
            'type': 'list',
            'name': 'menu_items',
            'message': 'Which program do you want to load ?',
            'choices': items
        }
    ]

    return prompt(options, style=custom_style_2)['menu_items']


def menu():
    choice = program_menu()

    print("You chose {}".format(choice))
    if choice == "Sample recorder":
        sample_recorder.sample_recorder()
    else:
        trainer.trainer()


if __name__ == '__main__':
    menu()