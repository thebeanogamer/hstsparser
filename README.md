# HSTS Parser

[![Lint Codebase](https://github.com/thebeanogamer/hstsparser/actions/workflows/lint.yaml/badge.svg)](https://github.com/thebeanogamer/hstsparser/actions/workflows/lint.yaml) [![Build Releases](https://github.com/thebeanogamer/hstsparser/actions/workflows/build.yaml/badge.svg)](https://github.com/thebeanogamer/hstsparser/actions/workflows/build.yaml) [![Licence](https://img.shields.io/github/license/thebeanogamer/hstsparser)](./LICENSE) ![Python 3.11.x](https://img.shields.io/badge/python-3.11.x-yellow.svg) [![PyPI](https://img.shields.io/pypi/v/hstsparser)](https://pypi.org/project/hstsparser) [![Downloads](https://pepy.tech/badge/hstsparser)](https://pepy.tech/project/hstsparser) [![Copr build status](https://copr.fedorainfracloud.org/coprs/thebeanogamer/hstsparser/package/hstsparser/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/thebeanogamer/hstsparser/package/hstsparser/)

HSTS Parser is a simple tool to parse Firefox and Chrome's HSTS databases into actually helpful forensic artifacts! You can read more about the research behind this tool and potential uses for it over on [my blog](https://blog.daniel-milnes.uk/hsts-for-forensics-you-can-run-but-you-cant)!

## Installation

HSTS Parser can be installed via pip, or as a native executable.

### From PyPi

If you already have Python installed, you can install HSTS Parser using pip.

```bash
pip install hstsparser
```

### On Fedora

[![Fedora package](https://img.shields.io/fedora/v/hstsparser/f38?label=Fedora%2038&link=https%3A%2F%2Fpackages.fedoraproject.org%2Fpkgs%2Fhstsparser%2Fhstsparser%2F)](https://packages.fedoraproject.org/pkgs/hstsparser/hstsparser/) [![Fedora package](https://img.shields.io/fedora/v/hstsparser/rawhide?label=Fedora%20Rawhide&link=https%3A%2F%2Fpackages.fedoraproject.org%2Fpkgs%2Fhstsparser%2Fhstsparser%2F)](<https://packages.fedoraproject.org/pkgs/hstsparser/hstsparser/>)

HSTS Parser is available for Fedora 38+.

```bash
dnf install hstsparser
```

### On Windows

Windows binaries are published by GitHub Actions CI for each release of HSTS Parser. You can download these on the [releases page](https://github.com/thebeanogamer/hstsparser/releases/latest).

## Usage

All of the below documentation is written for the Python version rather than the standalone executable, but the commands will be the same.

```shell
$ hstsparser -h
usage: hstsparser [-h] [-w WORDLIST] [--csv CSV] (--firefox | --chrome) FILE

Process HSTS databases

positional arguments:
  FILE         The path to the database to be processed

optional arguments:
  -h, --help   show this help message and exit
  -w WORDLIST  The path to a file containing a wordlist for bruteforcing hashes
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
- [Chromium - HSTS](https://www.chromium.org/hsts)
