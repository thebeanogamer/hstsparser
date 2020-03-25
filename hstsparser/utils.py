"""Utilities for reading and parsing HSTS databases."""

import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterator, TextIO, Union


class HSTSReader:
    """Implements a HSTS database reader."""

    def __init__(self, file: Union[str, Path], browser: str) -> None:
        """Initialise attributes."""
        if type(file) is str:
            file = Path(file).expanduser()
        self.file = file
        self.browser = browser

    @staticmethod
    def chrome(file: TextIO) -> Iterator:
        """Read a chrome database."""
        ...

    @staticmethod
    def firefox(file: TextIO) -> Iterator:
        """Read a firefox database."""
        pattern = re.compile(r'\s+|:|,')
        for line in file:
            record = pattern.split(line)
            domain, htype, visits, access, expires, _, subdomains, *_ = record
            expiry = int(expires) / 1000 if expires.isnumeric() else 32503680000
            yield [
                domain.split('^')[0],
                int(visits),
                datetime.utcfromtimestamp(0) + timedelta(int(access)),
                datetime.fromtimestamp(expiry),
                htype,
                'No' if subdomains == '0' else 'Yes'
            ]

    def __iter__(self) -> Iterator:
        """Return the relevant iterator."""
        with self.file.open() as file:
            if self.browser == 'firefox':
                yield from self.firefox(file)
            elif self.browser == 'chrome':
                yield from self.chrome(file)
            else:
                raise Exception
