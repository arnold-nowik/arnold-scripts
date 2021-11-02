#!/usr/bin/env python3

import pandas
import openpyxl
import csv
import argparse
import sys
import datetime
from os import remove

### Function for converting Pandas DataFrame object to dictionary data

def convert_df_to_dict(df, temp_file):
# output data in CSV format
    df_csv = df.to_csv(index=False, header=False)
    with open(temp_file, 'w') as f:
        print(df_csv.upper(), file=f, end="")
# Convert CSV to a dictionary
    reader = csv.reader(open(temp_file))
    dictionary = {}
    for row in reader:
        key = row[0]
        dictionary[key] = row[1:]
    return dictionary

### Parse CLI arguments ###

parser = argparse.ArgumentParser()
parser.add_argument("invoice_xlsx", help="Invoice Excel file")
parser.add_argument("sms_project_xlsx", help="Project Excel file from Sales Management System")
parser.add_argument("-t", "--timesheet", help="Timesheet Excel file")
args = parser.parse_args()

### Read SMS data ###

smsDataFrame = pandas.read_excel(args.sms_project_xlsx, usecols=[2,5,8])

# Output Workload value as a float instead of percent, the same as on invoices
smsDataFrame['Workload (%)'] = smsDataFrame['Workload (%)'] / 100

# Create dictionary
sms_dict = convert_df_to_dict(smsDataFrame, './sms.csv') 

# Cleanup temp file
remove('./sms.csv')

# Convert dictionary values to floats
for key in sms_dict.keys():
    sms_dict[key] = [float(sms_dict[key][0]),float(sms_dict[key][1])]


### Read invoice data ###

# Default to last month invoice details sheet
thisMonth = datetime.date.today().replace(day=1)
lastMonth = thisMonth - datetime.timedelta(days=1)
sheetName = lastMonth.strftime("明細書_%Y%m")

wb = input(f"Name of Excel worksheet containing Invoice details (press 'Enter' for default {sheetName}: ") or sheetName  # excel workbook name
try:
    skip_rows = (int(input("First row number to read: ")) -1) or 12 # number of rows to skip
    nrows = (int(input("Last row number to read: ")) - skip_rows) # number of rows to read
except ValueError:
    print("Error - Row number must be an integer. Exiting...")
    sys.exit(1)

inv_name = input("Column for member name (Press 'Enter' for default C): ").upper() or "C"
inv_wload = input("Column for workload (Press 'Enter' for default F): ").upper() or "F"
inv_bill = input ("Column for Billing Price (Press 'Enter' for default H): ").upper() or "H"
cols = inv_name + ', ' + inv_wload + ', ' + inv_bill

try:
    invoiceDataFrame = pandas.read_excel(args.invoice_xlsx, sheet_name=wb, header=None, usecols=cols, skiprows=skip_rows, nrows=nrows).iloc[::2] # make sure to read only every 2nd row by specifying iloc[::2]
except ValueError as err:
    print(f"\nError - {err}\n")
    sys.exit(1)

# Calculate total workload amount for given data frame
index = 5
if inv_wload == "F":
    index = 5
elif inv_wload == "E":
    index = 4
else:
    index = (input("Column number for workload value: ") -1)

invoice_workload = invoiceDataFrame[index].sum()

# Confirm data range for processing
print("\nSMS data to process: ")
print(smsDataFrame)
print("\nInvoice data range to process: ")
print(invoiceDataFrame, end="\n\n")
confirm_range = input("Is this okay? Type 'yes' to continue:\n>> ").lower()
if confirm_range != "yes":
    print("Confirmation failure, exiting.")
    sys.exit(2)
else:
    print()

# Create dictionary
invoice_dict = convert_df_to_dict(invoiceDataFrame, './invoice.csv')

# Cleanup temp file
remove('./invoice.csv')

# Convert dictionary values to floats
for key in invoice_dict.keys():
    invoice_dict[key] = [float(invoice_dict[key][0]),float(invoice_dict[key][1])]

### Compare data and output result to stdout ###

headcount = 0
for key in invoice_dict.keys():
    print(key.upper())
    headcount += 1

print(f"\n稼働率と単価チェック\n＝＝＝＝＝＝＝＝＝＝\n請求書の頭数：{headcount}名")
print(f"合計稼働率　：{invoice_workload}人月\n")

for key in invoice_dict.keys():
    cmp_inv = invoice_dict[key]
    try:
        cmp_sms = sms_dict[key]
    except KeyError:
        print(f" - ERROR - {key.upper()}はSMSデータには見つかりませんでした。")
    if cmp_inv == cmp_sms:
        print(f" - {key.upper()} - OK. 稼働率も単価も一致しています: {cmp_inv}.")
    else:
        print(f" - {key.upper()} - NG. 稼働率または単価が異なっています.\n>> Invoice: {cmp_inv}\n>> SMS:     {cmp_sms}.\n")


### Check Worktime Data ###

if args.timesheet:

#Set invoice worktime data source
    inv_worktime = input("\nColumn for worktime value (Press 'Enter' for default D): ").upper() or "D"
    cols_wt = inv_name + ', ' + inv_worktime

    invoiceDataFrameWT = pandas.read_excel(args.invoice_xlsx, sheet_name=wb, header=None, usecols=cols_wt, skiprows=skip_rows, nrows=nrows).iloc[::2]

    print(invoiceDataFrameWT)

# Create dictionary
    invoice_wt_dict = convert_df_to_dict(invoiceDataFrameWT, './invoice_wt.csv')

# Cleanup temp file
    remove('./invoice_wt.csv')

# Convert Worktime value to float
    for key in invoice_wt_dict.keys():
        invoice_wt_dict[key] = float(invoice_wt_dict[key][0])

# Read Timesheet Data
    try:
        input_name_cell = input("\nTimesheet cell containing member name (Press 'Enter' for default I7): ").upper() or "I7"
        input_worktime_cell = input("Timesheet cell containing total worktime: ").upper()
    except ValueError:
        print("Wrong input, exiting...")

    workbook = openpyxl.load_workbook(filename=args.timesheet, data_only=True)
    timesheet_dict = {}
    try:
        for sheet_name in workbook.sheetnames:
            sheet = workbook[sheet_name]
            name_cell = sheet[input_name_cell]
            worktime_cell = sheet[input_worktime_cell]
            print(f"{name_cell.value} = {worktime_cell.value}")
            timesheet_dict[str(name_cell.value)] = float(str(worktime_cell.value))
    except ValueError:
        pass
    print("\n稼働時間チェック\n＝＝＝＝＝＝＝＝")

# Compare Invoice worktime data with Timesheet data
    for key in invoice_wt_dict.keys():
        cmp_inv_wt = invoice_wt_dict[key]
        try:
            cmp_timesheet = timesheet_dict[key]
        except KeyError:
            print(f" - ERROR - {key.upper()}はタイムシートには見つかりませんでした。")
        if cmp_inv_wt == cmp_timesheet:
            print(f" - {key.upper()} - OK. 稼働時間が一致しています: {cmp_inv_wt}.")
        else:
            print(f" - {key.upper()} - NG. 稼働時間が異なっています.\n>> Invoice:  {cmp_inv_wt}\n>> Timesheet: {cmp_timesheet}.\n")
