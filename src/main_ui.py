from tkinter import Frame, Tk, Canvas, Label, Button
from tkinter import Event, OptionMenu, StringVar
from threading import Thread
from random import choice, randint
from typing import cast
from math import floor
import time


class MainUI(Frame):
    def __init__(self, master: Tk, ui):
        super().__init__(master)
        self.ui = ui
        self.canvas: Canvas = cast(Canvas, None)
        self.canvas_text_id: int = 0
        self.canvas_text: str = ""
        self.canvas_text_idx: int = 0
        self.canvas_guide_id: int = 0
        self.canvas_guide_idx: int = 1  # Represents the line user is currently
        self.max_chars: dict = {  # Should be dinamically calculated
            "canvas": 40,
            "specials": 2,
            "numbers": 2
        }
        self.text_correct: Label = cast(Label, None)
        self.text_incorrect: Label = cast(Label, None)
        self.text_counter: list = [0, 0]  # [correct, incorrect]
        self.text_timer: Label = cast(Label, None)
        self.seconds: int = 0
        self.numbers: bool = False
        self.specials: bool = False
        self.test_on: bool = False
        self.timer_on: bool = False
        self.bindings: list = [
            ("<Return>", self.start_typing_test),
            ("<Escape>", self.finish_typing_test),
            ("<KeyPress>", self.check_typing),
        ]
        self.no_keys: list = [
            "Return", "Escape", "Shift_L", "Shift_R", "Alt_L",
            "Alt_R", "Caps_Lock", "Control_L", "Control_R",
            "Delete", "Tab", "BackSpace", "Meta_L", "Meta_R",
        ]
        self.bind_ids: list = []
        self.words: list = []
        self.specials: list = []
        self.numbers: list = []
        self.language: StringVar = StringVar(self)
        self.language.set("english")
        self.languages: list = ["english", "spanish"]
        self.configure_layout()
        self.create_top_bar()
        self.create_canvas()
        self.create_bottom_bar()
        self.set_time_variable(30)

    def configure_layout(self) -> None:
        """Configure the main layout and the grid to be used"""
        self.config(bg=self.ui.styles.get("background_color"))
        self.grid_columnconfigure(tuple(range(9)), weight=1)
        self.grid_rowconfigure(1, weight=1)
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
        """Create the top navigation bar."""
        top_bar: Frame = Frame(
            self,
            bg=self.ui.styles.get("background_color"),
            relief="flat",
            bd=1
        )
        top_bar.grid(row=0, column=0, columnspan=10, sticky="ew", pady=20)
        top_bar.grid_columnconfigure(tuple(range(9)), weight=1)
        btn_styles: dict = {
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
        time_btn_config: list = [
            ("30s", self.set_time_variable, 0, 30),
            ("60s", self.set_time_variable, 1, 60),
            ("90s", self.set_time_variable, 2, 90),
            ("120s", self.set_time_variable, 3, 120)
        ]
        for text, command, col, secs in time_btn_config:
            btn: Button = Button(
                top_bar,
                text=text,
                command=lambda t=secs, cmd=command: cmd(t),
                **btn_styles
            )
            btn.grid(row=0, column=col, sticky="nsew", padx=2, pady=2)
            setattr(self, f"btn{text}", btn)
        sep1: Frame = Frame(
            top_bar,
            bg=self.ui.styles.get("background_color"),
            width=2
        )
        sep1.grid(row=0, column=4, sticky="ns", padx=5)
        setattr(self, "separator1", sep1)
        option_menu: OptionMenu = OptionMenu(
            top_bar,
            self.language,
            *self.languages
        )
        option_menu.config(
            bg=self.ui.styles.get("background_color"),
            fg=self.ui.styles.get("button_font_color"),
            activebackground=self.ui.styles.get("button_active_color"),
            highlightthickness=0, relief="flat", padx=10, pady=5
        )
        menu = option_menu.nametowidget(option_menu.menuname)
        menu.config(
            font=self.ui.styles.get("button_font"),
            bg=self.ui.styles.get("background_color"),
            fg=self.ui.styles.get("button_font_color"),
            activebackground=self.ui.styles.get("button_active_color"),
            activeforeground="white", bd=2
        )
        option_menu.grid(row=0, column=5, sticky="nsew", padx=2, pady=2)
        setattr(self, "option_menu", option_menu)
        extra_btn_config: list = [
            ("Specials", self.set_specials_variable, 6),
            ("Numbers", self.set_numbers_variable, 7)
        ]
        for text, command, col in extra_btn_config:
            btn: Button = Button(
                top_bar,
                text=text,
                command=command,
                **btn_styles
            )
            btn.grid(row=0, column=col, sticky="nsew", padx=2, pady=2)
            setattr(self, f"btn{text}", btn)
        sep2: Frame = Frame(
            top_bar,
            bg=self.ui.styles.get("background_color"),
            width=2
        )
        sep2.grid(row=0, column=8, sticky="ns", padx=5)
        setattr(self, "separator2", sep2)
        profile: Button = Button(
            top_bar,
            text="Profile",
            command=self.switch_to_profile,
            **btn_styles
        )
        profile.grid(row=0, column=9, sticky="nsew", padx=2, pady=2)
        setattr(self, "btnProfile", profile)
        return None

    def create_canvas(self) -> None:
        """Create and configure the canvas to show the corresponding text"""
        canvas_frame: Frame = Frame(
            self,
            bg=self.ui.styles.get("background_color"),
            relief="sunken"
        )
        canvas_frame.grid(
            row=1, column=0, columnspan=9, sticky="nsew", pady=20
        )
        canvas_frame.grid_columnconfigure(0, weight=1)
        canvas_frame.grid_rowconfigure(0, weight=1)
        self.canvas: Canvas = Canvas(
            canvas_frame,
            bg=self.ui.styles.get("canvas_color"),
            highlightthickness=0
        )
        self.canvas.grid(row=0, column=0, sticky="nsew")
        return None

    def create_bottom_bar(self) -> None:
        """Create and configure the bottom bar to show few metrics"""
        status_bar: Frame = Frame(
            self,
            bg=self.ui.styles.get("background_color"),
            relief="flat",
            bd=1
        )
        status_bar.grid(row=2, column=0, columnspan=9, sticky="ew", pady=20)
        for i in range(0, 9):
            status_bar.grid_columnconfigure(i, weight=1)
        metric_styles: dict = {
            "font": self.ui.styles.get("button_font"),
            "bg": self.ui.styles.get("background_color"),
            "padx": 10,
            "pady": 20
        }
        self.text_correct: Label = Label(
            status_bar,
            text=f"Correct: {self.text_counter[0]}",
            fg="#27ae60",
            anchor="w",
            **metric_styles
        )
        self.text_correct.grid(row=0, column=0, columnspan=3, sticky="w")
        self.text_timer: Label = Label(
            status_bar,
            text="Time: 0",
            fg="#000000",
            **metric_styles
        )
        self.text_timer.grid(row=0, column=3, columnspan=3, sticky="ns")
        self.text_incorrect: Label = Label(
            status_bar,
            text=f"Incorrect: {self.text_counter[1]}",
            fg="#c0392b",
            anchor="e",
            **metric_styles
        )
        self.text_incorrect.grid(row=0, column=6, columnspan=3, sticky="e")
        return None

    def switch_to_profile(self) -> None:
        """Switch to profile frame from the main frame"""
        if not self.test_on:
            self.ui.switch_frame(frameClassName="ProfileUI")
        return None

    def set_time_variable(self, seconds: int) -> None:
        """Change the time used for the tests"""
        if not self.test_on:
            self.seconds = seconds
            self.text_timer.config(text=f"Time: {self.seconds}s")
        return None

    def set_numbers_variable(self) -> None:
        """Change the numbers variable to enable or disable them"""
        if not self.test_on:
            self.numbers = not self.numbers
        return None

    def set_specials_variable(self) -> None:
        """Change the specials variable to enable or disable them"""
        if not self.test_on:
            self.specials = not self.specials
        return None

    def start_timer(self) -> None:
        """Start the timer for the typing test"""
        self.timer_on = True

        def countdown() -> None:
            time_left: int = self.seconds
            while time_left > 0 and self.timer_on:
                time.sleep(1)
                time_left -= 1
                self.text_timer.config(text=f"Time: {time_left}s")
            if time_left <= 0:
                self.timer_on = False
                self.show_test_results()
            return None

        timer_thread: Thread = Thread(target=countdown)
        timer_thread.daemon = True
        timer_thread.start()
        return None

    def start_typing_test(self, event: Event) -> None:
        """Start the typing test setting variables and calling functions"""
        if not self.test_on and not self.timer_on:
            print(f"Test started using {event.keysym} key.")
            self.test_on = True
            self.fill_words_list()
            if self.specials:
                self.fill_specials_list()
            if self.numbers:
                self.fill_numbers_list()
            self.start_timer()
            self.typing_test_text()
        return None

    def finish_typing_test(self, event: Event) -> None:
        """Finish the typing test if it started and timer has ended"""
        if self.test_on and not self.timer_on:
            print(f"Typing test finished using {event.keysym} key.")
            self.test_on = False
            self.clear_test()
        return None

    def clear_test(self) -> None:
        """Clear and set configurations to the initial ones"""
        self.clear_canvas()
        self.timer_on = False
        self.test_on = False
        self.text_counter = [0, 0]
        self.words = []
        self.specials = []
        self.numbers = []
        self.text_timer.config(text=f"Time: {self.seconds}s")
        self.text_correct.config(text=f"Correct: {self.text_counter[0]}")
        self.text_incorrect.config(text=f"Incorrect: {self.text_counter[1]}")
        return None

    def clear_canvas(self) -> None:
        """Clear all the canvas content and the related variables to it"""
        self.canvas.delete("all")
        self.canvas_text_id = None
        self.canvas_text_idx = 0
        self.canvas_guide_id = None
        self.canvas_guide_idx = 1
        return None

    def fill_words_list(self) -> None:
        """Get the words from the files/{language}_words.txt file"""
        with open(
            file=f"files/{self.language.get()}_words.txt", mode="r"
        ) as file:
            # A line has only one word.
            self.words: list = [
                word.replace("\n", "") for word in file.readlines()
            ]
        return None

    def fill_specials_list(self) -> None:
        """Get the special characters from the files/specials_file.txt file"""
        with open(
            file="files/specials_file.txt", mode="r"
        ) as file:
            # A line has only one special character.
            self.specials: list = [
                special.replace("\n", "") for special in file.readlines()
            ]
        return None

    def fill_numbers_list(self) -> None:
        """Get the number characters from the files/numbers_file.txt file"""
        with open(
            file="files/numbers_file.txt", mode="r"
        ) as file:
            # A line has only one number character.
            self.numbers: list = [
                number.replace("\n", "") for number in file.readlines()
            ]
        return None

    def get_random_word(self) -> str:
        """Return a random word from the initialized list"""
        return choice(self.words)

    def get_randon_special(self) -> str:
        """Return a random special character from the initialized list"""
        return choice(self.specials)

    def get_random_number(self) -> str:
        """Return a random number from the initialized list"""
        return choice(self.numbers)

    def create_text_line(self) -> str:
        """Return a line with random words to be displayed in the canvas"""
        line: list = []
        line_length: int = 0
        last_word = self.get_random_word()
        line.append(last_word)
        line_length += len(last_word)
        while line_length < self.max_chars.get("canvas"):
            word = self.get_random_word()
            if word != last_word:
                if (line_length + len(word)) < self.max_chars.get("canvas"):
                    line.append(word)
                    line_length += len(word)
                    last_word = word
                else:
                    line_length += 1
        if self.specials and self.numbers:
            counter: int = 0
            line_length: int = len(line) - 1
            while (
                    counter < self.max_chars.get("specials")
                    + self.max_chars.get("numbers")
            ):
                random_idx = randint(0, line_length)
                if counter % 2 == 0:
                    line[random_idx] = self.get_randon_special()
                else:
                    line[random_idx] = self.get_random_number()
                counter += 1
        elif self.specials:
            counter: int = 0
            line_length: int = len(line) - 1
            while counter < self.max_chars.get("specials"):
                random_idx = randint(0, line_length)
                line[random_idx] = self.get_randon_special()
                counter += 1
        elif self.numbers:
            counter: int = 0
            line_length: int = len(line) - 1
            while counter < self.max_chars.get("numbers"):
                random_idx = randint(0, line_length)
                line[random_idx] = self.get_random_number()
                counter += 1
        return " ".join(line)

    def typing_test_text(self) -> None:
        """Initialize and create the text in the canvas for the typing test"""
        text_lines = [
            self.create_text_line(),
            self.create_text_line(),
            self.create_text_line(),
            self.create_text_line(),
        ]
        full_text = "\n\n".join(text_lines)
        self.canvas_text = full_text
        self.canvas_text_id = self.canvas.create_text(
            700, 370,  # Should be dinamically calculated
            text=full_text,
            font=self.ui.styles.get("canvas_label_font"),
            fill=self.ui.styles.get("label_font_color"),
            justify="center"
        )
        self.typing_test_guide()
        return None

    def typing_test_guide(self) -> None:
        """Initialize and create the guide in the canvas for the typing text"""
        guide: str = f"Line: {self.canvas_guide_idx}   "
        guide += f"Next character: {self.canvas_text[self.canvas_text_idx]}"
        self.canvas_guide_id = self.canvas.create_text(
            700, 80,
            text=guide,
            font=self.ui.styles.get("canvas_guide_font"),
            fill=self.ui.styles.get("guide_font_color"),
            justify="center"
        )
        return None

    def check_typing(self, event: Event) -> None:
        """Compare the canvas text with the pressed key"""
        if self.test_on and self.timer_on:
            if event.keysym in self.no_keys:
                return None
            while self.canvas_text[self.canvas_text_idx] == "\n":
                self.canvas_text_idx += 1
            if event.char == self.canvas_text[self.canvas_text_idx]:
                self.text_counter[0] += 1  # Correct
                self.update_text_counter(0)
            else:
                self.text_counter[1] += 1  # Incorrect
                self.update_text_counter(1)
            self.canvas_text_idx += 1
            if self.canvas_text_idx >= len(self.canvas_text):
                self.clear_canvas()
                self.typing_test_text()
            self.update_guide()
        return None

    def update_text_counter(self, index: int) -> None:
        """Update the correct/incorrect text according to the received index"""
        if index == 0:
            self.text_correct.config(
                text=f"Correct: {self.text_counter[index]}"
            )
        else:
            self.text_incorrect.config(
                text=f"Incorrect: {self.text_counter[index]}"
            )
        return None

    def update_guide(self) -> None:
        """Update the canvas text guide as a whole single text"""
        text_idx = self.canvas_text_idx
        if self.canvas_text[text_idx] == "\n":
            text_idx += 2
            self.canvas_guide_idx += 1
        updated_guide: str = f"Line: {self.canvas_guide_idx}   "
        updated_guide += f"Next character: {self.canvas_text[text_idx]}"
        self.canvas.itemconfig(self.canvas_guide_id, text=updated_guide)
        return None

    def show_test_results(self) -> None:
        """Show in the canvas the results of the typing test"""
        self.clear_canvas()
        language: str = f"Language: {self.language.get()}"
        self.canvas.create_text(
            400, 200,
            text=language,
            font=self.ui.styles.get("canvas_label_font"),
            fill=self.ui.styles.get("label_font_color"),
            justify="center"
        )
        incorrect: str = f"Incorrect: {self.text_counter[1]}"
        self.canvas.create_text(
            400, 400,
            text=incorrect,
            font=self.ui.styles.get("canvas_label_font"),
            fill=self.ui.styles.get("label_font_color"),
            justify="center"
        )

        raw: str = f"Raw: {self.text_counter[0] + self.text_counter[1]}"
        self.canvas.create_text(
            750, 200,
            text=raw,
            font=self.ui.styles.get("canvas_label_font"),
            fill=self.ui.styles.get("label_font_color"),
            justify="center"
        )
        wpm: str = f"WPM: {self.calculate_wpm()}"
        self.canvas.create_text(
            750, 400,
            text=wpm, font=self.ui.styles.get("canvas_label_font"),
            fill=self.ui.styles.get("label_font_color"),
            justify="center"
        )

        seconds: str = f"Seconds: {self.seconds}"
        self.canvas.create_text(
            1100, 200,
            text=seconds,
            font=self.ui.styles.get("canvas_label_font"),
            fill=self.ui.styles.get("label_font_color"),
            justify="center"
        )
        correct: str = f"Correct: {self.text_counter[0]}"
        self.canvas.create_text(
            1100, 400,
            text=correct,
            font=self.ui.styles.get("canvas_label_font"),
            fill=self.ui.styles.get("label_font_color"),
            justify="center"
        )
        return None

    def calculate_wpm(self) -> int:
        """Calculate the wpm"""
        if self.text_counter[0] != 0:
            wpm = floor((self.text_counter[0] / 5) * (60 / self.seconds))
            return wpm
        return 0
