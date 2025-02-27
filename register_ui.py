from tkinter import Frame, Tk, Button, Entry


class RegisterUI(Frame):
    def __init__(self, master: Tk, ui):
        super().__init__(master)

        # Variables to be used
        self.ui = ui

        self.configure_layout()

        # User entries
        self.inputEmail: Entry = Entry(self)
        self.inputEmail.grid(row=0, column=0, sticky="nsew")
        self.inputName: Entry = Entry(self)
        self.inputName.grid(row=1, column=0, sticky="nsew")
        self.inputPassword: Entry = Entry(self)
        self.inputPassword.grid(row=2, column=0, sticky="nsew")
        # Options buttons
        self.btnRegister: Button = Button(self, text="Register", command=self.switch_to_main)
        self.btnRegister.grid(row=3, column=0, sticky="nsew")
        self.btnMore: Button = Button()

    def configure_layout(self) -> None:
        """Configure the main layout and the grid to be used"""
        self.grid_columnconfigure(tuple(range(1)), weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid(sticky="nsew", padx=10, pady=10)
        return None

    def switch_to_main(self) -> None:
        """Switch to main frame from the register frame"""
        self.ui.switch_frame(frameClassName="MainUI")
        return None
