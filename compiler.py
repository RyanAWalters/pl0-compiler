import sys

norw = 22  # number of reserved words
txmax = 100  # length of identifier table
nmax = 14  # max number of digits in number
al = 10  # length of identifiers

a = []
chars = []
rword = []
table = []

global infile, outfile, ch, sym, id, num, linlen, kk, line, errorFlag, linelen


class tableValue():
    def __init__(self, name, kind):
        self.name = name
        self.kind = kind


def error(num):
    global errorFlag;
    errorFlag = 1

    print
    if num == 1:
        print >> outfile, "Use = instead of :="
    elif num == 2:
        print >> outfile, "= must be followed by a number."
    elif num == 3:
        print >> outfile, "Identifier must be followed by ="
    elif num == 4:
        print >> outfile, "Const, Var, Procedure must be followed by an identifier."
    elif num == 5:
        print >> outfile, "Semicolon or comma missing"
    elif num == 6:
        print >> outfile, "Incorrect symbol after procedure declaration."
    elif num == 7:
        print >> outfile, "Statement expected."
    elif num == 8:
        print >> outfile, "Incorrect symbol after statement part in block."
    elif num == 9:
        print >> outfile, "Period expected."
    elif num == 10:
        print >> outfile, "Semicolon between statements is missing."
    elif num == 11:
        print >> outfile, "Undeclared identifier"
    elif num == 12:
        print >> outfile, "Assignment to a constant or procedure is not allowed."
    elif num == 13:
        print >> outfile, "Assignment operator := expected."
    elif num == 14:
        print >> outfile, "call must be followed by an identifier"
    elif num == 15:
        print >> outfile, "Call of a constant or a variable is meaningless."
    elif num == 16:
        print >> outfile, "Then expected"
    elif num == 17:
        print >> outfile, "Semicolon or end expected. "
    elif num == 18:
        print >> outfile, "DO expected"
    elif num == 19:
        print >> outfile, "Incorrect symbol following statement"
    elif num == 20:
        print >> outfile, "Relational operator expected."
    elif num == 21:
        print >> outfile, "Expression must not contain a procedure identifier"
    elif num == 22:
        print >> outfile, "Right parenthesis missing"
    elif num == 23:
        print >> outfile, "The preceding factor cannot be followed by this symbol."
    elif num == 24:
        print >> outfile, "An expression cannot begin with this symbol."
    elif num == 25:
        print >> outfile, "Constant or Number is expected."
    elif num == 26:
        print >> outfile, "This number is too large."
    elif num == 27:
        print >> outfile, "Left parenthesis missing"
    elif num == 28:
        print >> outfile, "UNTIL expected"
    elif num == 29:
        print >> outfile, "Identifier expected"
    elif num == 30:
        print >> outfile, "Identifier must be a variable"
    elif num == 31:
        print >> outfile, "TO or DOWNTO expected"
    elif num == 32:
        print >> outfile, "OF expected"
    elif num == 33:
        print >> outfile, "colon expected"
    elif num == 34:
        print >> outfile, "CEND expected"
    exit(0)


def getch():
    global whichChar, ch, linelen, line;
    if whichChar == linelen:  # if at end of line
        whichChar = 0
        line = infile.readline()  # get next line
        linelen = len(line)
        sys.stdout.write(line)
    if linelen != 0:
        ch = line[whichChar]
        whichChar += 1
    return ch


def getsym():
    global charcnt, ch, al, a, norw, rword, sym, nmax, id
    while ch == " " or ch == "\n" or ch == "\r":
        getch()
    a = []
    if ch.isalpha():
        k = 0
        while True:
            a.append(ch)
            getch()
            if not ch.isalnum():
                break
        id = "".join(a)
        flag = 0
        for i in range(0, norw):
            if rword[i] == id:
                sym = rword[i]
                flag = 1
        if flag == 0:  # sym is not a reserved word
            sym = "ident"

    elif ch.isdigit():
        k = 0
        num = 0
        sym = "number"
        while True:
            a.append(ch)
            k += 1
            getch()
            if not ch.isdigit():
                break
        if k > nmax:
            error(30)
        else:
            id = "".join(a)

    elif ch == ':':
        getch()
        if ch == '=':
            sym = "becomes"
            getch()
        else:
            sym = "colon"

    elif ch == '>':
        getch()
        if ch == '=':
            sym = "geq"
            getch()
        else:
            sym = "gtr"

    elif ch == '<':
        getch()
        if ch == '=':
            sym = "leq"
            getch()
        elif ch == '>':
            sym = "neq"
            getch()
        else:
            sym = "lss"
    else:
        sym = ssym[ch]
        getch()


# --------------POSITION FUNCTION----------------------------
def position(tx, k):
    global table;
    table[0] = tableValue(k, "TEST")
    i = tx
    while table[i].name != k:
        i = i - 1
    return i


# ---------------ENTER PROCEDURE-------------------------------
def enter(tx, k):
    global id;
    tx[0] += 1
    while (len(table) > tx[0]):
        table.pop()
    x = tableValue(id, k)
    table.append(x)


# --------------CONST DECLARATION---------------------------
def constdeclaration(tx):
    global sym, id;
    if sym == "ident":
        temp = id
        getsym()
        if sym == "eql":
            getsym()
            if sym == "number":
                id = temp
                enter(tx, "const")
                getsym()
            else:
                error(2)
        else:
            error(3)
    else:
        error(4)


# -------------VARIABLE DECLARATION-----------------------------------
def vardeclaration(tx):
    global sym;
    if sym == "ident":
        enter(tx, "variable")
        getsym()
    else:
        error(4)


# -------------BLOCK------------------------------------------------
def block(tableIndex):
    tx = [1]
    tx[0] = tableIndex
    global sym, id;
    while sym == 'CONST' or sym == 'VAR' or sym == 'PROC':
        if sym == "CONST":
            while True:  # makeshift do while in python
                getsym()
                constdeclaration(tx)
                if sym != "comma":
                    break
            if sym != "semicolon":
                error(10);
            getsym()

        if sym == "VAR":
            while True:
                getsym()
                vardeclaration(tx)
                if sym != "comma":
                    break
            if sym != "semicolon":
                error(10)
            getsym()

        while sym == "PROCEDURE":
            getsym()
            if sym == "ident":
                enter(tx, "procedure")
                getsym()
            else:
                error(4)
            if sym != "semicolon":
                error(10)
            getsym()
            block(tx[0])

            if sym != "semicolon":
                error(10)
            getsym()

    statement(tx[0])


# --------------STATEMENT----------------------------------------
def statement(tx):
    global sym, id;
    if sym == "ident":
        i = position(tx, id)
        if i == 0:
            error(11)
        elif table[i].kind != "variable":
            error(12)
        getsym()
        if sym != "becomes":
            error(13)
        getsym()
        expression(tx)

    elif sym == "CALL":
        getsym()
        if sym != "ident":
            error(14)
        i = position(tx, id)
        if i == 0:
            error(11)
        if table[i].kind != "procedure":
            error(15)
        getsym()

    elif sym == "IF":
        getsym()
        condition(tx)
        if sym != "THEN":
            error(16)
        getsym()
        statement(tx)
        # added ELSE as a possibility. If there's an ELSE, run that statement. If not, move on.
        if sym == 'ELSE':
            getsym()
            statement(tx)

    elif sym == "BEGIN":
        while True:
            getsym()
            statement(tx)
            if sym != "semicolon":
                break
        if sym != "END":
            error(17)
        getsym()

    elif sym == "WHILE":
        getsym()
        condition(tx)
        if sym != "DO":
            error(18)
        getsym()
        statement(tx)

    # if REPEAT, keep getting symbols and running statements as long as there are semicolons between them
    elif sym == "REPEAT":
        while True:
            getsym()
            statement(tx)
            if sym != "semicolon":
                break
        if sym != "UNTIL":  # if the next symbo wasn't a semicolon, it has to be UNTIL, or error
            error(28)
        getsym()
        condition(tx)

    elif sym == "WRITE":
        getsym()
        if sym != "lparen":  # if WRITE, the next symbol has to be a '('
            error(27)
        while True:  # keeping evaluating expressions as long as there are commas between symbols
            getsym()
            expression(tx)
            if sym != "comma":
                break
        if sym != "rparen":  # we has two non-commas in a row, so this had better be a closing parenthesis
            error(22)
        getsym()

    # WRITELN has identical requirements to WRITE
    elif sym == "WRITELN":
        getsym()
        if sym != "lparen":
            error(27)
        while True:
            getsym()
            expression(tx)
            if sym != "comma":
                break
        if sym != "rparen":
            error(22)
        getsym()

    elif sym == "FOR":
        getsym()
        if sym != "ident":  # an identifier must follow FOR
            error(29)
        i = position(tx, id)
        if i == 0:
            error(11)
        elif table[i].kind != "variable":  # also, the identifier must be a variable, not  a constant
            error(30)
        getsym()
        if sym != "becomes":  # a ':=' must follow the variable
            error(13)
        getsym()
        expression(tx)  # evaluate the expression
        if sym != "TO" and sym != "DOWNTO":  # after the expression, either TO or DOWNTO is required
            error(31)
        getsym()
        expression(tx)  # evaluate the DOWNTO expression
        if sym != "DO":  # after the conditional statement, we have to have a DO
            error(18)
        getsym()
        statement(tx)  # perform the statement in the loop

    elif sym == "CASE":
        getsym()
        expression(tx)  # evaluate the expression for CASE
        if sym != "OF":  # OF is required after CASE
            error(32)
        getsym()
        while sym == "ident" or sym == "number":  # loop as long as the current symbol evaluates to a number
            if sym == "ident":
                i = position(tx, id)
                if i == 0:
                    error(11)
                elif table[i].kind != "const":  # this number also cannot change, thus it must be a constant
                    error(25)
            getsym()
            if sym != "colon":  # a colon must follow immediately after the case id
                error(33)
            getsym()
            statement(tx)
            if sym != "semicolon":  # each case must end with a semicolon
                error(10)
            getsym()
        if sym != "CEND":  # the end of the CASE block ends with CEND
            error(34)
        getsym()


# --------------EXPRESSION--------------------------------------
def expression(tx):
    global sym;
    if sym == "plus" or sym == "minus":
        getsym()
        term(tx)
    else:
        term(tx)

    while sym == "plus" or sym == "minus":
        getsym()
        term(tx)


# -------------TERM----------------------------------------------------
def term(tx):
    global sym;
    factor(tx)
    while sym == "times" or sym == "slash":
        getsym()
        factor(tx)


# -------------FACTOR--------------------------------------------------
def factor(tx):
    global sym;
    if sym == "ident":
        i = position(tx, id)
        if i == 0:
            error(11)
        getsym()

    elif sym == "number":
        getsym()

    elif sym == "lparen":
        getsym()
        expression(tx)
        if sym != "rparen":
            error(22)
        getsym()

    else:
        #        print "sym here is: ", sym
        error(24)


# -----------CONDITION-------------------------------------------------
def condition(tx):
    global sym;
    if sym == "ODD":
        getsym()
        expression(tx)

    else:
        expression(tx)
        if not (sym in ["eql", "neq", "lss", "leq", "gtr", "geq"]):
            error(20)
        else:
            getsym()
            expression(tx)


# -------------------MAIN PROGRAM------------------------------------------------------------#

rword.append('BEGIN')
rword.append('CALL')
rword.append('CONST')
rword.append('DO')
rword.append('END')
rword.append('IF')
rword.append('ODD')
rword.append('PROCEDURE')
rword.append('THEN')
rword.append('VAR')
rword.append('WHILE')

# Added reserved words:
rword.append('ELSE')
rword.append('REPEAT')
rword.append('UNTIL')
rword.append('FOR')
rword.append('TO')
rword.append('DOWNTO')
rword.append('CASE')
rword.append('OF')
rword.append('CEND')
rword.append('WRITE')
rword.append('WRITELN')

ssym = {'+': "plus",
        '-': "minus",
        '*': "times",
        '/': "slash",
        '(': "lparen",
        ')': "rparen",
        '=': "eql",
        ',': "comma",
        '.': "period",
        '#': "neq",
        '<': "lss",
        '>': "gtr",
        '"': "leq",
        '@': "geq",
        ';': "semicolon",
        ':': "colon", }

charcnt = 0
whichChar = 0
linelen = 0
ch = ' '
kk = al
a = []
id = '     '
errorFlag = 0
table.append(0)  # making the first position in the symbol table empty
sym = ' '


infile = sys.stdin  # path to input file
outfile = sys.stdout  # path to output file, will create if doesn't already exist

"""
    My IDE doesn't have the ability to read from stdin so I tested by hard-coding the file locations as the infile.
    So choose the file and uncomment that line if yours doesn't either (e.g., PyCharm).
"""

# infile = open('pre-mod.pas')  # path to input file
# infile = open('post-mod.pas')  # path to input file
# infile = open('error1.pas')  # path to input file
# infile = open('error2.pas')  # path to input file
# infile = open('error3.pas')  # path to input file
# infile = open('error4.pas')  # path to input file


getsym()  # get first symbol
block(0)  # call block initializing with a table index of zero

if sym != "period":  # period expected after block is completed
    error(9)

print >> outfile
if errorFlag == 0:
    print >> outfile, "Successful compilation!"