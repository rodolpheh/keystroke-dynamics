# Installing and using the Jupyter notebooks

**This is a detailed description of the steps to obtain a working environment. For a quick start, execute the `deploy.sh` scrip**

Install Python 3.

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
pip install jupyterlab
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

That's all we need. You can start Jupyter lab with `jupyter lab`