from tkinter import Frame, Tk, Canvas, Label, Button
from threading import Thread
from typing import cast
import time


class MainUI(Frame):
    def __init__(self, master: Tk, ui):
        super().__init__(master)

        self.ui = ui
        self.canvas: Canvas = cast(Canvas, None)
        self.textCorrect: Label = cast(Label, None)
        self.textIncorrect: Label = cast(Label, None)
        self.textTimer: Label = cast(Label, None)
        self.seconds: int = 0
        self.numbers: bool = False
        self.specials: bool = False
        self.test_on: bool = False
        self.timer_on: bool = False

        self.configure_layout()
        self.create_top_bar()
        self.create_canvas()
        self.create_bottom_bar()

    def configure_layout(self) -> None:
        """Configure the main layout and the grid to be used"""
        self.config(bg=self.ui.styles.get("background_color"))
        self.grid_columnconfigure(tuple(range(9)), weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid(sticky="nsew", padx=10, pady=10)

        return None

    def create_top_bar(self) -> None:
        """Create the top navigation bar with the necessary buttons and separators"""
        topBar: Frame = Frame(self, bg=self.ui.styles.get("background_color"), relief="flat", bd=1)
        topBar.grid(row=0, column=0, columnspan=9, sticky="ew", pady=20)
        topBar.grid_columnconfigure(tuple(range(9)), weight=1)

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

        timeBtnConfigs: list = [
            ("30s", self.set_time_variable, 0, 30),
            ("60s", self.set_time_variable, 1, 60),
            ("90s", self.set_time_variable, 2, 90),
            ("120s", self.set_time_variable, 3, 120)
        ]

        for text, command, col, secs in timeBtnConfigs:
            btn: Button = Button(topBar, text=text, command=lambda t=secs, cmd=command: cmd(t), **buttonsStyles)
            btn.grid(row=0, column=col, sticky="nsew", padx=2, pady=2)
            setattr(self, f"btn{text}", btn)

        sep1: Frame = Frame(topBar, bg=self.ui.styles.get("background_color"), width=2)
        sep1.grid(row=0, column=4, sticky="ns", padx=5)
        setattr(self, "separator1", sep1)

        extraBtnConfigs: list = [
            ("Specials", self.set_specials_variable, 5),
            ("Numbers", self.set_numbers_variable, 6)
        ]

        for text, command, col in extraBtnConfigs:
            btn: Button = Button(topBar, text=text, command=command, **buttonsStyles)
            btn.grid(row=0, column=col, sticky="nsew", padx=2, pady=2)
            setattr(self, f"btn{text}", btn)

        sep2: Frame = Frame(topBar, bg=self.ui.styles.get("background_color"), width=2)
        sep2.grid(row=0, column=7, sticky="ns", padx=5)
        setattr(self, f"separator2", sep2)

        profile: Button = Button(topBar, text="Profile", command=self.switch_to_profile, **buttonsStyles)
        profile.grid(row=0, column=8, sticky="nsew", padx=2, pady=2)
        setattr(self, "btnProfile", profile)

        return None

    def create_canvas(self) -> None:
        """Create and configure the canvas to show the corresponding text"""
        canvasFrame: Frame = Frame(self, bg=self.ui.styles.get("background_color"), relief="sunken")
        canvasFrame.grid(row=1, column=0, columnspan=9, sticky="nsew", pady=20)
        canvasFrame.grid_columnconfigure(0, weight=1)
        canvasFrame.grid_rowconfigure(0, weight=1)

        self.canvas: Canvas = Canvas(canvasFrame, bg=self.ui.styles.get("canvas_color"), highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        return None

    def create_bottom_bar(self) -> None:
        """Create and configure the bottom bar to show few metrics"""
        statusBar: Frame = Frame(self, bg=self.ui.styles.get("background_color"), relief="flat", bd=1)
        statusBar.grid(row=2, column=0, columnspan=9, sticky="ew", pady=20)

        for i in range(0, 9):
            statusBar.grid_columnconfigure(i, weight=1)

        metricStyle: dict = {
            "font": self.ui.styles.get("button_font"),
            "bg": self.ui.styles.get("background_color"),
            "padx": 10,
            "pady": 20
        }

        self.textCorrect: Label = Label(statusBar, text="Correct: 0", fg="#27ae60", anchor="w", **metricStyle)
        self.textCorrect.grid(row=0, column=0, columnspan=3, sticky="w")
        self.textTimer: Label = Label(statusBar, text="Time: 0", fg="#000000", **metricStyle)
        self.textTimer.grid(row=0, column=3, columnspan=3, sticky="ns")
        self.textIncorrect: Label = Label(statusBar, text="Incorrect: 0", fg="#c0392b", anchor="e", **metricStyle)
        self.textIncorrect.grid(row=0, column=6, columnspan=3, sticky="e")

        return None

    def switch_to_profile(self) -> None:
        """Switch to profile frame from the main frame"""
        self.ui.switch_frame(frameClassName="ProfileUI")
        return None

    def set_time_variable(self, seconds: int) -> None:
        """Change the time used for the tests"""
        self.seconds = seconds
        self.textTimer.config(text=f"Time: {self.seconds}s")
        self.start_timer()

        return None

    def set_numbers_variable(self) -> None:
        """Change the numbers variable to enable or disable them"""
        self.numbers = not self.numbers
        print(f"Numbers are {self.numbers}")
        return None

    def set_specials_variable(self) -> None:
        """Change the specials variable to enable or disable them"""
        self.specials = not self.specials
        print(f"Specials are {self.specials}")
        return None

    def clear_test(self) -> None:
        """Clear and set the configurations to the initial ones in order to set ready the next test"""
        self.timer_on = False
        self.test_on = False
        self.specials = False
        self.numbers = False
        self.seconds = 0

        return None

    def start_timer(self) -> None:
        """Start the timer for the typing test"""
        self.timer_on = True

        def countdown() -> None:
            remainingTime: int = self.seconds
            while remainingTime > 0 and self.timer_on:
                time.sleep(1)
                remainingTime -= 1
                self.textTimer.config(text=f"Time: {remainingTime}s")
            if remainingTime <= 0:
                self.clear_test()
            return None

        timerThread: Thread = Thread(target=countdown)
        timerThread.daemon = True
        timerThread.start()

        return None

    def start_typing_test(self) -> None:
        """Start the typing test by showing the words in the canvas"""
        self.test_on = True

        return None
