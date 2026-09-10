# Data Mining

If `mineria_datos` is already set up, skip to **Start working**.

## Create the environment (first time only)

With Miniconda installed, run these commands after cloning the project:

```sh
conda create --name mineria_datos python=3.10 numpy pandas jupyter ipykernel
conda activate mineria_datos
python -m ipykernel install --user --name mineria_datos --display-name "Python (mineria_datos)"
```

You only need to do this once on each computer.

## Start working

Open a terminal and run:

```sh
cd /Users/dtd/work/2-areas/uni/s7/data-mining
conda activate mineria_datos
code .
```

In VS Code:

1. Open a notebook (`.ipynb`).
2. Click **Select Kernel** and choose `mineria_datos` (or `Python (mineria_datos)`).
3. Run a cell with `Shift+Enter`.

Activate the environment again whenever you open a new terminal to work.

## Use Jupyter in your browser

After activating the environment in the project folder, run:

```sh
jupyter notebook
```

## Install libraries

Activate the environment before installing a library:

```sh
conda activate mineria_datos
conda install matplotlib
```

Replace `matplotlib` with the library you need. To install several at once:

```sh
conda install matplotlib seaborn scikit-learn
```

If a library is not available through Conda, use pip inside the active environment:

```sh
python -m pip install library_name
```

Replace `library_name` with the package name. Restart your notebook kernel after installing.

## Finish working

Save your notebooks. If Jupyter is running in the terminal, press `Ctrl+C` and confirm to stop it. Then run:

```sh
conda deactivate
```
