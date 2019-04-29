import os
import glob
import pickle

# CLI style imports
from PyInquirer import prompt
from examples import custom_style_2

from termgraph.termgraph import chart, AVAILABLE_COLORS as colors


def get_file_list(folder: str, extension: str) -> "List[str]":
    """Get the list of candidate files in `sequence/` dir"""
    filenames = []
    os.makedirs(folder, exist_ok=True)
    for file in glob.glob(folder + "/*." + extension):
        filenames.append({'name': file.replace(folder + "/", "")})
    return filenames


def get_path() -> str:
    """Path of current dir"""
    return os.path.dirname(os.path.realpath(__file__))


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


def get_existing_filename(existing_files: "List[str]", multiple: bool = False) -> str:
    """Choose file name from a list of filenames"""

    # Ask user which file only if there are multiple files

    if len(existing_files) == 1:
        return existing_files[0]["name"]

    plural = '(s)' if multiple else ''

    questions = [
        {
            'type': 'checkbox' if multiple else 'list',
            'name': 'target_filename',
            'message': 'Which file' + plural + ' do you want to load ?',
            'choices': existing_files
        }
    ]
    return prompt(questions, style=custom_style_2)["target_filename"]


def print_report(report):
    print("\n# Metrics\n")
    labels = ['User', 'Impostor']
    data = [
        [report["TP"], report["FN"]],
        [report["TN"], report["FP"]]
    ]
    args = {
        'stacked': True, 'width': 80, 'no_labels': False, 'format': '{:<5.2f}',
        'suffix': '', "vertical": False
    }
    chart(colors=[
        colors['green'],
        colors['red']
        ], data=data, args=args, labels=labels)

    print("\n# Evaluation\n")
    labels = ['Precision', 'Recall', 'F1', 'Accuracy']
    data = [
        [report["precision"] * 100],
        [report["recall"] * 100],
        [report["f1"] * 100],
        [report["accuracy"] * 100]
    ]
    args = {
        'stacked': False, 'width': 50, 'no_labels': False,
        'format': '{:<5.2f}', 'suffix': '', "vertical": False
    }
    chart(colors=[], data=data, args=args, labels=labels)


def get_sequence_from_file(filename: str) -> "List[Sample]":
    """Recover sequence of samples from file"""
    samples = []

    with open(get_path() + "/sequence/" + filename, "rb") as file:
        while True:
            try:
                samples.append(pickle.load(file))
            except EOFError:
                break
    return samples
