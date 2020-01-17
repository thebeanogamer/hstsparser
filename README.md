# HSTS Parser

[![Build Status](https://dev.azure.com/thebeanogamer/HSTSparser/_apis/build/status/Lint%20Pipeline?branchName=master)](https://dev.azure.com/thebeanogamer/HSTSparser/_build/latest?definitionId=2&branchName=master) [![Release Status](https://dev.azure.com/thebeanogamer/HSTSparser/_apis/build/status/Release%20Pipeline?branchName=master)](https://dev.azure.com/thebeanogamer/HSTSparser/_build/latest?definitionId=7&branchName=master) ![Licence](https://img.shields.io/github/license/thebeanogamer/hstsparser) ![Python 3.8.x](https://img.shields.io/badge/python-3.8.x-yellow.svg) ![PyPI](https://img.shields.io/pypi/v/hstsparser)

HSTS Parser is a simple tool to parse Firefox and Chrome's HSTS databases into actually helpful forensic artifacts! You can read more about the research behind this tool and potential uses for it over on [my blog](https://blog.daniel-milnes.uk/hsts-for-forensics-you-can-run-but-you-cant)!

## Installation

HSTS Parser can be installed via pip, or with [Poetry](https://python-poetry.org/).

### From PyPi
```bash
pip install hstsparser
```

### Poetry (Linux)
```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
poetry install --no-dev
```

### Poetry (Windows)
```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
poetry install --no-dev
```

Alternatively, if you're using Windows, you can use the executables on the [releases page](https://github.com/thebeanogamer/hstsparser/releases/latest) to not need to install anything at all.

## Usage

```shell
$ hstsparser -h
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
hstsparser --firefox SiteSecurityServiceState.txt
```

#### Chrome

```shell
hstsparser --chrome TransportSecurity
```

#### Chrome with Wordlist

```shell
hstsparser -w wordlist.txt --chrome TransportSecurity
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
