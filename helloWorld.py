import tkinter as tk
import tkinter.ttk as ttk
import websocket
import json
import threading
import time
from threading import Timer

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.webs = Sokk()
        self.webs.start()
        # self.timer = Print(self.send, 0.2)
        # self.timer.start()
        self.timer = RepeatedTimer(0.2, self.send)
        self.master.protocol("WM_DELETE_WINDOW", lambda: self.close())
        self.master.bind('<Escape>', lambda e: print('fff'))
        self.pack()
        self.master.title('łojoj')
        # self.master.iconname('ddd.png')
        # self.create_widgets()
        self.xx = self.display()
        self.button()
        self.style = ttk.Style()
        self.style.configure("BW.TLabel", foreground="black", background="white", font='arial 44')
        
    def send(self):
        self.webs.WS.send("{COMMAND: 'GET_MOD_INFO'}")
        x = json.loads(self.webs.getMessage())
        try:
            self.xx['text']=(int(x['RECORD']['Mass'][0]['NetAct']['Value']))
        except:
            print('coś nie tak')

        if (x['COMMAND'] == 'EDIT_MESSAGE' and x['PARAM'] == 'SHOW' and x['RECORD']['Type'] == 'Catalog'):
            self.new_window(Win2, x['RECORD']['Items'], self.webs)
        
    def close(self):
        self.timer.stop()
        self.master.destroy()
        
        self.webs.close()
        # self.webs.exit()
        self.timer = 0
        

    def setLabelText(self, text):
        print(text)
        self.xx['text'] = self.xx['text'] + text
    def display(self):
        displayF = tk.Frame(self)
        displayF.pack(side='top',fill='both', expand='yes')
        label = ttk.Label(displayF, style='BW.TLabel')
        label['text'] = ''
        label.pack()
        return label
    def button(self):
        for key in ("123", "456", "789", "-0.", '+-*='):
            keyF = tk.Frame(self)
            keyF.pack(side='top',fill='both', expand=1)
            for char in key:
                button = tk.Button(keyF)
                button['text'] = char
                button['bg'] = '#21dccb'
                button['cursor'] = 'hand2'
                button['borderwidth'] = 2
                # button['width'] = 15
                button['command'] = lambda x=char: self.setLabelText(x)
                button.pack(side='left', expand=1)
        keyF1 = tk.Frame(self)
        keyF1['height'] = 200
        keyF1.pack(side='top')
        butt = tk.Button(keyF1)
        butt['text'] = 'Nowe'
        butt['command'] = self.sendMenu
        butt.pack()
        # spinbox = ttk.Spinbox(keyF1)
        # spinbox['from'] = 0
        # spinbox['to'] = 5
        # spinbox['increment'] =0.5
        # spinbox['wrap'] = True
        # # spinbox['height'] = 20
        # spinbox['command'] = self.uuu
        # spinbox.pack()
    def sendMenu(self):
        self.webs.WS.send("{COMMAND: 'EXECUTE_ACTION', PARAM: 'actSetup'}")
    def uuu(self):
        print('xxxxxx')
    
    def new_window(self, _class, array, thread):
        try:
            if self.new.state() == "normal":
                # self.new.focus()
                self.new.destroy()
                self.new = tk.Toplevel(self)
                _class(self.new, array, thread)
        except:
            self.new = tk.Toplevel(self)
            _class(self.new, array, thread)
        # except:
        #     pass
    
    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there['text'] = "Hello world"
        self.hi_there['command'] = self.say_hi
        self.hi_there.pack(side="top")

        self.label = ttk.Label(text="TEXT", style='BW.TLabel')
        self.label.pack()

        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.pack(side="bottom")
        self.hi_there.bind("<Enter>", self.turn_red)
    def say_hi(self):
        print("hi there, everyone!")
        # self.hi_there["bg"] = "red"
    
    def turn_red(self, event):
        event.widget["bg"] = "red"
class Win2:
    def __init__(self, root, array,thread):
        self.root = root
        # self.root.geometry("300x300+200+200")
        self.root["bg"] = "#21dccb"
        # keyF1 = tk.Frame(self.root)
        # keyF1['height'] = 200
        # keyF1.pack(side='top')
        # self.quit = tk.Button(keyF1)
        # self.quit['text'] = 'Nowe'
        # self.quit.pack()
        print(array)
        self.menus(array)
        self.thread = thread

    def menus(self, array):
        # i = 0
        # j = 0
        
        for w in range(5):
            keyF = tk.Frame(self.root)
            keyF.pack(side='top')
            for i in range (5):
                button = tk.Button(keyF)
                button['text'] = array[i+w]['Name']
                button['command'] = lambda x=array[i+w]: print(x)
                button.pack(side='left')
    
    def sendTap(self, guid, menuGuid):
        self.thread.WS.send("{COMMAND: 'TAP_PARAM', PARAM: param, KEY: menuGuid}")
class Print(threading.Thread):
    def __init__(self, fn, time=1):
        threading.Thread.__init__(self)
        self.time = time
        self.is_start = True
        self.fn = fn
        # self.thread = thread

    def run(self):
        while self.is_start:
            time.sleep(self.time)
            print('timer')
            self.fn()
            # self.thread.WS.send("{COMMAND: 'GET_MOD_INFO'}")

    def stop(self):
        self.is_start = False
class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

class Sokk(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        websocket.enableTrace(True)
        self.time = Print(2)
        
        self.WS = websocket.WebSocketApp("ws://10.10.3.60:4101",
                                on_message = self.on_message,
                                on_error = self.on_error,
                                on_close = self.on_close)
        self.test=''
    def getMessage(self):
        return self.test
    def setMessage(self, text):
        self.test = text

    def run(self):
        self.WS.on_open = self.on_open

        self.WS.run_forever()
        # self.time.start()
        

    def close(self):
        self.WS.close()
    def on_message(self, message):
        y = json.loads(message)
        # print('text: '+self.text)
        # print("test:" + message)
        self.test = message
        
        # print('text: '+test)


    def on_error(ws, error):
        print(error)


    def on_open(self):
        print('sok')
        self.WS.send('{"COMMAND": "REGISTER_LISTENER", "PARAM": "MENU"}')
    def on_close(ws):
        print("### closed ###")
        
root = tk.Tk()
app = App(master=root)

app.mainloop()
