from tkinter import Frame, Tk, Button, Entry, Label, Event, messagebox, END
from json import dump, load
from hashlib import sha256
from typing import cast


class RegisterUI(Frame):
    def __init__(self, master: Tk, ui):
        super().__init__(master)
        self.ui = ui
        self.input_email: Entry = cast(Entry, None)
        self.input_user: Entry = cast(Entry, None)
        self.input_password: Entry = cast(Entry, None)
        self.bindings: list = [
            ("<Return>", self.check_register_form),
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
        """Create and configure the form necessary to register"""
        form_frame: Frame = Frame(
            self,
            bg=self.ui.styles.get("background_color"),
            relief="flat",
            padx=40,
            pady=60
        )
        form_frame.grid(row=0, column=0, sticky="nsew")
        form_frame.grid_columnconfigure(tuple(range(1)), weight=1)
        email_label: Label = Label(
            form_frame,
            text="Email",
            font=self.ui.styles.get("button_font"),
            fg=self.ui.styles.get("label_font_color"),
            bg=self.ui.styles.get("background_color")
        )
        email_label.grid(row=0, column=0, sticky="nsew", padx=40, pady=(10, 5))
        self.input_email: Entry = Entry(
            form_frame,
            font=self.ui.styles.get("button_font")
        )
        self.input_email.grid(row=1, column=0, sticky="n", padx=40, pady=20)
        user_label: Label = Label(
            form_frame,
            text="Username",
            font=self.ui.styles.get("button_font"),
            fg=self.ui.styles.get("label_font_color"),
            bg=self.ui.styles.get("background_color")
        )
        user_label.grid(row=2, column=0, sticky="nsew", padx=40, pady=(10, 5))
        self.input_user: Entry = Entry(
            form_frame,
            font=self.ui.styles.get("button_font")
        )
        self.input_user.grid(row=3, column=0, sticky="n", padx=40, pady=20)
        password_label: Label = Label(
            form_frame,
            text="Password",
            font=self.ui.styles.get("button_font"),
            fg=self.ui.styles.get("label_font_color"),
            bg=self.ui.styles.get("background_color")
        )
        password_label.grid(
            row=4, column=0, sticky="nsew", padx=40, pady=(10, 5)
        )
        self.input_password: Entry = Entry(
            form_frame,
            font=self.ui.styles.get("button_font")
        )
        self.input_password.grid(row=5, column=0, sticky="n", padx=40, pady=20)
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
        register_btn: Button = Button(
            form_frame,
            text="Register",
            command=self.check_register_form,
            **button_styles
        )
        register_btn.grid(row=6, column=0, sticky="n", padx=40, pady=(10, 5))
        setattr(self, "registerButton", register_btn)
        return None

    def switch_to_main(self) -> None:
        """Switch to main frame from the register frame"""
        self.ui.switch_frame(frameClassName="MainUI")
        return None

    def check_register_form(self, event: Event = None) -> None:
        """Check and validate the form inputs to create access credentials"""
        email = self.input_email.get()
        username = self.input_user.get()
        password = self.input_password.get()
        if len(email) == 0 or len(username) == 0 or len(password) == 0:
            messagebox.showerror(
                title="Error registering",
                message="Don't leave blank inputs. Try again!"
            )
            return None
        self.save_credentials(email, username, password)
        messagebox.showinfo(
            title="Successful registering",
            message="Credentials successfully saved!"
        )
        self.clear_form()
        self.switch_to_main()
        return None

    def save_credentials(self, email: str, user: str, password: str) -> None:
        """Save the credentials old and new ones"""
        file_name: str = "src/local_users_credentials.json"
        try:
            with open(file=file_name, mode="r") as file:
                data: dict = load(file)
        except FileNotFoundError as e:
            print(e)
            data: dict = {"users": []}
        credentials: dict = {
            "email": email,
            "username": user,
            "password": self.hash_password(password)
        }
        data["users"].append(credentials)
        with open(file=file_name, mode="w") as json:
            dump(data, json, indent=4)
        return None

    @staticmethod
    def hash_password(password: str) -> str:
        """Return the received password as a SHA256 hash"""
        return sha256(password.encode("utf-8")).hexdigest()

    def clear_form(self) -> None:
        """Clear the form inputs"""
        self.input_email.delete(0, END)
        self.input_user.delete(0, END)
        self.input_password.delete(0, END)
        return None
