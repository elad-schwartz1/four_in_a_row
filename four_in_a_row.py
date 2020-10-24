################################################################################
# FILE : four_in_a_row.py
# WRITER: Elad_Schwartz
# DESCRIPTION: File contains main runner function for 4 in a row game. Uses graphics
#              imported from GUI file
################################################################################


from ex12.graphics import *

INSTRUCTIONS = 'Each player attempts to get 4 consecutive disks in a row. A win can be achieved in horizontal\n' \
               'vertical or diagonal directions. Before starting the game, player types must be selected for\n' \
               'player 1 and player 2 (options are AI or Human Players)'

INTRO = 'WELCOME TO CONNECT 4\n' \
        'We hope you had as much\n ' \
        'as we had creating this.'


def instructs():
    wnd = tk.Tk()
    wnd.winfo_toplevel().title("INSTRUCTIONS")
    wnd.configure(background='light steel blue')
    label1 = tk.Label(wnd, text=INSTRUCTIONS, font=("Courier", 12), bg='light steel blue')
    label1.pack()

def intro():
    wnd = tk.Tk()
    wnd.geometry('400x400')
    wnd.configure(background='light steel blue')
    wnd.winfo_toplevel().title("WELCOME")
    label1 = tk.Label(wnd, text=INTRO, font=("Courier", 20), bg='light steel blue')
    label1.place(x=200, y=200, anchor="center")

if __name__ == "__main__":
    root = tk.Tk()
    root.winfo_toplevel().title("Connect Four!!!!!")
    menubar = tk.Menu(root)

    # create a pulldown menu, and add it to the menu bar
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Instructions", command=instructs)
    filemenu.add_command(label="Introduction", command=intro)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="Help", menu=filemenu)

    root.config(menu=menubar)
    my = GUI(root)
    root.mainloop()