#!/usr/bin/env python3

import os
import pandas as pd
cwd = os.path.abspath('')
files = os.listdir(cwd)

df = pd.DataFrame()
for file in files:
    if file.endswith('.xlsx'):
        df = df.append(pd.read_excel(file), ignore_index=True)
df.to_excel('followers.xlsx', index=False)
