# Release Procedure
This guide aims to help how to release a new version of the package.

## Tests
To execute all test from a folder use:
```shell
python -m unitest discover tests/
```

## Setup
Ensure you have general installed ***build***
```shell
python3 -m build
```
And ***twine*** to publish a new version
```shell
python3 -m twine
```
Create a ***.pypirc*** file in your home with account creadentials
```editorconfig
[testpyi]
username = __token__
password = <pypi-token>
```
Password hold your generated token from account page.  

Eventually edit ***pyproject.toml*** file with a new version

## Build and publish
To build the package use:
```shell
python3 -m build
```
Then publish the package:
```shell
python3 -m twine upload --repository testpypi dist/*
```