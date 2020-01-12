# HSTS Parser

[![Build Status](https://dev.azure.com/thebeanogamer/HSTSparser/_apis/build/status/Lint%20Pipeline?branchName=master)](https://dev.azure.com/thebeanogamer/HSTSparser/_build/latest?definitionId=2&branchName=master) [![Release Status](https://dev.azure.com/thebeanogamer/HSTSparser/_apis/build/status/Release%20Pipeline?branchName=master)](https://dev.azure.com/thebeanogamer/HSTSparser/_build/latest?definitionId=7&branchName=master) ![Licence](https://img.shields.io/github/license/thebeanogamer/hstsparser) ![Python 3.8.x](https://img.shields.io/badge/python-3.8.x-yellow.svg)

HSTS Parser is a simple tool to parse Firefox and Chrome's HSTS databases into actually helpful forensic artifacts! You can read more about the research behind this tool and potential uses for it over on [my blog](https://blog.daniel-milnes.uk/hsts-for-forensics-you-can-run-but-you-cant)!

## Installation

Installing HSTS Parser is easy! Just run the below commands to install everything you need!

### Linux

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
poetry install
```

### Windows

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
poetry install
```

Alternatively, if you're using Windows, you can use the executables on the [releases page](https://github.com/thebeanogamer/hstsparser/releases/latest) to not need to install anything at all.

## Usage

All of the below documentation is written for the Python version rather than the standalone, but the commands are the same, just replacing `python3 hstsparser.py` with the name of the executable.

```shell
$ poetry run python hstsparser.py -h
usage: hstsparser.py [-h] [-w WORDLIST] (--firefox | --chrome) FILE

Process HSTS databases

positional arguments:
  FILE         The path to the database to be processed

optional arguments:
  -h, --help   show this help message and exit
  -w WORDLIST  The path to the database to be processed
  --csv CSV    Output to a CSV file
  --firefox    Process a Firefox database
  --chrome     Process a Chrome database
```

### Examples

#### Firefox

```shell
poetry run python hstsparser.py --firefox SiteSecurityServiceState.txt
```

#### Chrome

```shell
poetry run python hstsparser.py --chrome TransportSecurity
```

#### Chrome with Wordlist

```shell
poetry run python hstsparser.py -w wordlist.txt --chrome TransportSecurity
```

## Screenshots

### Firefox

![Screenshot of Firefox Processing](https://blog.daniel-milnes.uk/content/images/2019/11/image-3.png)

### Chrome with Wordlist

![Screenshot of Chrome Processing with a wordlist](https://blog.daniel-milnes.uk/content/images/2019/11/image-4.png)

## Links

- [My Blog Post](https://blog.daniel-milnes.uk/hsts-for-forensics-you-can-run-but-you-cant)
- [MDN - HSTS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security)
- [Chromium - HSTS](https://www.chromium.org/sts)
