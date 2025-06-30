from tkinter import Frame, Tk, Button, Label, Text, END, Event
from typing import cast


class ProfileUI(Frame):
    def __init__(self, master: Tk, ui):
        super().__init__(master)
        self.ui = ui
        self.text_history: Text = cast(Text, None)
        self.wpm30secs: Label = cast(Label, None)
        self.wpm60secs: Label = cast(Label, None)
        self.wpm90secs: Label = cast(Label, None)
        self.wpm120secs: Label = cast(Label, None)
        self.bindings: list = []
        self.bind_ids: list = []
        self.configure_layout()
        self.create_top_bar()
        self.create_metric_displays()

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
            self.bind_ids.append((bind, bindId))
        return None

    def on_frame_deactivation(self) -> None:
        """Unset the frame's key bindings and clear the list"""
        for seq, bId in self.bind_ids:
            self.master.unbind(seq, bId)
        self.bind_ids = []
        return None

    def create_top_bar(self) -> None:
        """Create and configure the top bar to show the buttons"""
        top_bar: Frame = Frame(
            self,
            bg=self.ui.styles.get("background_color"),
            relief="flat"
        )
        top_bar.grid(row=0, column=0, sticky="ew", pady=20)
        top_bar.grid_columnconfigure(tuple(range(7)), weight=1)
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
        option_btn_config: list = [
            ("Typing", self.switch_to_main, 0),
            ("Login", self.switch_to_login, 4),
            ("Logout", self.switch_to_login, 6)
        ]
        for text, command, col in option_btn_config:
            btn: Button = Button(
                top_bar,
                text=text,
                command=command,
                **button_styles
            )
            btn.grid(row=0, column=col, sticky="ew", padx=2, pady=2)
            setattr(self, f"btn{text}", btn)
        sep1: Frame = Frame(
            top_bar, bg=self.ui.styles.get("background_color"), width=2
        )
        sep1.grid(row=0, column=1, columnspan=3, sticky="nsew", padx=5)
        setattr(self, "separator1", sep1)
        sep2: Frame = Frame(
            top_bar, bg=self.ui.styles.get("background_color"), width=2
        )
        sep2.grid(row=0, column=5, sticky="nsew", padx=5)
        setattr(self, "separator2", sep2)
        return None

    def create_metric_displays(self) -> None:
        """Create and configure all the widgets to show the metrics"""
        metric_frame: Frame = Frame(
            self,
            bg=self.ui.styles.get("background_color"),
            relief="flat",
            bd=1
        )
        metric_frame.grid(row=1, column=0, sticky="ew", pady=20)
        metric_frame.grid_columnconfigure(tuple(range(5)), weight=1)
        label_styles: dict = {
            "font": self.ui.styles.get("body_label_font"),
            "fg": self.ui.styles.get("label_font_color"),
            "bg": self.ui.styles.get("background_color")
        }
        label_config: list = [
            ("30s", 0),
            ("60s", 1),
            ("90s", 2),
            ("120s", 3)
        ]
        label: Label = Label(
            metric_frame,
            text="Words Per Time",
            font=self.ui.styles.get("title_label_font"),
            fg=self.ui.styles.get("label_font_color"),
            bg=self.ui.styles.get("background_color")
        )
        label.grid(row=0, column=0, sticky="ew", columnspan=4, padx=10, pady=5)
        setattr(self, "labelWPT", label)
        for text, column in label_config:
            label: Label = Label(metric_frame, text=text, **label_styles)
            label.grid(row=1, column=column, sticky="nsew", padx=10, pady=5)
            setattr(self, f"{text}Label", label)
        self.wpm30secs: Label = Label(
            metric_frame, text="to be appeared", **label_styles
        )
        self.wpm30secs.grid(row=2, column=0, sticky="new", padx=10, pady=5)
        self.wpm60secs: Label = Label(
            metric_frame, text="to be appeared", **label_styles
        )
        self.wpm60secs.grid(row=2, column=1, sticky="new", padx=10, pady=5)
        self.wpm90secs: Label = Label(
            metric_frame, text="to be appeared", **label_styles
        )
        self.wpm90secs.grid(row=2, column=2, sticky="new", padx=10, pady=5)
        self.wpm120secs: Label = Label(
            metric_frame, text="to be appeared", **label_styles
        )
        self.wpm120secs.grid(row=2, column=3, sticky="new", padx=10, pady=5)
        label: Label = Label(
            metric_frame,
            text="History",
            font=self.ui.styles.get("title_label_font"),
            fg=self.ui.styles.get("label_font_color"),
            bg=self.ui.styles.get("background_color")
        )
        label.grid(row=0, column=4, sticky="ew", padx=10, pady=5)
        setattr(self, "labelHistory", label)
        self.text_history: Text = Text(
            metric_frame,
            bg=self.ui.styles.get("background_color"),
            height=20,
            width=15,
            relief="sunken",
            fg=self.ui.styles.get("label_font_color"),
            wrap="word",
            font=self.ui.styles.get("body_label_font"),
            highlightthickness=0,
            bd=1
        )
        self.text_history.grid(
            row=1, column=4, sticky="new", rowspan=2, padx=10, pady=5
        )
        self.text_history.insert(
            END, "Your typing session history will appear here."
        )
        self.text_history.config(state="disabled")
        return None

    def switch_to_main(self) -> None:
        """Switch to main frame from the profile frame"""
        self.ui.switch_frame(frameClassName="MainUI")
        return None

    def switch_to_login(self) -> None:
        """Switch to login frame from the profile frame"""
        self.ui.switch_frame(frameClassName="LoginUI")
        return None
