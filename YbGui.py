import yt_dlp
import tkinter
import customtkinter
from tkinter import filedialog
import json
from PIL import Image
from threading import Thread

# load config
with open('res/config.json', 'r', encoding='utf-8') as file:
    data = json.load(file)


# view settings
customtkinter.set_appearance_mode(data['mode'])
customtkinter.set_default_color_theme("blue")
app = customtkinter.CTk()
app.geometry("800x600")
app.resizable(False, False)
app.title("YtpLoader")


def save_config():
    with open('res/config.json', 'w', encoding='utf-8') as content:
        json.dump(data, content, indent=4, ensure_ascii=False)


def choose_dir():
    selected_folder = filedialog.askdirectory()
    data['path'] = selected_folder



def download():
    class MyLogger:
        count = 0
        def debug(self, msg):
            # For compatibility with youtube-dl, both debug and info are passed into debug
            # You can distinguish them by the prefix '[debug] '
            if msg.startswith('[debug] '):
                pass
            else:
                self.info(msg)

        def info(self, msg):
            self.count += 1
            textbox.insert(f"{self.count}.0", f"{msg}\n")

        def warning(self, msg):
            pass

        def error(self, msg):
            print(msg)



    url = entry.get()
    path = data['path']

    if "https://" in url:
        ydl_opts = {
        'format': 'ba[ext=m4a]', # bestaudio.m4a
        'paths': {'home': f'{path}'}, # temp and main files in one folder
        'retries': 10,
        'quiet': True, # without logs
        'progress': True, # show progress bar
        'skip_unavailable_fragments': True,
        'logger': MyLogger(),

        #'noplaylist': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download(url)
        except:
            print('Oops... Slomalsya')


def foo():
    th = Thread(target=download)
    th.start()

def change_appearance_mode_event(new_appearance_mode: str):
    customtkinter.set_appearance_mode(new_appearance_mode)
    data['mode'] = new_appearance_mode


# variables
dir_image = customtkinter.CTkImage(
    light_image=Image.open("res/folder.png"),
    dark_image=Image.open("res/folder.png"),
    size=(20, 20)
)

# init
label = customtkinter.CTkLabel(
    master=app,
    text="Put YouTube link to download",
    font=('da', 20)
)
entry = customtkinter.CTkEntry(
    master=app,
    placeholder_text="Url..."
)
choose_dir_button = customtkinter.CTkButton(
    master=app,
    text="",
    image=dir_image,
    command=choose_dir
)
download_button = customtkinter.CTkButton(
    master=app,
    text="Ok",
    command=foo
)
mode_opt = customtkinter.CTkOptionMenu(
    master=app,
    values=["Light", "Dark", "System"],
    command=change_appearance_mode_event
)
frame = customtkinter.CTkFrame(
    master=app,
    corner_radius=10
)

textbox = customtkinter.CTkTextbox(frame)

# create ui
def load():
    mode_opt.set(data['mode'])
    mode_opt.place(relx=0.01, rely=0.01, relwidth=0.1)
    label.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)
    choose_dir_button.place(relx=0.04, rely=0.2, relwidth=0.05)
    entry.place(relx=0.1, rely=0.2, relwidth=0.8)
    download_button.place(relx=0.91, rely=0.2, relwidth=0.05)
    frame.place(relx=0.5, rely=0.63, relwidth=0.9, relheight=0.65, anchor=tkinter.CENTER)
    textbox.place(relx=0, rely=0, relwidth=1, relheight=1)


# entry point
if __name__ == "__main__":
    load()
    try:
        app.mainloop()
    finally:
        save_config()
        exit()
