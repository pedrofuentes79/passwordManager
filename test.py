from tkinter import *
import tkinter
r = Tk()
age = '''
O.o
    giga
'''
gage = 'vrum'
r.title("getherefast")

def gtc(dtxt):
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(dtxt)
    r.update()

tkinter.Button(text='age', command=gtc(age)).grid(column=1, row=0)
tkinter.Button(text='gage', command=gtc(gage)).grid(column=2, row=0)

r.mainloop()
