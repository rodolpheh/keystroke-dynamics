# -*- coding: utf-8 -*-

import sample_recorder
import trainer
import tester
import evaluator

# CLI style imports
from PyInquirer import prompt
from examples import custom_style_2


def get_binary_validation(message: str, default: bool = True) -> bool:
    """Validation on a binary alternative"""
    questions = [
        {
            'type': 'confirm',
            'message': message,
            'name': 'confirmed',
            'default': default,
        }
    ]
    return prompt(questions, style=custom_style_2)["confirmed"]


def program_menu():
    items = ["Sample recorder", "Trainer", "Evaluator", "Tester"]
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
    print('''
\u001b[38;5;9;1mdP       .d88888b    dP
\u001b[38;5;10;1m88       88.    "'   88
\u001b[38;5;11;1m88  .dP  `Y88888b. d8888P 88d888b. .d8888b. dP.  .dP
\u001b[38;5;12;1m88888"         `8b   88   88'  `88 88'  `88  `8bd8'
\u001b[38;5;13;1m88  `8b. d8'   .8P   88   88       88.  .88  .d88b.
\u001b[38;5;14;1mdP   `YP  Y88888P    dP   dP       `88888P' dP'  `dP
\u001b[0m
    ''')

    is_running = True
    while is_running:
        choice = program_menu()

        if choice == "Sample recorder":
            sample_recorder.main()
        elif choice == "Trainer":
            trainer.main()
        elif choice == "Evaluator":
            evaluator.main()
        else:
            tester.main()

        again = get_binary_validation("Do you want to load another program ?", False)
        if not again:
            is_running = False


if __name__ == '__main__':
    menu()
