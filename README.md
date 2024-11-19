# AI Group Project

Some instructions here to help you guys get started.

Setup the frontend server with:

```
cd frontend
npm install
```

Run the frontend server with:

```
npm run dev
```

# Backend Installation and Environment Setup

Clone the repo to your local machine

```
git clone git@github.com:PraveenKusuluri08/npm_visual.git
```

## Install Python

You need python 3.12.5 I strongly recommend using pyenv to manage python versions. First install pyenv on your system. Follow instructions here. Be sure to update the path and install all packages pyenv depends on.
https://github.com/pyenv/pyenv

Install Python 3.12.5

```
pyenv install 3.12.5
```

## Install pipx

Install pipx via instructions here
https://pipx.pypa.io/stable/installation/
be sure to update path info. (this is how I installed on linux, Mac may be slightly different)

```
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc
```

ONLY DO THIS IF YOU HAVE TROUBLE. (you should not need to)
I had to install python3.8-venv on my machine to install poetry (this was before installing 3.12.5, maybe it will be different for you)

```
pip install pipx
sudo apt install python3.8-venv
```

## Install Poetry

Install poetry globally. Know that you may need to use the --force option

```
pipx install poetry
pipx upgrade poetry
```

Make sure poetry is installed

```
poetry --version
```

The version should not matter. Newer versions are usually better
My version is 1.8.3 installed using Python 3.8.10
Poetry requires a python version ^=3.8 to install. but the Python version can be different.

# Using Poetry

Once you got Poetry installed, navigate to this directory and run

```
poetry install
```

If poetry ever freezes during installs. you might be seeing the following [https://github.com/python-poetry/poetry/pull/6471](error). If this happens, run:

```
export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring
poetry install
```

# Running Development Server

```
poetry run flask run
```
