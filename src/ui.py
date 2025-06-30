from tkinter import Tk, Frame
from importlib import import_module
from typing import cast


class UI:
    def __init__(self, root: Tk):
        self.root: Tk = root
        self.styles: dict = {
            "background_color": "#CCCCCC",
            "button_font": ("Segoe UI", 20, "normal"),
            "button_font_color": "#000000",
            "button_active_color": "#3A5A8C",
            "canvas_color": "#DfDEDE",
            "title_label_font": ("Segoe UI", 20, "bold"),
            "body_label_font": ("Segoe UI", 18, "normal"),
            "label_font_color": "#000000",
            "canvas_label_font": ("Segoe UI", 50, "normal"),
            "canvas_guide_font": ("Segoe UI", 40, "italic"),
            "guide_font_color": "#50a5ff"
        }
        self.screen_width: int = self.get_window_size()[0]
        self.screen_height: int = self.get_window_size()[1]
        self.current_frame: Frame = cast(Frame, None)
        self.modules: dict = {
            "MainUI": "main_ui",
            "ProfileUI": "profile_ui",
            "LoginUI": "login_ui",
            "RegisterUI": "register_ui"
        }
        self.configure_root()
        self.switch_frame("LoginUI")

    def get_window_size(self) -> tuple:
        """Returns the size of the user's window as a tuple: (width, height)"""
        return self.root.winfo_screenwidth(), self.root.winfo_screenheight()

    def configure_root(self) -> None:
        """Configures the main Tk object (root) for better visualization"""
        self.root.geometry(f"{self.screen_width}x{self.screen_height}")
        self.root.state("zoomed")
        self.root.configure(background=self.styles.get("background_color"))
        self.root.resizable(width=False, height=False)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        return None

    def switch_frame(self, frameClassName: str) -> None:
        """
        Switch the current frame to the specified one,
        using the class name (str)
        """
        if self.current_frame is not None:
            self.current_frame.on_frame_deactivation()
            self.current_frame.destroy()
        if not isinstance(frameClassName, str):
            raise ValueError(
                "The 'frameClassName' value is not a string"
            )
        module_name = self.modules.get(frameClassName)
        if not module_name:
            raise ValueError(
                "The class name does not exist or isn't valid"
            )
        module = import_module(module_name)
        module_class = getattr(module, frameClassName)
        self.current_frame = module_class(self.root, self)
        self.current_frame.on_frame_activation()
        self.current_frame.grid(row=0, column=0, sticky="nsew")
        self.current_frame.grid_propagate(False)
        self.root.update_idletasks()
        return None

    def keep_open(self) -> None:
        """Calls the 'mainloop' function to keep open the main Tk window"""
        self.root.mainloop()
        return None
