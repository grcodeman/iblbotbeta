import gspread

gc = gspread.service_account(filename="sheets-test-343522-8a764f8b82da.json")

sh = gc.open_by_key("1Kah3LT9dlDBFP71Y2GNAq8a2RbJjgiVHFTyGOeEnyLg").worksheet('view')

key = ['Season','Team','Name','PTS','REB','oReb','AST','STL','BLK','TO','PF','PRF','Dunks','FGM','FGA','FG%','3PM','3PA','3P%','FTM','FTA','FT%','GP','Pos','Level']

def grab_stats(season,player):
    string = ""
    try:
        c = sh.find(str(season) + "-" + player)
        for i in range(len(key)):
            if i > 0:
                string += ", "
            string += key[i] + ": "
            string += str(sh.cell(c.row, i+2).value)
    except:
        string = "Process Failed"
    return string