from tkinter import Frame, Tk, Button, Entry, Label, Event, messagebox, END
from json import dump, load
from hashlib import sha256
from typing import cast


class RegisterUI(Frame):
    def __init__(self, master: Tk, ui):
        super().__init__(master)
        self.ui = ui
        self.hashObject = sha256()
        self.inputEmail: Entry = cast(Entry, None)
        self.inputUser: Entry = cast(Entry, None)
        self.inputPass: Entry = cast(Entry, None)
        self.bindings: list = [
            ("<Return>", self.check_register_form),
        ]
        self.bindIds: list = []
        self.configure_layout()
        self.create_form()

    def configure_layout(self) -> None:
        """Configure the main layout and the grid to be used"""
        self.config(bg=self.ui.styles.get("background_color"))
        self.grid_columnconfigure(tuple(range(1)), weight=1)
        self.grid(sticky="nsew", padx=10, pady=10)
        return None

    def on_frame_activation(self) -> None:
        """Set the frame's key bindings and save them for later use"""
        for bind, callback in self.bindings:
            bindId = self.master.bind(bind, callback)
            self.bindIds.append((bind, bindId))
        return None

    def on_frame_deactivation(self) -> None:
        """Unset the frame's key bindings and clear the list"""
        for seq, bId in self.bindIds:
            self.master.unbind(seq, bId)
        self.bindIds = []
        return None

    def create_form(self) -> None:
        """Create and configure the form necessary to register"""
        formFrame: Frame = Frame(self, bg=self.ui.styles.get("background_color"), relief="flat", padx=40, pady=60)
        formFrame.grid(row=0, column=0, sticky="nsew")
        formFrame.grid_columnconfigure(tuple(range(1)), weight=1)
        emailLabel: Label = Label(formFrame, text="Email", font=self.ui.styles.get("button_font"),
                                  fg=self.ui.styles.get("label_font_color"), bg=self.ui.styles.get("background_color"))
        emailLabel.grid(row=0, column=0, sticky="nsew", padx=40, pady=(10, 5))
        self.inputEmail: Entry = Entry(formFrame, font=self.ui.styles.get("button_font"))
        self.inputEmail.grid(row=1, column=0, sticky="n", padx=40, pady=20)
        userLabel: Label = Label(formFrame, text="Username", font=self.ui.styles.get("button_font"),
                                 fg=self.ui.styles.get("label_font_color"), bg=self.ui.styles.get("background_color"))
        userLabel.grid(row=2, column=0, sticky="nsew", padx=40, pady=(10, 5))
        self.inputUser: Entry = Entry(formFrame, font=self.ui.styles.get("button_font"))
        self.inputUser.grid(row=3, column=0, sticky="n", padx=40, pady=20)
        passLabel: Label = Label(formFrame, text="Password", font=self.ui.styles.get("button_font"),
                                 fg=self.ui.styles.get("label_font_color"), bg=self.ui.styles.get("background_color"))
        passLabel.grid(row=4, column=0, sticky="nsew", padx=40, pady=(10, 5))
        self.inputPass: Entry = Entry(formFrame, font=self.ui.styles.get("button_font"))
        self.inputPass.grid(row=5, column=0, sticky="n", padx=40, pady=20)
        buttonsStyles: dict = {
            "bg": self.ui.styles.get("background_color"),
            "fg": self.ui.styles.get("button_font_color"),
            "font": self.ui.styles.get("button_font"),
            "relief": "flat",
            "activebackground": self.ui.styles.get("button_active_color"),
            "padx": 10,
            "pady": 5,
            "borderwidth": 0,
            "cursor": "center_ptr"
        }
        registerBtn: Button = Button(formFrame, text="Register", command=self.check_register_form, **buttonsStyles)
        registerBtn.grid(row=6, column=0, sticky="n", padx=40, pady=(10, 5))
        setattr(self, "registerButton", registerBtn)
        return None

    def switch_to_main(self) -> None:
        """Switch to main frame from the register frame"""
        self.ui.switch_frame(frameClassName="MainUI")
        return None

    def check_register_form(self, event: Event = None) -> None:
        """Check and validate the form inputs in order to create new access credentials"""
        print(f"Check register form using: {event.keysym if event is not None else 'Button'}")
        email = self.inputEmail.get()
        username = self.inputUser.get()
        password = self.inputPass.get()
        if len(email) == 0 or len(username) == 0 or len(password) == 0:
            messagebox.showerror(title="Error registering", message="Don't leave blank inputs. Try again!")
            return None
        self.save_all_credentials(email, username, password)
        messagebox.showinfo(title="Successful registering", message="Credentials successfully saved!")
        self.clear_form()
        return None

    def save_all_credentials(self, email: str, username: str, password: str) -> None:
        """Get the saved credentials, append the new ones and write them all back"""
        fileName: str = "local_users_credentials.json"
        try:
            with open(file=fileName, mode="r") as jsonFile:
                data: dict = load(jsonFile)
        except FileNotFoundError as e:
            print(e)
            data: dict = {"users": []}
        credentials: dict = {
            "email": email,
            "username": username,
            "password": self.hash_password(password).hex()
        }
        data["users"].append(credentials)
        with open(file=fileName, mode="w") as jsonFile:
            dump(data, jsonFile, indent=4)
        return None

    def hash_password(self, password: str) -> bytes:
        """Convert the received password into a hash using the SHA256 algorithm and return it"""
        self.hashObject.update(password.encode("utf-8"))
        return self.hashObject.digest()

    def clear_form(self) -> None:
        """Clear the form inputs"""
        self.inputEmail.delete(0, END)
        self.inputUser.delete(0, END)
        self.inputPass.delete(0, END)
        return None
