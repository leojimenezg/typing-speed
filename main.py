# ----- GRAPHIC USER INTERFACE -----
# TODO: Complete the MainUI to show the text, app options and few metrics
# TODO: Complete the ProfileUI to show the profile information and specific metrics
# TODO: Complete the LoginUI and the RegisterUI

# ----- FUNCTIONALITY -----
# TODO: Generate random words for the user to write
# TODO: Get the input keywords from the user for comparisons
# TODO: Move forward as the user writes, even if there are errors (or deletes)
# TODO: Compare the user input with the current word

# ----- METRICS -----
# TODO: Calculate the metrics (precision, speed, wpm, correct and incorrect letters, etc)

from tkinter import Tk
from ui import UI

rt = Tk()
ui_obj = UI(root=rt)
ui_obj.keep_open()
