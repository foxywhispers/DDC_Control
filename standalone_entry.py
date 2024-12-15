from PyQt5.QtWidgets import QApplication
from ddc_control import DDC_Control

def main():
    app = QApplication([])
    window = DDC_Control()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()