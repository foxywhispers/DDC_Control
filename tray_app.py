from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction, QApplication
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtCore import QPoint

class TrayApp(QSystemTrayIcon):
    def __init__(self, main_window, icon_path, parent=None):
        super().__init__(parent)
        self.setIcon(QIcon(icon_path))
        self.setToolTip("DDC Control Tray")
        self.menu = QMenu(parent)

        self.quit_action = QAction("Quit", parent)
        self.menu.addAction(self.quit_action)

        self.setContextMenu(self.menu)

        self.main_window = main_window

        self.quit_action.triggered.connect(QApplication.quit)

        self.activated.connect(self.on_tray_icon_click)

        self.main_window.closeEvent = self.close_event

    def position_window_above_icon(self):

        cursor_pos = QCursor.pos()

        window_rect = self.main_window.frameGeometry()
        window_rect.moveTopLeft(cursor_pos - QPoint(window_rect.width() // 2, window_rect.height() + 35))

        self.main_window.move(window_rect.topLeft())

    def on_tray_icon_click(self, reason):
        if reason == QSystemTrayIcon.Trigger:  # Left click
            if self.main_window.isVisible():
                self.hide_app()
            else:
                self.show_app()

    def show_app(self):
        self.main_window.show()
        self.main_window.raise_()
        self.main_window.activateWindow()
        self.position_window_above_icon()
    
    def hide_app(self):
        self.main_window.hide()
    
    def close_event(self, event):
        event.ignore()
        self.hide_app()

    def quit_app(self):
        QApplication.quit()