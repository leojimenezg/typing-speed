from tkinter import Frame, Tk, Button, Entry, Label, Event, END, messagebox
from hashlib import sha256
from typing import cast
from json import load


class LoginUI(Frame):
    def __init__(self, master: Tk, ui):
        super().__init__(master)
        self.ui = ui
        self.input_username: Entry = cast(Entry, None)
        self.input_password: Entry = cast(Entry, None)
        self.bindings: list = [
            ("<Return>", self.check_login_form),
        ]
        self.binds_id: list = []
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
            self.binds_id.append((bind, bindId))
        return None

    def on_frame_deactivation(self) -> None:
        """Unset the frame's key bindings and clear the list"""
        for seq, bId in self.binds_id:
            self.master.unbind(seq, bId)
        self.binds_id = []
        return None

    def create_form(self) -> None:
        """Create and configure the form necessary to login"""
        form_frame: Frame = Frame(
            self,
            bg=self.ui.styles.get("background_color"),
            relief="flat",
            padx=40,
            pady=60
        )
        form_frame.grid(row=0, column=0, sticky="nsew")
        form_frame.grid_columnconfigure(tuple(range(1)), weight=1)
        user_label: Label = Label(
            form_frame,
            text="Username",
            font=self.ui.styles.get("button_font"),
            fg=self.ui.styles.get("label_font_color"),
            bg=self.ui.styles.get("background_color")
        )
        user_label.grid(row=0, column=0, sticky="nsew", padx=40, pady=(10, 5))
        self.input_username: Entry = Entry(
            form_frame,
            font=self.ui.styles.get("button_font")
        )
        self.input_username.grid(row=1, column=0, sticky="n", padx=40, pady=20)
        password_label: Label = Label(
            form_frame,
            text="Password",
            font=self.ui.styles.get("button_font"),
            fg=self.ui.styles.get("label_font_color"),
            bg=self.ui.styles.get("background_color")
        )
        password_label.grid(
            row=2, column=0, sticky="nsew", padx=40, pady=(10, 5)
        )
        self.input_password: Entry = Entry(
            form_frame,
            font=self.ui.styles.get("button_font")
        )
        self.input_password.grid(row=3, column=0, sticky="n", padx=40, pady=20)
        button_styles: dict = {
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
        button_options: list = [
            ("  Login   ", self.check_login_form, 4),
            ("Register", self.switch_to_register, 5)
        ]
        for text, command, row in button_options:
            btn: Button = Button(
                form_frame,
                text=text,
                command=command,
                **button_styles
            )
            btn.grid(row=row, column=0, sticky="n", padx=40, pady=(10, 5))
            setattr(self, f"{text}Button", btn)
        return None

    def switch_to_main(self) -> None:
        """Switch to main frame from the login frame"""
        self.ui.switch_frame(frameClassName="MainUI")
        return None

    def switch_to_register(self) -> None:
        """Switch to register frame from the login frame"""
        self.ui.switch_frame(frameClassName="RegisterUI")
        return None

    def check_login_form(self, event: Event = None) -> None:
        """Check the form inputs to validate the credentials"""
        user: str = self.input_username.get()
        password: str = self.input_password.get()
        if len(user) == 0 or len(password) == 0:
            messagebox.showerror(
                title="Error logging in",
                message="Don't leave blank inputs. Try again!"
            )
            return None
        data: dict = self.get_all_credentials()
        if len(data["users"]) == 0:
            messagebox.showerror(
                title="Missing data",
                message="There are not any credentials saved. Try registering!"
            )
            return None
        credentials = None
        for info in data["users"]:
            if info["username"] == user:
                credentials = info
                break
        if credentials is None:
            messagebox.showerror(
                title="Incorrect credentials",
                message="The user does not exist or is incorrect. Check again!"
            )
            self.clear_form()
            return None
        hashedPass = self.hash_password(password)
        if credentials["password"] != hashedPass:
            messagebox.showerror(
                title="Incorrect credentials",
                message="The introduced password is incorrect. Check again!"
            )
            return None
        messagebox.showinfo(
            title="Successful login",
            message="The introduced credentials are valid!"
        )
        self.switch_to_main()
        return None

    @staticmethod
    def get_all_credentials() -> dict:
        """Get all the credentials saved in the json file"""
        file_name: str = "src/local_users_credentials.json"
        try:
            with open(file=file_name, mode="r") as jsonFile:
                data: dict = load(jsonFile)
        except FileNotFoundError as e:
            print(e)
            data: dict = {"users": []}
        return data

    @staticmethod
    def hash_password(password: str) -> str:
        """Return the received password as a SHA256 hash"""
        return sha256(password.encode("utf-8")).hexdigest()

    def clear_form(self) -> None:
        """Clear the form inputs"""
        self.input_username.delete(0, END)
        self.input_password.delete(0, END)
        return None
