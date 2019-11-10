# HSTS Parser

[![Build Status](https://thebeanogamer.visualstudio.com/HSTSparser/_apis/build/status/HSTSparser?branchName=master)](https://thebeanogamer.visualstudio.com/HSTSparser/_build/latest?definitionId=2&branchName=master) ![Publish Status](https://thebeanogamer.vsrm.visualstudio.com/_apis/public/Release/badge/f24623e9-719d-4c7f-b194-3be7917a22bf/1/1) ![Python 3.7.x](https://img.shields.io/badge/python-3.7.x-yellow.svg) 

HSTS Parser is a simple tool to parse Firefox and Chrome's HSTS databases into actually helpful forensic artifacts! You can read more about the research behind this tool and potential uses for it over on [my blog](https://blog.daniel-milnes.uk/hsts-for-forensics-you-can-run-but-you-cant)!

## Installation

Installing HSTS Parser is easy! Just run the below command to install the dependencies and you're good to go!

```shell
pip3 install -r requirements.txt
```

Alternatively, if you're using Windows, you can use the executables on the [releases page](https://github.com/thebeanogamer/hstsparser/releases/latest) to not need to install anything at all.

## Usage

All of the below documentation is written for the Python version rather than the standalone, but the commands are the same, just replacing `python3 hstsparser.py` with the name of the executable.

```shell
$ python3 hstsparser.py -h
usage: hstsparser.py [-h] [-w WORDLIST] (--firefox | --chrome) FILE

Process HSTS databases

positional arguments:
  FILE         The path to the database to be processed

optional arguments:
  -h, --help   show this help message and exit
  -w WORDLIST  The path to the database to be processed
  --firefox    Process a Firefox database
  --chrome     Process a Chrome database
```

### Examples
#### Firefox

```shell
python3 hstsparser.py --firefox SiteSecurityServiceState.txt
```

#### Chrome

```shell
python3 hstsparser.py --chrome TransportSecurity
```

#### Chrome with Wordlist

```shell
python3 hstsparser.py -w wordlist.txt --chrome TransportSecurity
```

## Screenshots

### Firefox

![](https://blog.daniel-milnes.uk/content/images/2019/11/image-3.png)

### Chrome with Wordlist

![](https://blog.daniel-milnes.uk/content/images/2019/11/image-4.png)

## Links

- [My Blog Post](https://blog.daniel-milnes.uk/hsts-for-forensics-you-can-run-but-you-cant)
- [MDN - HSTS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security)
- [Chromium - HSTS](https://www.chromium.org/sts)
