# Miniconda + VS Code para Minería de Datos (macOS Apple Silicon)

Fecha de verificación: 23 de agosto de 2026.

## Estado verificado en esta Mac

- Arquitectura: Apple Silicon (`arm64`).
- Python global: 3.14.0. Se conserva; no se instalarán paquetes de la materia ahí.
- Miniconda: instalado con Homebrew en `/opt/homebrew/Caskroom/miniconda/base`.
- Shell: `zsh`, ya inicializado mediante `conda init zsh`.
- VS Code: instalado, versión 1.101.2 para `arm64`.
- Extensiones: `ms-python.python` y `ms-toolsai.jupyter` ya instaladas.
- Pendiente: aceptar personalmente los términos de los canales oficiales de Anaconda y crear el entorno.

## 1. Terminar la configuración de Conda

Abre una terminal nueva. Si quieres continuar en la terminal actual, ejecuta:

```zsh
source ~/.zshrc
```

Comprueba Miniconda:

```zsh
conda --version
conda info --base
```

La primera creación del entorno quedó detenida porque los canales oficiales ahora solicitan aceptar sus términos. Lee los términos enlazados por Conda y, si estás de acuerdo, acepta personalmente ambos canales:

```zsh
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r
```

Después ejecuta los comandos solicitados por la materia:

```zsh
conda create --name mineria_datos python=3.10 -y
conda activate mineria_datos
conda install numpy pandas jupyter -y
```

Comprueba versiones e importaciones sin depender de VS Code:

```zsh
python --version
python -c 'import numpy, pandas; print("NumPy", numpy.__version__); print("pandas", pandas.__version__)'
conda env list
```

El resultado de `python --version` debe comenzar con `Python 3.10`, y `mineria_datos` debe aparecer con un asterisco en `conda env list`.

## 2. Preparar y abrir VS Code

Las extensiones Python y Jupyter ya están instaladas. Falta habilitar el comando `code` en la terminal:

1. Abre VS Code.
2. Presiona `Cmd+Shift+P`.
3. Ejecuta **Shell Command: Install 'code' command in PATH**.
4. Cierra y vuelve a abrir la terminal.

Desde este repositorio, abre la carpeta con:

```zsh
cd /Users/dtd/work/2-areas/uni/s7/data-mining
code .
```

Abre `test_entorno.ipynb`, pulsa **Select Kernel** y elige el entorno `mineria_datos` (puede mostrarse como `Python (mineria_datos)`). Ejecuta la celda con `Shift+Enter`.

Si el entorno no aparece en la lista de kernels, con el entorno activado ejecuta:

```zsh
python -m ipykernel install --user --name mineria_datos --display-name "Python (mineria_datos)"
```

## 3. Restablecer la apariencia de VS Code

Para restablecer solamente la distribución de ventanas, vistas y paneles, sin borrar extensiones ni otros ajustes:

1. Presiona `Cmd+Shift+P`.
2. Ejecuta **View: Reset View Locations**.
3. Si también faltan menús, ejecuta **View: Reset All Menus**.

Tu configuración global contiene personalizaciones adicionales: tema `Aroma`, Activity Bar oculta, Status Bar oculta, una sola pestaña, sidebar a la derecha, tema de iconos, barra de título nativa, colores y fuente personalizados. Para volver a los valores visuales predeterminados:

1. Abre Settings con `Cmd+,`.
2. Busca cada ajuste modificado.
3. En el engrane de cada ajuste, elige **Reset Setting**.

Los ajustes visuales principales que conviene restablecer son:

```text
workbench.colorTheme
workbench.activityBar.location
workbench.editor.showTabs
workbench.statusBar.visible
workbench.sideBar.location
workbench.iconTheme
window.customTitleBarVisibility
window.titleBarStyle
workbench.colorCustomizations
editor.fontFamily
editor.fontSize
editor.fontLigatures
```

No borres toda la carpeta de configuración de VS Code: eso también eliminaría preferencias no relacionadas y es innecesario para recuperar el diseño predeterminado.

## 4. Evidencia y Git

Cuando la celda se ejecute correctamente:

1. Guarda el notebook para conservar también la salida.
2. Captura el código, la salida numérica y el kernel `mineria_datos` visible.
3. Revisa y agrega los archivos al repositorio:

```zsh
git status
git add test_entorno.ipynb SETUP_MINICONDA_VSCODE.md .gitignore
git commit -m "Add data mining environment verification notebook"
```

Publica el commit en el remoto que corresponda a tu portafolio y entrega el enlace solicitado por la materia.
