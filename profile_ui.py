from tkinter import Frame, Tk, Button, Label


class ProfileUI(Frame):
    def __init__(self, master: Tk, ui):
        super().__init__(master)

        # Variables to be used
        self.ui = ui

        self.configure_layout()
        # Button to go back to Main
        self.btnGoTyping = Button(self, text="Go Typing", command=self.switch_to_main,
                                  bg="#4a7abc", fg="black", font=("Arial", 14, "bold"), relief="flat")
        self.btnGoTyping.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        # Button LogOut
        self.btnLogout = Button(self, text="Go Login", command=self.switch_to_login,
                                bg="#e74c3c", fg="black", font=("Arial", 14, "bold"), relief="flat")
        self.btnLogout.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        # Different metrics indicators
        self.textWPM = Label(self, text="Words Per Minute: 0",
                             font=("Arial", 12, "normal"), anchor="w", padx=10, pady=5)
        self.textWPM.grid(row=1, column=0, columnspan=2, sticky="ew", pady=2)
        self.textCorrectW = Label(self, text="Total Correct Words: 0",
                                  font=("Arial", 12, "normal"), anchor="w", padx=10, pady=5)
        self.textCorrectW.grid(row=2, column=0, columnspan=2, sticky="ew", pady=2)
        self.textIncorrectW = Label(self, text="Total Incorrect Words: 0",
                                    font=("Arial", 12, "normal"), anchor="w", padx=10, pady=5)
        self.textIncorrectW.grid(row=3, column=0, columnspan=2, sticky="ew", pady=2)
        # History section with frame
        historyFrame = Frame(self, bd=2, relief="groove", bg="#f5f5f5")
        historyFrame.grid(row=4, column=0, columnspan=2, sticky="nsew", pady=10)
        historyFrame.grid_columnconfigure(0, weight=1)
        historyFrame.grid_rowconfigure(0, weight=1)

        self.textHistory = Label(historyFrame, text="History will appear here",
                                 bg="#f5f5f5", fg="black", anchor="nw", justify="left", padx=10, pady=10)
        self.textHistory.grid(row=0, column=0, sticky="nsew")

    def configure_layout(self) -> None:
        """Configure the main layout and the grid to be used"""
        self.grid_columnconfigure(tuple(range(2)), weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid(sticky="nsew", padx=10, pady=10)
        return None

    def switch_to_main(self) -> None:
        """Switch to main frame from the profile frame"""
        self.ui.switch_frame(frameClassName="MainUI")
        return None

    def switch_to_login(self) -> None:
        """Switch to login frame from the profile frame"""
        self.ui.switch_frame(frameClassName="LoginUI")
        return None
