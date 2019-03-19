#! /usr/bin/env bash

python -m venv env
source env/bin/activate
pip install --upgrade pip
pip install jupyterlab ipywidgets ipympl pandas scikit-learn

jupyter nbextension enable --py widgetsnbextension --sys-prefix
jupyter labextension install @jupyter-widgets/jupyterlab-manager
jupyter labextension install jupyter-matplotlib
