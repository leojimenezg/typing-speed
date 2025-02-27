from tkinter import Frame, Tk, Button, Entry


class LoginUI(Frame):
    def __init__(self, master: Tk, ui):
        super().__init__(master)

        # Variables to be used
        self.ui = ui

        self.configure_layout()

        # User entries
        self.inputUser: Entry = Entry(self)
        self.inputUser.grid(row=0, column=0, sticky="nsew")
        self.inputPass: Entry = Entry(self)
        self.inputPass.grid(row=1, column=0, sticky="nsew")
        # Options buttons
        self.btnLogin: Button = Button(self, text="Log In", command=self.switch_to_main)
        self.btnLogin.grid(row=2, column=0, sticky="nsew")
        self.btnMore: Button = Button(self, text="Register", command=self.switch_to_register)
        self.btnMore.grid(row=3, column=0, sticky="nsew")

    def configure_layout(self) -> None:
        """Configure the main layout and the grid to be used"""
        self.grid_columnconfigure(tuple(range(1)), weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid(sticky="nsew", padx=10, pady=10)
        return None

    def switch_to_main(self) -> None:
        """Switch to main frame from the login frame"""
        self.ui.switch_frame(frameClassName="MainUI")
        return None

    def switch_to_register(self) -> None:
        """Switch to register frame from the login frame"""
        self.ui.switch_frame(frameClassName="RegisterUI")
        return None
