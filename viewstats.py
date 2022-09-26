import gspread

gc = gspread.service_account(filename="sheets-test-343522-8a764f8b82da.json")

sh = gc.open_by_key("1Kah3LT9dlDBFP71Y2GNAq8a2RbJjgiVHFTyGOeEnyLg")

avgkey = ['Season','Team','Name','PTS','REB','oReb','AST','STL','BLK','TO','PF','PRF','Dunks','FGM','FGA','FG%','3PM','3PA','3P%','FTM','FTA','FT%','GP','Pos','Level']

def grab_stats(season,player):
    string = ""
    ws = sh.worksheet("view")
    try:
        c = ws.find(str(season) + "-" + player)
        for i in range(len(avgkey)):
            if i > 0:
                string += ", "
            string += avgkey[i] + ": "
            string += str(ws.cell(c.row, i+2).value)
    except:
        string = "Process Failed"
    return string