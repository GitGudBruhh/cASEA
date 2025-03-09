# cASEA
Compilers Course Project - IITDh Spring 24-25

# Setup
1. Create a virtual environment and use it for the project.
```
python -m venv .venv
source .venv/bin/activate
```

2. Run the following command to install `sphinx` and other documentation tools
```
pip install -r requirements.txt
```

# What are RST Files?

**RST (reStructuredText)** is a lightweight markup language used for writing documentation, particularly in Python projects. It is commonly associated with Sphinx, a documentation generator.

## Key Features

- **Human-Readable**: Easy to read and write in plain text.
- **Structured Formatting**: Supports headings, lists, links, images, and code blocks.
- **Integration with Sphinx**: The default format for Sphinx, allowing automatic documentation generation from code docstrings.

## Example Syntax
```
Title
=====

This is a paragraph with **bold text** and *italic text*.

- Item 1
- Item 2

.. code-block:: python

   def hello_world():
       print("Hello, World!")
```

# Documentation Build Instructions
1. Run the following commant from the root of the directory. This reads docstrings from python modules in `src/` to autogenerate `.rst` files in the `doc_src/` directory.
```
sphinx-apidoc -o ./doc_src/ ./doc_src/../src
```

2. Run the following to build the HTML documentation (LaTeX and PDF are also supported)
```
make html --file=Makefile-doc
```