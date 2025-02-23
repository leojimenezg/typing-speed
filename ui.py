from tkinter import Tk, Button, Canvas, Label, Entry, Frame
from typing import cast


class UI:
    def __init__(self, root: Tk):
        self.root: Tk = root
        self.root.geometry("800x800")
        self.root.configure(background="green")
        self.root.resizable(width=True, height=True)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.currentFrame: Frame = cast(Frame, None)

        self.switch_frame(MainUI)

    def keep_open(self):
        self.root.mainloop()

    def switch_frame(self, frameClass) -> None:
        if self.currentFrame is not None:
            self.currentFrame.destroy()

        self.currentFrame = frameClass(self.root, self)
        self.currentFrame.grid(row=0, column=0, sticky="nsew")
        self.currentFrame.grid_propagate(False)

        return None


class MainUI(Frame):
    def __init__(self, master: Tk, ui: UI):
        super().__init__(master)
        self.ui: UI = ui
        self.sepFont = ("Arial", 30, "bold")

        self.btn30Secs: Button = Button(self, text="30s", command="")
        self.btn30Secs.grid(row=0, column=0, sticky="nsew")
        self.btn60Secs: Button = Button(self, text="60s", command="")
        self.btn60Secs.grid(row=0, column=1, sticky="nsew")
        self.btn90Secs: Button = Button(self, text="90s", command="")
        self.btn90Secs.grid(row=0, column=2, sticky="nsew")
        self.btn120Secs: Button = Button(self, text="120s", command="")
        self.btn120Secs.grid(row=0, column=3, sticky="nsew")

        self.separator1: Label = Label(self, text="|", font=self.sepFont)
        self.separator1.grid(row=0, column=4, sticky="nsew")

        self.btnSpecials: Button = Button(self, text="Specials", command="")
        self.btnSpecials.grid(row=0, column=5, sticky="nsew")
        self.btnNumbers: Button = Button(self, text="Numbers", command="")
        self.btnNumbers.grid(row=0, column=6, sticky="nsew")

        self.separator2: Label = Label(self, text="|", font=self.sepFont)
        self.separator2.grid(row=0, column=7, sticky="nsew")

        self.btnProfile: Button = Button(self, text="Profile", command=self.switch_to_profile)
        self.btnProfile.grid(row=0, column=8, sticky="nsew")

        self.canvas: Canvas = Canvas(self, bg="blue")
        self.canvas.grid(row=1, column=0, columnspan=9, sticky="nsew")

        self.textCorrect: Label = Label(self, text="Correct: ")
        self.textCorrect.grid(row=2, column=1, columnspan=3, sticky="ew")
        self.textIncorrect: Label = Label(self, text="Incorrect: ")
        self.textIncorrect.grid(row=2, column=5, columnspan=2, sticky="ew")

    def switch_to_profile(self) -> None:
        self.ui.switch_frame(ProfileUI)
        return None


class ProfileUI(Frame):
    def __init__(self, master: Tk, ui: UI):
        super().__init__(master)
        self.ui: UI = ui

        self.btnGoTyping: Button = Button(self, text="Go Typing", command=self.switch_to_main)
        self.btnGoTyping.grid(row=0, column=0, sticky="nsew")

        self.btnLogout: Button = Button(self, text="Go Login", command=self.switch_to_login)
        self.btnLogout.grid(row=0, column=1, sticky="nsew")

        self.textWPM: Label = Label(self, text="Words Per Minute: ")
        self.textWPM.grid(row=1, column=0, sticky="nsew")

        self.textCorrectW: Label = Label(self, text="Total Correct Words: ")
        self.textCorrectW.grid(row=1, column=0, sticky="nsew")
        self.textIncorrectW: Label = Label(self, text="Total Incorrect Words: ")
        self.textIncorrectW.grid(row=2, column=0, sticky="nsew")

        self.textHistory: Label = Label()

    def switch_to_main(self) -> None:
        self.ui.switch_frame(MainUI)
        return None

    def switch_to_login(self) -> None:
        self.ui.switch_frame(LoginUI)
        return None


class LoginUI(Frame):
    def __init__(self, master: Tk, ui: UI):
        super().__init__(master)
        self.ui: UI = ui

        self.inputUser: Entry = Entry(self)
        self.inputUser.grid(row=0, column=0, sticky="nsew")
        self.inputPass: Entry = Entry(self)
        self.inputPass.grid(row=1, column=0, sticky="nsew")
        self.btnLogin: Button = Button(self, text="Log In", command=self.switch_to_main)
        self.btnLogin.grid(row=2, column=0, sticky="nsew")
        self.btnMore: Button = Button(self, text="Register", command=self.switch_to_register)
        self.btnMore.grid(row=3, column=0, sticky="nsew")

    def switch_to_main(self) -> None:
        self.ui.switch_frame(MainUI)
        return None

    def switch_to_register(self) -> None:
        self.ui.switch_frame(RegisterUI)
        return None


class RegisterUI(Frame):
    def __init__(self, master: Tk, ui: UI):
        super().__init__(master)
        self.ui: UI = ui

        self.inputEmail: Entry = Entry(self)
        self.inputEmail.grid(row=0, column=0, sticky="nsew")
        self.inputName: Entry = Entry(self)
        self.inputName.grid(row=1, column=0, sticky="nsew")
        self.inputPassword: Entry = Entry(self)
        self.inputPassword.grid(row=2, column=0, sticky="nsew")
        self.btnRegister: Button = Button(self, text="Register", command=self.switch_to_main)
        self.btnRegister.grid(row=3, column=0, sticky="nsew")
        self.btnMore: Button = Button()

    def switch_to_main(self) -> None:
        self.ui.switch_frame(MainUI)
        return None
