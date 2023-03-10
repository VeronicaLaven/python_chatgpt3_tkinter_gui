
from tkinter import *
from tkinter import messagebox
from tkinter import Scrollbar
from PIL import Image, ImageTk
import openai
import configparser

# load API key from config.ini
config = configparser.ConfigParser()
config.read('config.ini')
api_key = config['openai']['api_key']
openai.api_key = api_key

# set up GPT-3.5 model
gpt3_model = "text-davinci-003"

# TKinter gui
root = Tk()

# set gui window width and height
root.geometry("570x580")

# configure gui background color #821040 - wine color
root.config(bg="#821040")


# top chat image file
image = Image.open("images/chat.png")

# set the desired width and height
img_width = 100
img_height = 70

# resize the image to fit the desired width and height
image = image.resize((img_width, img_height), Image.ANTIALIAS)

# convert the image to a Tkinter-compatible photo image
photo = ImageTk.PhotoImage(image)

# create a label to hold the image with the desired width and height
image_label = Label(root, image=photo, width=img_width, height=img_height)

# add top image label to the window
image_label.place(x = 45, y = 20)

# add top heading label
label = Label(root, text="Enter Prompt to Chat!", bg="#821040", fg="white", font=("verdana", 24, "bold"), bd=2)
label.place(x = 160, y = 45)

# define response function to extract data from entry widget
def response(event=None):
    entry_prompt = prompt_box.get()
    # insert question / prompt user enters
    prompt_log_box.insert(0, "Prompt Log : " + entry_prompt)
    answer = openai.Completion.create(
        engine=gpt3_model,
        prompt=entry_prompt,
        max_tokens = 2000,
        stop = None,
    )
    message = answer.choices[0].text
    response_box.configure(wrap=WORD)
    response_box.insert(END, "chatbot : " + message + " \n")

# define function to clear box contents
def clear():
    prompt_box.delete(0, END)
    prompt_log_box.delete(0,END)
    response_box.delete('1.0', END)

# create box where user enters prompt
message = StringVar()
prompt_box = Entry(root, textvariable=message, font=('verdana', 12, 'normal'), border=0, width=48)
prompt_box.place(x=45, y=105)

# create horizontal scrollbar for prompt_box
prompt_box_scrollbar = Scrollbar(root, orient=HORIZONTAL, command=prompt_box.xview)
prompt_box_scrollbar.pack(side=BOTTOM, fill=X)
prompt_box.configure(xscrollcommand=prompt_box_scrollbar.set)


# button to send prompt entered by user
send_button = Button(root, text="Send", command=response)
send_button.config(borderwidth=0, highlightthickness=0)
send_button.place(x=448, y=105)


# create prompt log box
prompt_log_box = Listbox(root, height=5, width=52)
prompt_log_box.place(x=45, y=150)

# create response box that contains chatbot response
response_box = Text(root, height=14, width=58, wrap=WORD, font=('verdana', 12, 'normal'), border=0)
response_box.place(x=45, y=260)

# create vertical scrollbar for chatbot response box
scrollbar = Scrollbar(root, orient=VERTICAL, command=response_box.yview)

response_box.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)

# bind the Enter key to the send_message function
root.bind('<Return>', response)


# button to clear contents from all boxes
clearbutton = Button(root, text='Clear', command=clear)
clearbutton.config(borderwidth=0, highlightthickness=0)
clearbutton.place(x=45, y=510)


# define a function to copy response text generated from chatbot
def copy_text():
    text = response_box.get("1.0", "end-1c")
    root.clipboard_clear()
    root.clipboard_append(text)

# button to copy response box contents
copy_button = Button(root, text="Copy", command=copy_text)
copy_button.config(borderwidth=0, highlightthickness=0)
copy_button.place(x=250, y=510)



# define a function to close the window
def close():
   #root.destroy()
   root.quit()

# button to call close() to exit app
close_button = Button(root, text= "Exit", command=close)
close_button.config(borderwidth=0, highlightthickness=0)
close_button.place(x=457, y=510)


root.mainloop()
