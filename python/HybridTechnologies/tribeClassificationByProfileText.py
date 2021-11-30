#!/usr/bin/env python3

import pandas
import sys
import argparse

### Argument parser ###

parser = argparse.ArgumentParser()
parser.add_argument("user_list", help="Input Power User Excel file")
parser.add_argument("kwds", help="Keyword list")
args = parser.parse_args()

try:
    tribes = (int(input("Number of tribes: ")) + 1)
except (TypeError, ValueError) as err:
    print("Value must be an integer")
    sys.exit(1)

input = pandas.read_excel(args.user_list)
kwds = pandas.read_excel(args.kwds)

kwd = {}
for i in range(1,tribes):
    kwd[f"{i}"] = '|'.join(kwds[i].dropna().tolist())
result = {}
for i in range(1,tribes):
    result[f"{i}"] = input.プロフィール.str.contains(kwd[f"{i}"])
pandas.DataFrame.from_dict(result).to_csv(path_or_buf=f"./result.csv",  index=False)
