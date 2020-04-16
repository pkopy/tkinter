import tkinter as tk
from PIL import ImageTk
class  HelloWorld(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        image = Image.open('ddd.png')
        label = tk.Label(self, text="Hello World!")
        label.pack(padx=20, pady=20) # Pack it into the window

root = tk.Tk()

main = HelloWorld(root)
main.pack(fill='both', expand=True)

root.mainloop()