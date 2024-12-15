from PyQt5.QtWidgets import QApplication
from ddc_control import DDC_Control
from PyQt5.QtGui import QIcon
from tray_app import TrayApp
import os, sys

def main():
    app = QApplication([])
    main_window = DDC_Control()

    if getattr(sys, 'frozen', False):
        # Running in a packaged executable
        icon_path = os.path.join(sys._MEIPASS, "sun.png")
    else:
        icon_path = os.path.abspath("sun.png")

    tray_icon = TrayApp(main_window, icon_path)
    tray_icon.show()
    app.exec_()

if __name__ == "__main__":
    main()