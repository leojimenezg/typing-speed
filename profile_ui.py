from tkinter import Frame, Tk, Button, Label, Text, END, Event
from typing import cast


class ProfileUI(Frame):
    def __init__(self, master: Tk, ui):
        super().__init__(master)
        self.ui = ui
        self.textHistory: Text = cast(Text, None)
        self.wpm30secs: Label = cast(Label, None)
        self.wpm60secs: Label = cast(Label, None)
        self.wpm90secs: Label = cast(Label, None)
        self.wpm120secs: Label = cast(Label, None)
        self.bindings: list = [
            ("<Return>", self.test),
        ]
        self.bindIds: list = []
        self.configure_layout()
        self.create_top_bar()
        self.create_metric_displays()

    def test(self, event: Event):
        print(f"Bind worked from profileUI {event.keysym}")
        return None

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

    def create_top_bar(self) -> None:
        """Create and configure the top bar to show the buttons"""
        topBar: Frame = Frame(self, bg=self.ui.styles.get("background_color"), relief="flat")
        topBar.grid(row=0, column=0, sticky="ew", pady=20)
        topBar.grid_columnconfigure(tuple(range(7)), weight=1)
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
        optBtnConfigs: list = [
            ("Typing", self.switch_to_main, 0),
            ("Login", self.switch_to_login, 4),
            ("Logout", self.switch_to_login, 6)
        ]
        for text, command, col in optBtnConfigs:
            btn: Button = Button(topBar, text=text, command=command, **buttonsStyles)
            btn.grid(row=0, column=col, sticky="ew", padx=2, pady=2)
            setattr(self, f"btn{text}", btn)
        sep1: Frame = Frame(topBar, bg=self.ui.styles.get("background_color"), width=2)
        sep1.grid(row=0, column=1, columnspan=3, sticky="nsew", padx=5)
        setattr(self, "separator1", sep1)
        sep2: Frame = Frame(topBar, bg=self.ui.styles.get("background_color"), width=2)
        sep2.grid(row=0, column=5, sticky="nsew", padx=5)
        setattr(self, "separator2", sep2)
        return None

    def create_metric_displays(self) -> None:
        """Create and configure all the widgets to show the metrics"""
        metricFrame: Frame = Frame(self, bg=self.ui.styles.get("background_color"), relief="flat", bd=1)
        metricFrame.grid(row=1, column=0, sticky="ew", pady=20)
        metricFrame.grid_columnconfigure(tuple(range(5)), weight=1)
        labelStyles: dict = {
            "font": self.ui.styles.get("body_label_font"),
            "fg": self.ui.styles.get("label_font_color"),
            "bg": self.ui.styles.get("background_color")
        }
        labelConfigs: list = [
            ("30s", 0),
            ("60s", 1),
            ("90s", 2),
            ("120s", 3)
        ]
        label: Label = Label(metricFrame, text="Words Per Time", font=self.ui.styles.get("title_label_font"),
                             fg=self.ui.styles.get("label_font_color"), bg=self.ui.styles.get("background_color"))
        label.grid(row=0, column=0, sticky="ew", columnspan=4, padx=10, pady=5)
        setattr(self, "labelWPT", label)
        for text, column in labelConfigs:
            label: Label = Label(metricFrame, text=text, **labelStyles)
            label.grid(row=1, column=column, sticky="nsew", padx=10, pady=5)
            setattr(self, f"{text}Label", label)
        self.wpm30secs: Label = Label(metricFrame, text="to be appeared", **labelStyles)
        self.wpm30secs.grid(row=2, column=0, sticky="new", padx=10, pady=5)
        self.wpm60secs: Label = Label(metricFrame, text="to be appeared", **labelStyles)
        self.wpm60secs.grid(row=2, column=1, sticky="new", padx=10, pady=5)
        self.wpm90secs: Label = Label(metricFrame, text="to be appeared", **labelStyles)
        self.wpm90secs.grid(row=2, column=2, sticky="new", padx=10, pady=5)
        self.wpm120secs: Label = Label(metricFrame, text="to be appeared", **labelStyles)
        self.wpm120secs.grid(row=2, column=3, sticky="new", padx=10, pady=5)
        label: Label = Label(metricFrame, text="History", font=self.ui.styles.get("title_label_font"),
                             fg=self.ui.styles.get("label_font_color"), bg=self.ui.styles.get("background_color"))
        label.grid(row=0, column=4, sticky="ew", padx=10, pady=5)
        setattr(self, "labelHistory", label)
        self.textHistory: Text = Text(metricFrame, bg=self.ui.styles.get("background_color"), height=20, width=15,
                                      relief="sunken", fg=self.ui.styles.get("label_font_color"), wrap="word",
                                      font=self.ui.styles.get("body_label_font"), highlightthickness=0, bd=1)
        self.textHistory.grid(row=1, column=4, sticky="new", rowspan=2, padx=10, pady=5)
        self.textHistory.insert(END, "Your typing session history will appear here.")
        self.textHistory.config(state="disabled")
        return None

    def switch_to_main(self) -> None:
        """Switch to main frame from the profile frame"""
        self.ui.switch_frame(frameClassName="MainUI")
        return None

    def switch_to_login(self) -> None:
        """Switch to login frame from the profile frame"""
        self.ui.switch_frame(frameClassName="LoginUI")
        return None
