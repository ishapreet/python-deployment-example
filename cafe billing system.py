from tkinter import*
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import pymysql
obj = Tk()
obj.geometry("965x580")
obj.configure(bg='light blue')
obj.title("Cafe's Billing System")
#***********************Listeners*****************
def quantityl(a,b,c):
    global quantityVar
    global costVar
    global itemrate
    quantity=quantityVar.get()
    if quantity != "":
        try:
            quantity=float(quantity)
            cost=quantity*itemrate
            quantityVar.set("%.2f"%quantity)
            costVar.set("%.2f"%cost)
        except ValueError:
            quantity=(quantity[:-1])
            quantityVar.set(quantity)
    else:
        quantity=0
        quantityVar.set("%.2f"%quantity)
def costl(a,b,c):
    global quantityVar
    global costVar
    global itemrate
    cost = costVar.get()
    if cost != "":
        try:
            cost = float(cost)
            quantity = cost/itemrate
            quantityVar.set("%.2f"%quantity)
            costVar.set("%.2f"%cost)
        except ValueError:
            cost = costVar[:-1]
            costVar.set(cost)
    else:
        cost=0
        costVar.set(cost)
#**********************login variables**************************************
uservar=StringVar()
pwvar=StringVar()
#****************main window variable***************************************
namevar=StringVar()
pnvar=StringVar()
addvar=StringVar()
emailvar=StringVar()
options = []
rateDict = {}
itemVariable = StringVar()
values = StringVar()
quantityVar = StringVar()
quantityVar.trace('w',quantityl)
itemrate=2
rateVar = StringVar()
rateVar.set("%.2f"%itemrate)
costVar = StringVar()
costVar.trace('w',costl)
Totalvar=StringVar()
entry1 = StringVar()
entry2 = StringVar()
entry3 = StringVar()
entry4 = StringVar()
global textreciept
#**************add item variables*********************************************
storeOptions = ['Frozen', 'Fresh']
namevar = StringVar()
ratevar = StringVar()
typevar = StringVar()
storevar = StringVar()
storevar.set(storeOptions[0])
itemList = list()
totalCost = 0.0
totalCostVar = StringVar()
totalCostVar.set("{}".format(totalCost))
updateItemId = ""
#***********************Tview******************************************
recieptV = ttk.Treeview(height=15, column=('Rate', 'Quantity', 'Cost'))
updateV = ttk.Treeview(height=10, column=('Name', 'Rate', 'Type', 'Store_Type'))
#************************add to list function***************************
def add_to_listf():
    global itemVariable
    global quantityVar
    global itemrate
    global costVar
    global itemList
    global totalCost
    global totalCostVar
    itemname=itemVariable.get()
    quantity=quantityVar.get()
    cost=costVar.get()
    conn = pymysql.connect(host='localhost', user='root', password="9999", database="bill system")
    cursor = conn.cursor()
    query="INSERT INTO bill(name,quantity,rate,cost) VALUES('{}','{}','{}','{}')".format(itemname,quantity,itemrate,cost)
    cursor.execute(query)
    conn.commit()
    conn.close()
    listDict = {"name": itemname, "rate": itemrate, "quantity": quantity, "cost": cost}
    itemList.append(listDict)
    totalCost += float(cost)
    quantityVar.set("0")
    costVar.set("0")
    updaterecieptV()
    totalCostVar.set("{}".format(totalCost))
#********************************Double click update function***************
def OnDoubleClick(event):
    global namevar
    global ratevar
    global typevar
    global storedvar
    global updateItemId
    item = updateV.selection()
    updateItemId = updateV.item(item, "text")
    items_detail = updateV.item(item, "values")
    item_index = storeOptions.index(items_detail[3])
    typevar.set(items_detail[2])
    ratevar.set(items_detail[1])
    namevar.set(items_detail[0])
    storevar.set(storeOptions[item_index])
#*********************************update bill view******************
def updaterecieptV():
    records = recieptV.get_children()
    for element in records:
        recieptV.delete(element)
    for row in itemList:
        recieptV.insert('', 'end', text=row['name'], values=(row["rate"], row["quantity"], row["cost"]))
#********************************grtting item list in update**********************
def getitemlists():
    records = updateV.get_children()
    for element in records:
        updateV.delete(element)
    conn = pymysql.connect(host='localhost', user='root', password="9999", database="bill system")
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    query = "SELECT * FROM itemlist"
    cursor.execute(query)
    data = cursor.fetchall()
    for row in data:
        updateV.insert('', 'end', text=row['Nameid'], values=(row['Name'], row['Rate'], row['Type'], row['Stored_Type']))
    updateV.bind("<Double-1>", OnDoubleClick)
    conn.close()
#***********************************generating reciept****************
#****************************remove widget function********************************
def removew():
    global obj
    for widget in obj.winfo_children():
        widget.place_forget()
        widget.grid_remove()
#********************************login function********************
def loginf():
    global uservar
    global pwvar
    Username=uservar.get()
    Password=pwvar.get()
    conn = mysql.connector.connect(host='localhost',user='root',password="9999",database="bill system")
    mycursor=conn.cursor()
    query = "select * from users where Username='{}' and Password='{}'".format(Username,Password)
    mycursor.execute(query)
    data = mycursor.fetchall()
    admin = False
    for row in data:
        admin=True
    conn.close()
    if admin:
        readalldata()
    else:
        messagebox.showerror("Invalid user","credentials enters are invalid")
#****************************function to read data from list of item*************************
def readalldata():
    global options
    global rateDict
    global itemVariable
    global itemrate
    global ratevar
    options = []
    rateDict = {}
    conn = pymysql.connect(host='localhost', user='root', password="9999", database="bill system")
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    query = "SELECT * FROM itemlist"
    cursor.execute(query)
    data = cursor.fetchall()
    count = 0
    for row in data:
        count+=1
        options.append(row['Nameid'])
        rateDict[row['Nameid']]=row['Rate']
        itemVariable.set(options[0])
        itemrate=(rateDict[options[0]])
    conn.close()
    rateVar.set(itemrate)
    if count==0:
        removew()
        additem()
    else:
        removew()
        mainwindow()
#**************************************menu's combination with rate***********************
def menulistener(event):
    global itemVariable
    global rateDict
    global itemrate
    item=itemVariable.get()
    itemrate=int(rateDict[item])
    rateVar.set("%.2f"%itemrate)
#**************************************additem button function*************
def additembl():
    removew()
    additem()
#*************************************updateitem button function in main************
def movetoupdate():
    removew()
    updateitem()

#***********************************logout button***********************
def logoutb():
    removew()
    adminlogin()
    uservar.set("")
    pwvar.set("")
#**************************************reset button********************
def resetbf():
    removew()
    mainwindow()
    itemVariable.set("")
    quantityVar.set("")
    rateVar.set("")
    costVar.set("")
    Totalvar.set("")
    entry1.set("")
    entry2.set("")
    entry3.set("")
    entry4.set("")
    recieptV.delete(*recieptV.get_children())
#*********************************exitbf********************************************
def exitbf():
    exitt=messagebox.askyesno("Cafe's Billing System","Confirm if you want to exit")
    if exitt>0:
        obj.destroy()
    return
#**********************************update button****************
def updateb():
    removew()
    showmenuf()
#*************************************add item function*********************
def additemf():
    global namevar
    global ratevar
    global typevar
    global storedvar
    name=namevar.get()
    rate=ratevar.get()
    type=typevar.get()
    storetype=storevar.get()
    nameid=name.replace(" ","_")
    conn = mysql.connector.connect(host='localhost', user='root', password="9999", database="bill system")
    mycursor = conn.cursor()
    query="INSERT INTO itemlist(Name,Nameid,Rate,Type,Stored_Type)VALUES('{}','{}','{}','{}','{}')".format(name,nameid,rate,type,storetype)
    mycursor.execute(query)
    conn.commit()
    conn.close()
    namevar.set("")
    ratevar.set("")
    typevar.set("")
    #storevar.set("")
#*************************************update item button*************************
def updateitemf():
    global namevar
    global ratevar
    global typevar
    global storedvar
    global updateItemId
    name = namevar.get()
    rate = ratevar.get()
    type = typevar.get()
    storetype = storevar.get()
    conn = mysql.connector.connect(host='localhost', user='root', password="9999", database="bill system")
    mycursor = conn.cursor()
    query = "UPDATE itemlist set Name='{}',Rate='{}',Type='{}',Stored_Type='{}' WHERE nameid='{}'".format(name,rate,type,storetype,updateItemId)
    mycursor.execute(query)
    conn.commit()
    conn.close()

    namevar.set("")
    ratevar.set("")
    typevar.set("")
    getitemlists()
#**************************update bill data (shoe entry)************************
def updatebilldata():
    records = recieptV.get_children()
    for element in records:
        recieptV.delete(element)
    conn = pymysql.connect(host='localhost', user='root', password="9999", database="bill system")
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    query = "SELECT * FROM bill"
    cursor.execute(query)
    data = cursor.fetchall()
    for row in data:
        recieptV.insert('', 'end', text=row['name'], values=(row["rate"], row["quantity"], row["cost"]))
    conn.close()
#********************************************loginPage*****************************
def adminlogin():
    titlelabel=Label(obj,text="Cafe's Billing System",font=('arial',40,'bold'),bd=15,bg='sky blue',fg='black',relief=SUNKEN,padx=217,justify=CENTER).grid(row=0,column=0)
    loginlabel=Label(obj,text="Admin Login",fg='black',bg='light blue',font=('arial',20,'underline','bold')).place(x=380,y=155)
    userlabel=Label(obj, text="Username:", fg='black', bg='light blue', font=('arial', 20)).place(x=330,y=220)
    pwlabel=Label(obj, text="Password:", fg='black', bg='light blue', font=('arial', 20)).place(x=330,y=300)
    t1=Entry(obj,textvar=uservar).place(x=490,y=230)
    t2=Entry(obj,textvar=pwvar,show="*").place(x=490,y=310)
    loginb=Button(obj,text="Login",width=20,height=2,font=('arial',12,'bold'),command=lambda:loginf()).place(x=375,y=370)
#****************************************Customer Info***********************************
def mainwindow():
    label = Label(obj, text="Customer Info:", bg="light blue", font=("arial", 12, 'bold'))
    label.place(x=5, y=6)
    f1 = Frame(obj, width=400, height=180, bd=14, relief=FLAT)
    f1.place(x=8, y=28)
    label1 = Label(f1, text="Name", font=('arial', 13))
    label1.grid(row=0, column=0, sticky=W)
    entry1 = Entry(f1,textvar=namevar)
    entry1.grid(row=0, column=1)
    label2 = Label(f1, text="Phone number", font=('arial', 13))
    label2.grid(row=1, column=0, sticky=W)
    entry2 = Entry(f1,textvar=pnvar)
    entry2.grid(row=1, column=1)
    label3 = Label(f1, text="Address", font=('arial', 13))
    label3.grid(row=2, column=0, sticky=W)
    entry3 = Entry(f1,textvar=addvar).grid(row=2, column=1)
    label4 = Label(f1, text="E-Mail", font=('arial', 13))
    label4.grid(row=3, column=0, sticky=W)
    entry4 = Entry(f1,textvar=emailvar).grid(row=3, column=1)
# ***********************************ORDER INFO FRAME**********************************
    orderlbl = Label(obj, text='Order Info:', bg="light blue", font=("arial", 12, 'bold'))
    orderlbl.place(x=280, y=6)
    f2 = Frame(obj, width=400, height=180, bd=14, relief=FLAT)
    f2.place(x=280, y=28)
    lbl1 = Label(f2, text="Select Item", font=('arial', 13))
    lbl1.grid(row=0, column=0, sticky=W)
    combo1 = OptionMenu(f2, itemVariable, *options, command=menulistener).grid(row=0, column=1)
    lbl2 = Label(f2, text="Quantity", font=('arial', 13))
    lbl2.grid(row=1, column=0, sticky=W)
    quantityentry = Entry(f2, textvar=quantityVar).grid(row=1, column=1)
    lbl3 = Label(f2, text="Rate", font=('arial', 13))
    lbl3.grid(row=2, column=0, sticky=W)
    rentry = Entry(f2, textvar=rateVar).grid(row=2, column=1)
    lbl4 = Label(f2, text="Cost", font=('arial', 13))
    lbl4.grid(row=3, column=0, sticky=W)
    centry = Entry(f2, textvar=costVar).grid(row=3, column=1)
    totall = Label(obj, text="Total", font=("arial", 15), bg="light blue").place(x=380, y=533)
    total = Entry(obj, textvar=totalCostVar).place(x=440, y=538)

#*****************************receipth function***************************************************************
    def print_reciept():
        textreciept.delete("1.0", END)
        global itemList
        global totalCost
        global entry1

        textreciept.insert(END, "=============Receipt==========\n")
        textreciept.insert(END, "==============================\n")
        textreciept.insert(END, "{:<25}{:<10}{:<15}{:<10}\n".format("Name", "Rate", "Quantity", "Cost"))
        textreciept.insert(END,"=============================\n")
        for item in itemList:
            textreciept.insert(END, "{:<25}{:<10}{:<15}{:<10}\n".format(item["name"], item["rate"], item["quantity"],item["cost"]))
        textreciept.insert(END, "==========================\n")
        textreciept.insert(END, "{:<25}{:<10}{:<18}{:<10}\n".format("TotalCost", " ", " ", totalCost))
        itemList = []
        totalCost = 0.0
        updaterecieptV()
        totalCostVar.set("{}".format(totalCost))

    #***********************buttons**************************************
    additem=Button(obj,text="Add Item",width=15,height=2,command=lambda:additembl()).place(x=555,y=28)
    updateitem=Button(obj,text="Update Items",width=15,height=2,command=lambda:movetoupdate()).place(x=695,y=28)
    showent=Button(obj,text="Show Entries",width=15,height=2,command=lambda:updateb()).place(x=825,y=28)
    logout=Button(obj,text="Logout",width=15,height=2,command=lambda:logoutb()).place(x=695,y=85)
    exitb = Button(obj, text="Exit", width=15, height=2,command=lambda:exitbf()).place(x=825,y=85)
    recieptl=Label(obj, text='Reciept:', bg="light blue", font=("arial", 12, 'bold'))
    recieptl.place(x=618,y=145)
    f3 = Frame(obj, width=310, height=335, bd=10, relief=FLAT)
    f3.place(x=610, y=170)


    receiptb=Button(obj, text="Reciept", width=15, height=2,command=lambda:print_reciept()).place(x=790, y=530)
    resetb = Button(obj, text="Reset", width=15, height=2, command=lambda: resetbf()).place(x=650, y=530)
    recieptV.place(x=10,y=190)
    addlistb=Button(obj,text="Add to List",width=15,height=2,command=lambda:add_to_listf()).place(x=555,y=85)
    scrollbar = Scrollbar(obj, orient="vertical", command=recieptV.yview)
    scrollbar.place(x=555, y=191)
    recieptV.configure(yscrollcommand=scrollbar.set)
    recieptV.heading('#0',text='Item Name')
    recieptV.column('#0',minwidth=0,width=160)
    recieptV.heading('#1', text='Rate')
    recieptV.column('#1',minwidth=0,width=120)
    recieptV.heading('#2', text='Quantity')
    recieptV.column('#2',minwidth=0,width=120)
    recieptV.heading('#3', text='Cost')
    recieptV.column('#3',minwidth=0,width=160)
    textreciept=Text(f3,font=("arial",12),bg="white",width=35,height=18)
    textreciept.grid(row=0,column=0)
    updaterecieptV()


    #******************add item*************************************
def additem():
    backbutton=Button(obj,text="Back", width=15, height=2,command=lambda:readalldata()).place(x=845, y=525)
    tlabel=Label(obj,text="Add Item",fg='black',bg='light blue',font=('arial',20,'underline','bold')).place(x=400,y=10)
    nlabel=Label(obj,text="Name:",font=('arial', 20),bg="light blue").place(x=140,y=100)
    nentry=Entry(obj,textvar=namevar).place(x=250,y=110)
    rlabel = Label(obj, text="Rate:", font=('arial', 20), bg="light blue").place(x=470, y=100)
    rentry = Entry(obj, textvar=ratevar).place(x=570, y=110)
    tlabel = Label(obj, text="Type:", font=('arial', 20), bg="light blue").place(x=140, y=150)
    tentry = Entry(obj, textvar=typevar).place(x=250, y=160)
    slabel = Label(obj, text="Stored Type:", font=('arial', 20), bg="light blue").place(x=470, y=150)
    sentry = OptionMenu(obj, storevar,*storeOptions).place(x=645,y=160)
    additemb = Button(obj, text="Add Item", width=20, height=2, font=('arial', 12, 'bold'),command=lambda:additemf()).place(x=375, y=250)
#*****************************************update item***************************************
def updateitem():
    bbutton = Button(obj, text="Back", width=15, height=2,command=lambda:readalldata()).place(x=845, y=525)
    ulabel = Label(obj, text="Update Item", fg='black', bg='light blue', font=('arial', 20, 'underline', 'bold')).place(x=400, y=10)
    nlbl = Label(obj, text="Name:", font=('arial', 20), bg="light blue").place(x=140, y=100)
    ntry = Entry(obj, textvar=namevar).place(x=250, y=110)
    rlbl = Label(obj, text="Rate:", font=('arial', 20), bg="light blue").place(x=470, y=100)
    rtry = Entry(obj, textvar=ratevar).place(x=570, y=110)
    tlbl = Label(obj, text="Type:", font=('arial', 20), bg="light blue").place(x=140, y=150)
    ttry = Entry(obj, textvar=typevar).place(x=250, y=160)
    slbl = Label(obj, text="Stored Type:", font=('arial', 20), bg="light blue").place(x=470, y=150)
    stry =  sentry = OptionMenu(obj, storevar,*storeOptions).place(x=645,y=160)
    upitemb = Button(obj, text="Update Item", width=20, height=2, font=('arial', 12, 'bold'),command=lambda:updateitemf()).place(x=375, y=220)
    updateV.place(x=150, y=300)
    scrollbar = Scrollbar(obj, orient="vertical", command=updateV.yview)
    scrollbar.place(x=815, y=300)
    updateV.configure(yscrollcommand=scrollbar.set)
    updateV.heading('#0', text='Item id')
    updateV.heading('#1', text='Name')
    updateV.column('#1', minwidth=0, width=160)
    updateV.heading('#2', text='Rate')
    updateV.column('#2', minwidth=0, width=120)
    updateV.heading('#3', text='Type')
    updateV.column('#3', minwidth=0, width=100)
    updateV.heading('#4', text='Stored Type')
    updateV.column('#4', minwidth=0, width=100)
    getitemlists()
#**********************************show entry button function/*********************
def showmenuf():
    bbutton = Button(obj, text="Back", width=15, height=2, command=lambda: readalldata()).place(x=845, y=525)
    ulabel = Label(obj, text="Entry Showing Window", fg='black', bg='light blue', font=('arial', 20, 'underline', 'bold')).place(x=370, y=10)
    recieptV.place(x=180, y=100)
    scrollbar=Scrollbar(obj,orient="vertical",command=recieptV.yview)
    scrollbar.place(x=786,y=101)
    recieptV.configure(yscrollcommand=scrollbar.set)
    recieptV.heading('#0', text='Item Name')
    recieptV.heading('#1', text='Rate')
    recieptV.column('#1', minwidth=0, width=160)
    recieptV.heading('#2', text='Quantity')
    recieptV.column('#2', minwidth=0, width=140)
    recieptV.heading('#3', text='Cost')
    recieptV.column('#3', minwidth=0, width=160)
    updatebilldata()

adminlogin()
obj.mainloop()
