import datetime
import json
import os
import re
from argparse import ArgumentParser
from base64 import b64encode
from hashlib import sha256

from prettytable import PrettyTable


def convert(domain):
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


def printDB(database, field_names):
    table = PrettyTable()
    table.field_names = field_names
    for i in database:
        table.add_row(i)
    print(table)


def serial_date_to_string(srl_no):
    new_date = datetime.datetime.utcfromtimestamp(0) + datetime.timedelta(int(srl_no))
    return new_date.strftime("%Y-%m-%d")


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error(f"The file {arg} does not exist!")
    else:
        return open(arg, "r")


parser = ArgumentParser(description="Process HSTS databases")
parser.add_argument(
    dest="database_file",
    help="The path to the database to be processed",
    metavar="FILE",
    type=lambda x: is_valid_file(parser, x),
)
parser.add_argument(
    "-w",
    dest="wordlist_file",
    help="The path to the database to be processed",
    metavar="WORDLIST",
    type=lambda x: is_valid_file(parser, x),
)
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--firefox", action="store_true", help="Process a Firefox database")
group.add_argument("--chrome", action="store_true", help="Process a Chrome database")

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
            record[3] = datetime.datetime.fromtimestamp(int(cleaned[0]) / 1000)
            if int(cleaned[2]):
                record.append("Yes")
            else:
                record.append("No")
            database.append(record)
    printDB(
        database,
        ["URL", "Visits", "Last Accessed", "Expiry", "Type", "Include Subdomains"],
    )

if args.chrome:
    dirtydb = json.loads(dirtydb)
    for i in dirtydb:
        current = dirtydb[i]
        if "expect_ct" not in current:
            if bool(current["sts_include_subdomains"]):
                subdomains = "Yes"
            else:
                subdomains = "No"
            database.append(
                [
                    i,
                    datetime.datetime.fromtimestamp(current["expiry"]),
                    subdomains,
                    datetime.datetime.fromtimestamp(current["sts_observed"]),
                ]
            )
    if args.wordlist_file:
        wordlist = args.wordlist_file.read().splitlines()
        rainbow = []
        for i in wordlist:
            rainbow.append(convert(i))
        for i in database:
            for j in range(0, len(rainbow)):
                if i[0] == rainbow[j].decode("utf-8"):
                    i.append(wordlist[j])
            if len(i) == 4:
                i.append("")
        printDB(
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
        printDB(
            database,
            ["Base64 URL Hash", "Expiry", "Include Subdomains", "Last Observed"],
        )
