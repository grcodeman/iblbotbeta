import gspread

gc = gspread.service_account(filename="sheets-test-343522-8a764f8b82da.json")

sh = gc.open_by_key("1L9FGQs9Hv59XGVvewKRRo-7MalPo_QUr5-Tl2eghw9Q")

def grab_teamac(team):
    ws = sh.worksheet('Bank')
    string = ""
    try:
        c = ws.find(team)
        string += "**" + team + " AC:**\n"
        for i in range(5):
            string += ws.cell(c.row + i, 2).value
            string += " = "
            string += ws.cell(c.row + i, 24).value
            string += "\n"
    except:
        string = "Process Failed"
    return string

def grab_teambal(team):
    ws = sh.worksheet('Bank')
    string = ""
    try:
        c = ws.find(team)
        string += "**" + team + " Bal:**\n"
        for i in range(5):
            string += ws.cell(c.row + i, 2).value
            string += " = "
            string += ws.cell(c.row + i, 4).value
            string += "XP\n"
    except:
        string = "Process Failed"
    return string

def grab_bal(player):
    ws = sh.worksheet('Bank')
    string = ""
    try:
        c = ws.find(player)
        string += player + ": **" + ws.cell(c.row, 4).value + "XP**"
    except:
        string = "Process Failed"
    return string

def grab_claims(week, player):
    ws = sh.worksheet('XP Claims')
    string = ""

    c = ws.findall(player + "-" + week)
    string += "__**" + player + " " + week + " claims**__" + "\n"
    for i in c:
        string += "Time: __" + str(ws.cell(i.row, 1).value) + "__ "
        string += "Cat: __" + str(ws.cell(i.row, 4).value) + "__ "
        amount = str(ws.cell(i.row, 5).value)
        string += "Amount: __" + amount + "XP__ "
        string += "Desc: __" + str(ws.cell(i.row, 6).value) + "__ "
        string += "\n"
        status = str(ws.cell(i.row, 7).value)
        if (status == "Yes"):
            string += amount + "XP **Approved** by " + str(ws.cell(i.row, 8).value)
        elif (status == "No"):
            string += amount + "XP **Denied** by " + str(ws.cell(i.row, 8).value) + " Reason: " + str(ws.cell(i.row, 9).value)
        else:
            string += amount + "XP **Pending**"
        string += "\n"

    return string

print(grab_claims("Week 2", "M. Fairway"))