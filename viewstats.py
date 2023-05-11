import gspread

import random
from re import A
import pandas as pd
import math

gc = gspread.service_account(filename="sheets-test-343522-8a764f8b82da.json")

sh = gc.open_by_key("1Kah3LT9dlDBFP71Y2GNAq8a2RbJjgiVHFTyGOeEnyLg")

avgkey = ['Season','Team','Name','PTS','REB','oReb','AST','STL','BLK','TO','PF','PRF','Dunks','FGM','FGA','FG%','3PM','3PA','3P%','FTM','FTA','FT%','GP','Pos','Level']

# grabs the live stats
def grab_stats(season,player):
    string = ""
    ws = sh.worksheet("view")
    try:
        # locates cell of season and player combination
        c = ws.find(str(season) + "-" + player)

        # loops through the values and attaches them to the string
        for i in range(len(avgkey)):
            if i > 0:
                string += ", "
            string += avgkey[i] + ": "
            string += str(ws.cell(c.row, i+2).value)
    except:
        string = "Process Failed"
    return string

filename = 'statexport.csv'
df = pd.read_csv(filename)

# grabs the cached stats
def cached_stats(season,player):
    string = ""
    try:
        # locates the row
        tag = str(season) + "-" + player
        row = df[df['Tag'] == tag].index[0]

        # loops through and attaches the values to the string
        for i in range(len(avgkey)):
            if i > 0:
                string += ", "
            string += avgkey[i] + ": "
            string += str(df.iloc[row,i+1])
    except:
        string = "Process Failed"
    return string