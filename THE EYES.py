# CHARON :
# Script for Tkinter GUI chat client. 

import tkinter
import tkinter.ttk as ttk
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def receive():
    """ Handles receiving of messages. """
    while True:
        try:
            msg = sock.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break

def send(event=None):
    """ Handles sending of messages. """
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    sock.send(bytes(msg, "utf8"))
    if msg == "#quit":
        sock.close()
        top.quit()

def on_closing(event=None):
    """ This function is to be called when the window is closed. """
    my_msg.set("#quit")
    send()

def darkstyle(root):
    ''' Return a dark style to the window'''
    
    style = ttk.Style(root)
    root.tk.call('source', 'azure dark/azure dark.tcl')
    style.theme_use('azure')
    style.configure("Accentbutton", foreground='white')
    style.configure("Togglebutton", foreground='white')
    return style

top = tkinter.Tk()
#top.iconbitmap("icon.ico")
top.title("THE EYES")
messages_frame = tkinter.Frame(top)
style = darkstyle(top)

my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=70, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()

messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg, bd = 5, foreground="White")
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = ttk.Button(top, text="Send", style="Accentbutton", command=send)
send_button.pack()


top.protocol("WM_DELETE_WINDOW", on_closing)



HOST = "127.0.0.1"
PORT = 5050
BUFSIZ = 1024
ADDR = (HOST, PORT)
sock = socket(AF_INET, SOCK_STREAM)
sock.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution.