# Python bindings for the Durham University (UK) Directory

This package provides basic python bindings for [the Durham University
Directory](https://dur.ac.uk/directory/password), where Durham University
students and staff can look up fellow students and staff.

It is nothing more than a wrapper around `requests` and `bs4`, and absolutely
nothing clever is being done (although I do think the code is pleasantly
simple), and absolutely nothing clever is being done (although I do think the
code is pleasantly simple).

## Installation

```bash
python -m pip install durham-directory
```

## CLI Usage

```bash
durham-directory --help
durham-directory --oname John --surname Morris
```

## API Usage

```python
from durham_directory import Query
query = Query(username="me") # will prompt for password when evaluated
query(oname="John", surname="Morris", type_="any")
```
