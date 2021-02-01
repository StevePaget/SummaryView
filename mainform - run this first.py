import tkinter as tk
from tkinter import messagebox

from DB_manager import *

class Main(tk.Tk):
    def __init__(self, *args, **kwargs):
        self.db = DatabaseUtility("testDB.db")
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("800x800+100+100")
        self.title("Database Demo")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in [SummaryView]:

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(SummaryView)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        try:
            frame.loadUp()
        except AttributeError:
            pass

class SummaryView(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        self.db = controller.db
        tk.Frame.__init__(self,parent)

        #make a list box to hold the data
        self.table = tk.Listbox(self,width=38, bg="white", font=("Courier",12))
        self.table.grid(row=0,column=0)

        #make a detail pane
        self.detailView = tk.Listbox(self,width=38, bg="#FFAAFF", font=("Courier",12))
        self.detailView.grid(row=1,column=0)
        self.table.bind("<<ListboxSelect>>",self.showDetail)

    def loadUp(self):
        # this will grab the latest data and fill in the table
        
        # we want the table to display the people and their average score
        # we can do this using SQL, so we don't need to calculate the averages manually

        result = self.db.RunCommand("SELECT People.name, AVG(Scores.score) FROM People, Scores WHERE People.username = Scores.username GROUP BY People.username")
        # the above SQL command means "Get the Names and Average Scores from the People and Scores table, where the usernames match"
        self.data = result.fetchall()
        
        # now put the results into the listbox called self.table
        self.table.delete(0,tk.END)
        # Add a header row to the table. Colour just this row blue.
        self.table.insert(0,"Name".ljust(25," ")+"Average Score".ljust(13," "))
        self.table.itemconfig(0, {'fg':'blue'})
        # go through all the lines of data, adding them to the listbox

        for line in self.data:
            self.table.insert(tk.END,line[0].ljust(25,".")+str(int(line[1])).ljust(13," "))

    def showDetail(self,e):
        # show the individual scores for this person
        selectedindex = self.table.curselection()[0]
        if selectedindex >0:
            selectedname = self.data[selectedindex-1][0]
        result = self.db.RunCommand("SELECT * from People, Scores WHERE Scores.username = People.username and People.name = ?", (selectedname,))
        detailedScores = result.fetchall()
        self.detailView.delete(0,tk.END)
        self.detailView.insert(0,"This user's scores are:")
        self.detailView.itemconfig(0, {'fg':'blue'})

        for line in detailedScores:
            self.detailView.insert(tk.END, line[4])

def createDemoData():
    # this WIPES the tables and makes new ones, for demo purposes
    db = DatabaseUtility("testDB.db")
    db.RunCommand("DROP TABLE IF EXISTS People")
    db.RunCommand("CREATE TABLE People (username text, name text, form text)")
    # make some test people
    db.RunCommand("INSERT INTO People VALUES (?,?,?)", ["jacone", "Jack O'Neill", "7SAP"])
    db.RunCommand("INSERT INTO People VALUES (?,?,?)", ["samcar", "Sam Carter", "8PLI"])
    db.RunCommand("INSERT INTO People VALUES (?,?,?)", ["danjac", "Daniel Jackson", "8PLI"])
    db.RunCommand("DROP TABLE IF EXISTS Scores")
    db.RunCommand("CREATE TABLE Scores (username text, score int)")
    db.RunCommand("INSERT INTO Scores VALUES (?,?)", ["jacone", 10])
    db.RunCommand("INSERT INTO Scores VALUES (?,?)", ["jacone", 12])
    db.RunCommand("INSERT INTO Scores VALUES (?,?)", ["jacone", 13])
    db.RunCommand("INSERT INTO Scores VALUES (?,?)", ["samcar", 50])
    db.RunCommand("INSERT INTO Scores VALUES (?,?)", ["samcar", 34])
    db.RunCommand("INSERT INTO Scores VALUES (?,?)", ["samcar", 22])
    db.RunCommand("INSERT INTO Scores VALUES (?,?)", ["danjac", 29])



createDemoData()
app = Main()
app.mainloop()