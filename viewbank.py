import gspread

gc = gspread.service_account(filename="sheets-test-343522-8a764f8b82da.json")

sh = gc.open_by_key("1L9FGQs9Hv59XGVvewKRRo-7MalPo_QUr5-Tl2eghw9Q").worksheet('Bank')

def grab_teamac(team):
    string = ""
    try:
        c = sh.find(team)
        string += "**" + team + " AC:**\n"
        for i in range(5):
            string += sh.cell(c.row + i, 2).value
            string += " = "
            string += sh.cell(c.row + i, 24).value
            string += "\n"
    except:
        string = "Process Failed"
    return string

def grab_teambal(team):
    string = ""
    try:
        c = sh.find(team)
        string += "**" + team + " Bal:**\n"
        for i in range(5):
            string += sh.cell(c.row + i, 2).value
            string += " = "
            string += sh.cell(c.row + i, 4).value
            string += "XP\n"
    except:
        string = "Process Failed"
    return string

def grab_bal(player):
    string = ""
    try:
        c = sh.find(player)
        string += player + ": **" + sh.cell(c.row, 4).value + "XP**"
    except:
        string = "Process Failed"
    return string
