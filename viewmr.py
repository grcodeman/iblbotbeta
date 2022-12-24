import gspread

gc = gspread.service_account(filename="sheets-test-343522-8a764f8b82da.json")

sh = gc.open_by_key("1PvgXlpFieLPh-xiwBxLkpiCjeXtvwdplpnj_M5oKcWo")

# team assets contracts

# team assets picks

# grab player mr value
def grab_mr(player, num):
    ws = sh.worksheet('MR Data 2K23')
    string = ""
    try:
        c = ws.find(player)
        name = ws.cell(1, int(num)).value
        value = ws.cell(c.row, int(num)).value
        if (value == None):
            value = "`Empty`"
        string += player + " - " + name + ": **" + value + "**"
    except:
        string = "Process Failed"
    return string

def find_row(value):
    ws = sh.worksheet('MR Data 2K23')
    string = ""
    try:
        c = ws.find(value)
        string = str(c.col)
    except:
        string = "1"
    return string