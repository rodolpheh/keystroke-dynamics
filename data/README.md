# Installing and using the Jupyter notebooks

Install Python

Go into the wanted folder and type:

```bash
python -m venv ./env/
```

Start the environment with:

```bash
source env/bin/activate
```

Install Jupyter lab:

```bash
pip install jupyter-lab
```

Install matplotlib and widgets (nodejs will be necessary):

```bash
pip install ipympl
jupyter labextension install @jupyter-widgets/jupyterlab-manager
jupyter labextension install jupyter-matplotlib
```

Now we have initialised a basic environment with Jupyter (with widgets support). But we're half way to be able to work on the project.

```bash
pip install pandas scikit-learn
```

That's all we need (it seems for now, scikit haven't been tested with this guide). You can start Jupyter lab with `jupyter-lab`