import tkinter as tk
from tkinter import filedialog as fd
root = tk.Tk()

root.title("Top 8 manager")
root.configure(background="white")
root.minsize(700, 700)
root.maxsize(700, 700)
root.geometry("1500x800-2000-500")

tk.Label(root, text="sUPER TOp 8 bracket maNAGER !!1!!1", font=("Comic Sans MS", 30), fg="red", background="white").pack()
tk.Label(root, text="by Cocci", background="white").pack()


fileLocation = ""
fileSelected = False
def CreateTop8():
    try:
        fileLocation = fd.asksaveasfile(filetypes=[("Bracket Files", "*.bracket")], defaultextension=[("Bracket Files", "*.bracket")]).name
        fileSelected = True
    except:
        pass
def OpenTop8():
    try:
        fileLocation = fd.askopenfilename(filetypes=[("Bracket Files", "*.bracket")], defaultextension=[("Bracket Files", "*.bracket")])
        fileSelected = True
    except: pass
CreateButton = tk.Button(root, text="Créer un top8", command=CreateTop8)
CreateButton.place(x=310, y=80)
CreateButton = tk.Button(root, text="Ouvrir un top8", command=OpenTop8)
CreateButton.place(x=260, y=120)

canvas = tk.Canvas(root, width=6500, height=500, bg="lightgray")
canvas.place(x=25, y=200)

root.mainloop()