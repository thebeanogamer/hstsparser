#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2023 Daniel Milnes
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import csv
import datetime
import importlib.metadata
import json
import os
import re
import typing
from argparse import ArgumentParser, Namespace
from base64 import b64encode
from hashlib import sha256

from prettytable import PrettyTable


def convert_domain(domain: str) -> str:
    """Convert string to the Google Chrome domain format"""
    output = [chr(0)]
    idx = 0
    for char in reversed(domain):
        if char == ".":
            output.append(chr(idx))
            idx = 0
        else:
            output.append(char)
            idx += 1
    output.append(chr(idx))
    return b64encode(sha256("".join(reversed(output)).encode("utf-8")).digest())


def print_db(database: list, field_names: list) -> None:
    """Print the database in a formatted table"""
    table = PrettyTable()
    table.field_names = field_names
    for i in database:
        table.add_row(i)
    print(table)


def serial_date_to_string(srl_no: str) -> str:
    """Convert serial date object to printable string"""
    new_date = datetime.datetime.utcfromtimestamp(0) + datetime.timedelta(int(srl_no))
    return new_date.strftime("%Y-%m-%d")


def is_valid_file(parser: ArgumentParser, arg: str) -> typing.TextIO:
    """Check that file already exists"""
    if not os.path.exists(arg):
        parser.error(f"The file {arg} does not exist!")
    else:
        return open(arg, "r")


def file_already_exists(parser: ArgumentParser, arg: str) -> typing.TextIO:
    """Check that the file does not already exist"""
    if os.path.exists(arg):
        parser.error(f"The file {arg} already exists!")
    else:
        return open(arg, "w", newline="")


def print_if_no_args(args: Namespace, database: list, field_names: list) -> None:
    """Print database if no output file has been specified"""
    if not args.csv_file:
        print_db(database, field_names)
    else:
        file_write(args, database, field_names)


def file_write(args: Namespace, database: list, field_names: list) -> None:
    """Write to a CSV file"""
    if args.csv_file:
        with args.csv_file as csvfile:
            csvfile = csv.writer(csvfile)
            csvfile.writerow(field_names)
            for i in database:
                csvfile.writerow(i)


def date_round(date: datetime.datetime) -> datetime.datetime:
    """Round `datetime` object"""
    return date - datetime.timedelta(
        minutes=date.minute % 10, seconds=date.second, microseconds=date.microsecond
    )


def parse_chrome_record(data: dict, database: list, host: str, args: Namespace) -> None:
    if "expect_ct" not in data:
        if bool(data["sts_include_subdomains"]):
            subdomains = "Yes"
        else:
            subdomains = "No"
        record = [
            host,
            datetime.datetime.fromtimestamp(data["expiry"]),
            subdomains,
            datetime.datetime.fromtimestamp(data["sts_observed"]),
        ]
        if args.csv_file:
            record[1] = date_round(record[1])
            record[3] = date_round(record[3])
        database.append(record)


parser = ArgumentParser(prog="hstsparser", description="Process HSTS databases")
parser.add_argument(
    dest="database_file",
    help="The path to the database to be processed",
    metavar="FILE",
    type=lambda x: is_valid_file(parser, x),
)
parser.add_argument(
    "-w",
    dest="wordlist_file",
    help="The path to a file containing a wordlist for bruteforcing hashes",
    metavar="WORDLIST",
    type=lambda x: is_valid_file(parser, x),
)
parser.add_argument(
    "--csv",
    dest="csv_file",
    help="Output to a CSV file",
    metavar="CSV",
    type=lambda x: file_already_exists(parser, x),
)
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--firefox", action="store_true", help="Process a Firefox database")
group.add_argument("--chrome", action="store_true", help="Process a Chrome database")

try:
    __version__ = importlib.metadata.version("hstsparser")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.0.1"

parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")


def main() -> None:
    """Entry point for command line alias."""
    args = parser.parse_args()

    dirtydb = args.database_file.read()
    database = []

    if args.firefox:
        dirtydb = dirtydb.split("\n")
        for i in dirtydb:
            if i != "":
                record = re.split(r"\t+", i)
                record.append(record[0][-4:])
                record[0] = re.search(r"^([^:\^]+)", record[0]).group(0)
                record[2] = serial_date_to_string(record[2])
                cleaned = record[3].split(",")
                try:
                    record[3] = datetime.datetime.fromtimestamp(int(cleaned[0]) / 1000)
                except (OSError, ValueError):
                    record[3] = datetime.datetime.fromtimestamp(
                        32503680000
                    )  # 3000-01-01 00:00:00
                if int(cleaned[2]):
                    record.append("Yes")
                else:
                    record.append("No")
                if args.csv_file:
                    record[3] = date_round(record[3])
                database.append(record)
        print_if_no_args(
            args,
            database,
            ["URL", "Visits", "Last Accessed", "Expiry", "Type", "Include Subdomains"],
        )

    if args.chrome:
        dirtydb = json.loads(dirtydb)

        # v1 of this file did not specify a version number
        chrome_version: int = dirtydb.get("version", 1)

        match chrome_version:
            case 1:
                for i in dirtydb:
                    parse_chrome_record(dirtydb[i], database, i, args)
            case 2:
                for i in dirtydb.get("sts", []):
                    parse_chrome_record(i, database, i.get("host", ""), args)
            case _:
                print(
                    "Unrecognised Chrome file version. "
                    "Please raise an issue on https://github.com/thebeanogamer/hstsparser"
                )
                raise NotImplementedError

        if args.wordlist_file:
            wordlist = args.wordlist_file.read().splitlines()
            rainbow = []
            for i in wordlist:
                rainbow.append(convert_domain(i))
            for i in database:
                for j in range(0, len(rainbow)):
                    if i[0] == rainbow[j].decode("utf-8"):
                        i.append(wordlist[j])
                if len(i) == 4:
                    i.append("")
            print_if_no_args(
                args,
                database,
                [
                    "Base64 URL Hash",
                    "Expiry",
                    "Include Subdomains",
                    "Last Observed",
                    "Cracked Hash",
                ],
            )
        else:
            print_if_no_args(
                args,
                database,
                ["Base64 URL Hash", "Expiry", "Include Subdomains", "Last Observed"],
            )


if __name__ == "__main__":
    main()
