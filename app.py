import sys
import time
import rotatescreen

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction, QIcon, QPalette, QColor, QGuiApplication

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QSystemTrayIcon, QMenu

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QSizePolicy
)

def get_darkModePalette( app=None ) :
    
    darkPalette = app.palette()
    darkPalette.setColor( QPalette.ColorRole.Window, QColor( 53, 53, 53 ) )
    darkPalette.setColor( QPalette.ColorRole.WindowText, QColor(255,255,255) )
    darkPalette.setColor( QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, QColor( 127, 127, 127 ) )
    darkPalette.setColor( QPalette.ColorRole.Base, QColor( 42, 42, 42 ) )
    darkPalette.setColor( QPalette.ColorRole.AlternateBase, QColor( 66, 66, 66 ) )
    darkPalette.setColor( QPalette.ColorRole.ToolTipBase, QColor( 53, 53, 53 ) )
    darkPalette.setColor( QPalette.ColorRole.ToolTipText, QColor(255,255,255) )
    darkPalette.setColor( QPalette.ColorRole.Text, QColor(255,255,255) )
    darkPalette.setColor( QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, QColor( 127, 127, 127 ) )
    darkPalette.setColor( QPalette.ColorRole.Dark, QColor( 35, 35, 35 ) )
    darkPalette.setColor( QPalette.ColorRole.Shadow, QColor( 20, 20, 20 ) )
    darkPalette.setColor( QPalette.ColorRole.Button, QColor( 53, 53, 53 ) )
    darkPalette.setColor( QPalette.ColorRole.ButtonText, QColor(255,255,255) )
    darkPalette.setColor( QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, QColor( 127, 127, 127 ) )
    darkPalette.setColor( QPalette.ColorRole.BrightText, QColor(255,0,0) )
    darkPalette.setColor( QPalette.ColorRole.Link, QColor( 42, 130, 218 ) )
    darkPalette.setColor( QPalette.ColorRole.Highlight, QColor( 42, 130, 218 ) )
    darkPalette.setColor( QPalette.ColorGroup.Disabled, QPalette.ColorRole.Highlight, QColor( 80, 80, 80 ) )
    darkPalette.setColor( QPalette.ColorRole.HighlightedText, QColor(255,255,255) )
    darkPalette.setColor( QPalette.ColorGroup.Disabled, QPalette.ColorRole.HighlightedText, QColor( 127, 127, 127 ), )
    
    return darkPalette

# Subclass QMainWindow to customize your application's main window
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.setWindowTitle("My App")

#         button = QPushButton("Press Me!")

#         self.setFixedSize(QSize(400, 300))

#         # Set the central widget of the Window.
#         self.setCentralWidget(button)

class ImageTextButton(QPushButton):
    def __init__(self, image_path, text, parent=None):
        super().__init__(parent)
        self.image_label = QLabel()
        self.image_label.setPixmap(QIcon(image_path).pixmap(self.size()))  # Use sizeHint()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center image both horizontally and vertically

        self.text_label = QLabel(text)
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)  # Center image both horizontally and vertically
        self.image_label.setScaledContents(True)
        
        padding = self.size().width() // 16  # Calculate half the remaining space
        
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.text_label)
        layout.setContentsMargins(padding, padding, padding, padding)  # Add padding to all sides
        self.setLayout(layout)
        self.setFixedSize(192, 192)

        # Ensure buttons have equal width based on initial size
        size_policy = QSizePolicy()
        size_policy.setHorizontalPolicy(QSizePolicy.Policy.Expanding)
        size_policy.setVerticalPolicy(QSizePolicy.Policy.Fixed)
        self.setSizePolicy(size_policy)

class MainWindow(QWidget):
    def __init__(self):
        self.config = {
            "mode": "laptop",
            "laptop_id": 0,
            "book_id": 0,
            "presentation_id": 0,
            "tablet_id": 0,
        }
        super().__init__()
        self.setWindowTitle("FlipBookControl")

        # Replace with your actual image paths
        image_paths = ["res/images/laptop_mode.png", "res/images/book_mode.png", "res/images/presentation_mode.png", "res/images/tablet_mode"]
        texts = ["Laptop", "Book", "Presentation"]
        actions = [self.action_laptop, self.action_book, self.action_presentation]

        layout = QHBoxLayout()
        for image_path, text, action in zip(image_paths, texts, actions):
            button = ImageTextButton(image_path, text)
            # Optional: Connect button clicks to desired actions
            # button.clicked.connect(self.handle_button_click)  # Define handle_button_click()
            button.clicked.connect(action)
            layout.addWidget(button, stretch=1)

        self.setLayout(layout)
        # Center the window on the screen
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.centerOnScreen()

    def action_laptop(self):
        screen1 = rotatescreen.get_primary_display()
        screen2 = rotatescreen.get_secondary_displays()[0]
        screen1.set_landscape()	
        screen2.set_landscape()
        self.hide()
    
    def action_book(self):
        screen1 = rotatescreen.get_primary_display()
        screen2 = rotatescreen.get_secondary_displays()[0]
        screen1.set_portrait_flipped()	
        screen2.set_portrait_flipped()	
        self.hide()

    def action_presentation(self):
        screen1 = rotatescreen.get_primary_display()
        screen2 = rotatescreen.get_secondary_displays()[0]
        screen1.set_landscape()
        screen2.set_landscape_flipped()
        self.hide()
        	

    def action_tablet(self):
        pass

    def centerOnScreen(self):
        # Get the primary screen using QGuiApplication.primaryScreen()
        screen = QGuiApplication.primaryScreen()

        # Get screen geometry and available size
        screen_geometry = screen.geometry()
        available_size = screen.availableGeometry()

        # Calculate window position for centering (improved)
        window_center_x = screen_geometry.center().x() - self.width() // 2
        window_center_y = (available_size.top() + available_size.height() // 2) - self.height() // 2

        # Adjust for taskbar height (optional)
        taskbar_height = screen_geometry.bottom() - available_size.bottom()  # Approximate taskbar height
        if taskbar_height > 0:
            window_center_y -= taskbar_height // 2  # Adjust for half the taskbar height

        # Move the window to the calculated position
        self.move(window_center_x, window_center_y)



    # def handle_button_click(self):
    #     # Implement button click behavior here

class FlipBookControl(QApplication):
    def __init__(self):
        super().__init__(sys.argv  + ['-platform', 'windows:darkmode=2'])
        self.setStyle( 'Fusion' )
        self.setPalette(get_darkModePalette( self ))

        icon = QIcon("res/images/cover_mode_v2.png")

        self.window = MainWindow()  # Create the main window instance
        self.window.setWindowIcon(icon)
        self.setQuitOnLastWindowClosed(False)

        # Create the tray
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(icon)
        self.tray_icon.setVisible(True)

        self.menu = QMenu()
        self.show_window_action = QAction("Show Main Window", self)
        self.show_window_action.triggered.connect(self.show_main_window)
        self.menu.addAction(self.show_window_action)

        self.tray_icon.activated.connect(self.show_main_window)

        # Add a Quit option to the menu.
        self.quit_action = QAction("Quit")
        self.quit_action.triggered.connect(self.quit)
        self.menu.addAction(self.quit_action)

        self.tray_icon.setContextMenu(self.menu)
        #self.tray_icon.setVisible(True)

    def show_main_window(self):
        if not self.window.isVisible():
            self.window.show()  # Ensure the main window is shown when the action is triggered
            self.window.centerOnScreen()  # Center the window on the screen
        else:
            self.window.hide()


def main():
    app = FlipBookControl()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
