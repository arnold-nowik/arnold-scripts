#!/usr/bin/env python3
import pandas
import datetime
import argparse

### Argument parser ###

parser = argparse.ArgumentParser()
parser.add_argument("input_data", help="Input Power User Excel file")
parser.add_argument("cluster_output", help="Data Clustering output csv file")
args = parser.parse_args()

### Read data ###

dfInput = pandas.read_excel(args.input_data)
dfCluster = pandas.read_csv(args.cluster_output)

### Output data clustering result in 1 Excel file ###
    
date = datetime.date.today().strftime("%Y-%m-%d")

result = pandas.merge(dfCluster.iloc[:,:3], dfInput, how="left", on="内部ID")
result.to_excel(f"./DataClustering-Result_{date}.xlsx", index=False)

### Output data for every cluster in Excel format

clusterGroup = result.groupby('クラスタNO')
for c in clusterGroup.groups:
    path = 'Cluster' + str(int(c)) + '.xlsx'
    clusterGroup.get_group(c).to_excel(path, index=False)
