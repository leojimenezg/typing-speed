from tkinter import Tk, Frame
from importlib import import_module
from typing import cast


class UI:
    def __init__(self, root: Tk):
        self.root: Tk = root
        self.styles: dict = {
            "background_color": "#cccccc",
            "button_font": ("Segoe UI", 20, "normal"),
            "button_font_color": "#000000",
            "button_active_color": "#3a5a8c",
            "canvas_color": "#dfdede",
            "title_label_font": ("Segoe UI", 20, "bold"),
            "body_label_font": ("Segoe UI", 18, "normal"),
            "label_font_color": "#000000",
            "canvas_label_font": ("Segoe UI", 50, "normal"),
        }
        self.screenWidth: int = self.get_window_size()[0]
        self.screenHeight: int = self.get_window_size()[1]
        self.currentFrame: Frame = cast(Frame, None)
        self.moduleDict: dict = {
            "MainUI": "main_ui",
            "ProfileUI": "profile_ui",
            "LoginUI": "login_ui",
            "RegisterUI": "register_ui"
        }
        self.configure_root()
        self.switch_frame("MainUI")

    def get_window_size(self) -> tuple:
        """Returns the size of the user's window as a tuple: (width, height)"""
        return self.root.winfo_screenwidth(), self.root.winfo_screenheight()

    def configure_root(self) -> None:
        """Configures the main Tk object (root) for better visualization"""
        self.root.geometry(f"{self.screenWidth}x{self.screenHeight}")
        self.root.state("zoomed")
        self.root.configure(background=self.styles.get("background_color"))
        self.root.resizable(width=False, height=False)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        return None

    def switch_frame(self, frameClassName: str) -> None:
        """Switch the current frame to the specified one, using the class name (str)"""
        if self.currentFrame is not None:
            self.currentFrame.on_frame_deactivation()
            self.currentFrame.destroy()
        if not isinstance(frameClassName, str):
            raise ValueError(f"The received value of 'frameClassName' is not a string object: {frameClassName}")
        moduleName = self.moduleDict.get(frameClassName)
        if not moduleName:
            raise ValueError(f"The given class name does not exist or isn't valid: '{frameClassName}'")
        module = import_module(moduleName)
        frameClass = getattr(module, frameClassName)
        self.currentFrame = frameClass(self.root, self)
        self.currentFrame.on_frame_activation()
        self.currentFrame.grid(row=0, column=0, sticky="nsew")
        self.currentFrame.grid_propagate(False)
        self.root.update_idletasks()
        return None

    def keep_open(self) -> None:
        """Calls the 'mainloop' function to keep open the main Tk window"""
        self.root.mainloop()
        return None
