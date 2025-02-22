from tkinter import Tk, Button, Canvas, Label, Entry, Frame
from typing import cast


class UI:
    def __init__(self, root: Tk):
        self.root: Tk = root
        self.currentFrame: Frame = cast(Frame, None)

    def switch_frame(self, frameClass) -> None:
        if self.currentFrame is not None:
            self.currentFrame.destroy()

        self.currentFrame = frameClass(self.root, self)
        self.currentFrame.pack(fill="both", expand=True)

        return None


class MainUI(Frame):
    def __init__(self, root: Tk, ui: UI):
        super().__init__(root)
        self.ui: UI = ui

        self.btnProfile: Button = Button()
        self.btnTime: Button = Button()
        self.btnSpecialChars: Button = Button()
        self.btnLang: Button = Button()
        self.btnNumbers: Button = Button()

        self.canvas: Canvas = Canvas()

        self.textCorrect: Label = Label()
        self.textIncorrect: Label = Label()

    def switch_to_profile(self) -> None:
        self.ui.switch_frame(ProfileUI)
        return None


class ProfileUI(Frame):
    def __init__(self, root: Tk, ui: UI):
        super().__init__(root)
        self.ui: UI = ui

        self.btnTheme: Button = Button()
        self.btnGoTyping: Button = Button()
        self.btnAccountOpts: Button = Button()

        self.textWPM: Label = Label()
        self.textCorrectW: Label = Label()
        self.textIncorrectW: Label = Label()

        self.textHistory: Label = Label()

    def switch_to_main(self) -> None:
        self.ui.switch_frame(MainUI)
        return None

    def switch_to_login(self) -> None:
        self.ui.switch_frame(LoginUI)
        return None


class LoginUI(Frame):
    def __init__(self, root: Tk, ui: UI):
        super().__init__(root)
        self.ui: UI = ui

        self.inputUser: Entry = Entry()
        self.inputPass: Entry = Entry()

        self.btnLogin: Button = Button()
        self.btnMore: Button = Button()

    def switch_to_main(self) -> None:
        self.ui.switch_frame(MainUI)
        return None

    def switch_to_register(self) -> None:
        self.ui.switch_frame(RegisterUI)
        return None


class RegisterUI(Frame):
    def __init__(self, root: Tk, ui: UI):
        super().__init__(root)
        self.ui: UI = ui

        self.inputEmail: Entry = Entry()
        self.inputName: Entry = Entry()
        self.inputPassword: Entry = Entry()

        self.btnRegister: Button = Button()
        self.btnMore: Button = Button()

    def switch_to_main(self) -> None:
        self.ui.switch_frame(MainUI)
        return None
