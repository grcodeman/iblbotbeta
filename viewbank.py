import gspread

gc = gspread.service_account(filename="sheets-test-343522-8a764f8b82da.json")

sh = gc.open_by_key("1kMjNXd9vgc4BybQYhByucby4TIi6_QuWXMZ951ms3f0")

def grab_teamac(team):
    ws = sh.worksheet('Bank')
    string = ""
    try:
        # locates the team cell and starts the string
        c = ws.find(team)
        string += "**" + team + " AC:**\n"

        # loops through team list
        for i in range(5):
            string += ws.cell(c.row + i, 2).value
            string += " = "
            string += ws.cell(c.row + i, 29).value
            string += "\n"
    except:
        string = "Process Failed"
    return string

def grab_teambal(team):
    ws = sh.worksheet('Bank')
    string = ""
    try:
        # locates the team cell and starts the string
        c = ws.find(team)
        string += "**" + team + " Bal:**\n"

        # loops through team list
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
        # locates the player cell and pulls their xp value
        c = ws.find(player)
        string += player + ": **" + ws.cell(c.row, 4).value + "XP**"
    except:
        string = "Process Failed"
    return string

def grab_claims(week, player):
    ws = sh.worksheet('Claim View')
    string = ""
    amt_approved = 0
    amt_denied = 0
    amt_pending = 0

    # finds all matching cells for the player and period combination
    c = ws.findall(player + "-" + week)
    string += "__**" + player + " " + week + " claims**__" + "\n"

    # loops through the claims list
    for i in c:
        # displays the information
        string += "Time: __" + str(ws.cell(i.row, 1).value) + "__ "
        string += "Cat: __" + str(ws.cell(i.row, 4).value) + "__ "
        amount = str(ws.cell(i.row, 5).value)
        string += "Amount: __" + amount + "XP__ "
        string += "Desc: __" + str(ws.cell(i.row, 6).value) + "__ "
        string += "\n"

        # displays the status
        status = str(ws.cell(i.row, 7).value)
        if (status == "Yes"):
            string += "🟢 " + amount + "XP **Approved** by " + str(ws.cell(i.row, 8).value)
            amt_approved += int(amount)
        elif (status == "No"):
            string += "🔴 " + amount + "XP **Denied** by " + str(ws.cell(i.row, 8).value) + " Reason: " + str(ws.cell(i.row, 9).value)
            amt_denied += int(amount)
        else:
            string += "🟡 " + amount + "XP **Pending**"
            amt_pending += int(amount)
        string += "\n"
    
    # displays the summary
    string += "**Summary:**\n" + "🟢 " + str(amt_approved) + "XP 🔴" + str(amt_denied) + "XP 🟡" + str(amt_pending) + "XP"

    return string
