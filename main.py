# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pathlib
import tkinter as tk
from apscheduler.schedulers.background import BackgroundScheduler
import os
from datetime import datetime
from slugify import slugify
import playsound
from PIL import ImageTk, Image
from Reader.BPTReader import BPTReader
from tkinter import filedialog


class Timer:
    def __init__(self):
        self.minute = 6
        self.seconds = 59

    def reset(self):
        self.minute = 6
        self.seconds = 59

    def current_timer(self):
        return str(self.minute) + ":" + str(self.seconds)

    def update_timer(self):
        if self.seconds == 0:
            if self.minute == 0:
                pass
            else:
                self.minute -= 1
                self.seconds = 59
        else:
            self.seconds -= 1


def get_random_card():
    clear_input_text()
    if input_text.cget("state") == "disabled":
        input_text.config(state="normal", background="white")
    label_topic.config(text=reader.get_random_topic())
    timer.reset()
    label_file_saved.config(text="")


def save_answers():
    ans = input_text.get("1.0", 'end-1c')
    file_location = input_save_location.get("1.0", "end-1c")

    if not os.path.isdir(file_location):
        label_file_saved.config(text="'{}' is not valid directory".format(file_location), fg="red")
        return

    filename = slugify(reader.current_topic) + datetime.now().strftime("%d-%b-%Y-%H-%M-%S") + ".txt"

    full_file_path = os.path.join(file_location, filename)
    if ans:
        try:
            file = open(full_file_path, "w+")
            file.write(ans)
            file.close()
            label_file_saved.config(text="File saved successfully", fg="green")
        except Exception as e:
            label_file_saved.config(text="There was an error saving a file", fg="red")
            print("cannot write to file {}".format(e))


def clear_input_text():
    if input_text.cget("state") == "normal":
        input_text.delete('1.0', tk.END)
    else:
        input_text.config(state="normal")
        input_text.delete('1.0', tk.END)
        input_text.config(state="disabled")

    label_file_saved.config(text="")


def update_stopwatch():
    timer.update_timer()
    label_timer.config(text=timer.current_timer())
    if timer.seconds == 0 and timer.minute == 0:
        input_text.config(state="disabled", background="light grey")

    # save file


process = None


def stop_music():
    global process
    if process is not None:
        process.terminate()
        process = None


def play_music():
    global process
    process = Process(name="sound", target=play, daemon=True)
    process.start()


def play():
    playsound.playsound("Enchanted_TS.mp3")


def show_photo():
    if button_show_me.cget("text") == "show love birds <3":
        love_birds_label.grid()
        button_show_me.config(text="Hide love birds :'(")
    else:
        love_birds_label.grid_forget()
        button_show_me.config(text="show love birds <3")
    pass


def ask_open_directory():
    global answers_saved_path
    answers_saved_path = filedialog.askdirectory()
    if answers_saved_path:
        input_save_location.delete("1.0", tk.END)
        input_save_location.insert(tk.INSERT, answers_saved_path)


def browse_excel_file():
    excel_path = filedialog.askopenfile()
    if excel_path:
        label_excel_location.config(text=excel_path.name)

    reader.parse_file(excel_path.name)
    reader.get_all_topics()
    button.update()


if __name__ == "__main__":
    answers_saved_path = "C:\\Answers"
    reader = BPTReader()

    current_path = pathlib.Path().resolve()
    settings_file = open(str(current_path) + "\\settings.txt", "r")
    excel_file_path = settings_file.readline()
    settings_file.close()

    reader.parse_file(excel_file_path)
    reader.get_all_topics()

    timer = Timer()

    window = tk.Tk()
    window.title("Flash card revision")

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    window.geometry(str(screen_width)+"x"+str(screen_height))

    excel_file = tk.Button(window, text="Browse Excel", command=browse_excel_file)
    excel_file.grid(row=8, column=0, sticky="w", padx="30", pady="10")

    label_excel_location = tk.Label(window, text="C:test")
    label_excel_location.grid(row=8, column=0, sticky="w", padx="110")

    schedule = BackgroundScheduler()
    schedule.add_job(update_stopwatch, "interval", seconds=1)
    schedule.start()

    label_topic = tk.Label(window, text=reader.get_random_topic(), fg="red", font="Arial 12 bold")
    label_topic.grid(row=1, column=0)
    label_topic.grid_rowconfigure(1, weight=1)
    label_topic.grid_columnconfigure(1, weight=1)

    label_timer = tk.Label(window, text=timer.current_timer(), fg="black")
    label_timer.grid(row=2, column=0, padx="5")

    button = tk.Button(window, text="Get card", fg="black", command=get_random_card)
    button.grid(row=3, column=0, pady=10)

    label_save_location = tk.Button(window, text="location:", command=ask_open_directory)
    label_save_location.grid(row=4, column=0, sticky="w", padx=30)

    input_save_location = tk.Text(window, height=1, width=80)
    input_save_location.insert(tk.INSERT, answers_saved_path)
    input_save_location.grid(row=4, column=0, padx=90, sticky="w")

    input_text = tk.Text(window, height=15, width=100)
    input_text.grid(row=5, column=0, columnspan="3", padx=30, pady=10)

    button_save = tk.Button(window, text="Save", fg="black", command=save_answers)
    button_save.grid(row=6, column=0, sticky="w", padx=30)

    button_clear = tk.Button(window, text="Clear", fg="black", command=clear_input_text)
    button_clear.grid(row=6, column=0, stick="w", padx="80")

    #------------------------------------

    from multiprocessing import Process

    button_play_music = tk.Button(window, text="Play", command=play_music)
    button_play_music.grid(row=6, column=0, stick="w", padx="130")

    button_stop = tk.Button(window, text="Stop", command=stop_music)
    button_stop.grid(row=6, column=0, stick="w", padx="180")

    button_show_me = tk.Button(window, text="show love birds <3", command=show_photo)
    button_show_me.grid(row=6, column=0, stick="w", padx="230")

    label_file_saved = tk.Label(window)
    label_file_saved.grid(row=7, column=0, stick="w", padx="50")

    img = ImageTk.PhotoImage(Image.open("heart.jpg").resize((450, 300), Image.ANTIALIAS))

    love_birds_label = tk.Label(window, image=img)
    love_birds_label.grid(row=8, rowspan=2, columnspan=2)
    love_birds_label.grid_forget()

    window.mainloop()
