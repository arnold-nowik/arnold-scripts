#!/usr/bin/env python3

import pandas
import sys
import argparse

### Argument parser ###

parser = argparse.ArgumentParser()
parser.add_argument("tribes", help="Tribes classification output file")
parser.add_argument("follower_list", help="Follower List Excel file")
args = parser.parse_args()

try:
    tribeno = (int(input("Number of tribes: ")) + 1)
except (TypeError, ValueError) as err:
    print("Value must be an integer")
    sys.exit(1)

tribeDf = pandas.read_excel(args.tribes, sheet_name=None)
followersDf = pandas.read_excel(args.follower_list)
writer = pandas.ExcelWriter("./finalOutput.xlsx")
merge = {}
for df in range(1,tribeno):
    merge[f"{df}"] = pandas.merge(tribeDf[f"{df}"],followersDf,how="left", on="サンプルアカウント")
    for key in merge:
        merge[key].to_excel(writer, key, index=False)
writer.save()
