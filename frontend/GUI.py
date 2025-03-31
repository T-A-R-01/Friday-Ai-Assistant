from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QStackedWidget, QWidget, QLineEdit, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QLabel, QSizePolicy
from PyQt5.QtGui import QIcon, QPainter, QMovie, QColor, QTextCharFormat, QFont, QPixmap, QTextBlockFormat
from PyQt5.QtCore import Qt, QSize, QTimer
from dotenv import dotenv_values
import sys
import os


env_vars = dotenv_values(".env")
Assistantname = env_vars.get("Assistantname")
current_dir = os.getcwd()
old_chat_message = ""
TempDirPath = rf"{current_dir}\Frontend\Files"
GraphicsDirPath = rf"{current_dir}\Frontend\Graphics"

def AnswerModifier(Answer):
    lines = Answer.split("\n")
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = "\n".join(non_empty_lines)
    return modified_answer

def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "when", "where", "who", "which", "why", "can you", "whom", "whose", "what's", "where's"]

    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in [".", "?", "!"]:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        if query_words[-1][-1] in [".", "?", "!"]:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."

    return new_query.capitalize()

def SetMicrophoneStatus(Command):
    with open(rf"{TempDirPath}/Mic.data", "w", encoding="utf-8") as file:
        file.write(Command)

def GetMicrophoneStatus():
    with open(rf"{TempDirPath}/Mic.data", "r", encoding="utf-8") as file:
        return file.read()

def SetAssistantStatus(Status):
    with open (rf"{TempDirPath}/Status.data", "w", encoding="utf-8") as file:
        file.write(Status)
SetAssistantStatus("Speaking....")

def GetAssistantStatus():
    with open (rf"{TempDirPath}/Status.data", "r", encoding="utf-8") as file:
        return file.read()

def MicButtonInitialed():
    SetMicrophoneStatus("False")

def MicButtonClosed():
    SetMicrophoneStatus("True")

def GraphicsDictonaryPath(Filename):
    Path = rf"{GraphicsDirPath}\{Filename}"
    return Path

def TempDictonaryPath(Filename):
    Path = rf"{TempDirPath}\{Filename}"
    return Path

def ShowTextToScreen(Text):
    with open(rf"{TempDirPath}\Responses.data", "w", encoding="utf-8") as file:
        file.write(Text)

class ChatSection(QWidget):
    def __init__(self):
        super(ChatSection, self).__init__()

        # Get screen dimensions
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()

        # Reduce the GIF size
        max_gif_size_W = int(screen_width / 6)  # Small width
        max_gif_size_H = int(max_gif_size_W / 16 * 9)

        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)  # Proper margins
        layout.setSpacing(10)

        # Chat text edit (Ensure it remains visible)
        self.chat_text_edit = QTextEdit()
        self.chat_text_edit.setReadOnly(True)
        self.chat_text_edit.setTextInteractionFlags(Qt.TextSelectableByMouse)  # Allow selection
        self.chat_text_edit.setFrameStyle(QFrame.NoFrame)
        self.chat_text_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.chat_text_edit.setMinimumHeight(300)  # Ensure chat area is big enough
        layout.addWidget(self.chat_text_edit, stretch=5)  # Large stretch for chat

        # Set visible text color (Ensure text is not hidden)
        text_color = QColor(Qt.white)
        text_format = QTextCharFormat()
        text_format.setForeground(text_color)
        self.chat_text_edit.setCurrentCharFormat(text_format)

        # Set a test message (for debugging)
        self.chat_text_edit.setPlainText("Hello! This is a test message.")  # Ensure text is displayed

        # Styling
        self.setStyleSheet("background-color: black;")
        font = QFont()
        font.setPointSize(13)
        self.chat_text_edit.setFont(font)

        # GIF Section (Small size)
        self.gif_label = QLabel()
        self.gif_label.setStyleSheet("border: none;")
        movie = QMovie(GraphicsDictonaryPath("Jarvis.gif"))
        movie.setScaledSize(QSize(max_gif_size_W, max_gif_size_H))  # Small GIF
        self.gif_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.gif_label.setMovie(movie)
        movie.start()
        layout.addWidget(self.gif_label, stretch=1)  # Small stretch for GIF

        # Label under GIF
        self.label = QLabel("Jarvis Assistant")
        self.label.setStyleSheet("color: white; font-size: 14px; border: none; margin-top: -10px;")
        self.label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.label)

        # Scrollbar Styling (Ensure readability)
        self.chat_text_edit.setStyleSheet("""
            QTextEdit { color: white; }
            QScrollBar:vertical {
                border: none;
                background: black;
                width: 10px;
            }
            QScrollBar::handle:vertical {
                background: white;
                min-height: 20px;
            }
        """)

        # Timer for messages and speech recognition
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loadMessages)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(5)

        self.chat_text_edit.viewport().installEventFilter(self)


    def loadMessages(self):
        global old_chat_message

        with open(TempDictonaryPath("Responses.data"), "r", encoding="utf-8") as file:
            messages = file.read()

            if None == messages:
                pass

            elif len(messages) < 1:
                pass

            elif str(old_chat_message) == str(messages):
                pass

            else:
                self.addMessage(message=messages, color="White")
                old_chat_message = messages

    def SpeechRecogText(self):
        with open(TempDictonaryPath("Status.data"), "r", encoding="utf-8") as file:
            messages = file.read()
            self.label.setText(messages)

    def load_icon(self, path, width=60, height=60):
        pixmap = QPixmap(path)
        new_pixmap = pixmap.scaled(width, height)
        self.icon_label.setPixmap(new_pixmap)

    def toggle_icon(self, event=None):
        if self.toggled:
            self.load_icon(GraphicsDictonaryPath("voice.png"), 10, 10)
            MicButtonInitialed()
        else:
            self.load_icon(GraphicsDictonaryPath("mic.png"), 10, 10)
            MicButtonClosed()

        self.toggled = not self.toggled

    def addMessage(self, message, color):
        cursor = self.chat_text_edit.textCursor()
        format = QTextCharFormat()
        formatm = QTextBlockFormat()
        formatm.setTopMargin(10)
        formatm.setLeftMargin(10)
        format.setForeground(QColor(color))
        self.chat_text_edit.ensureCursorVisible()
        cursor.setCharFormat(format)
        cursor.setBlockFormat(formatm)
        cursor.insertText(message + "\n")
        self.chat_text_edit.setTextCursor(cursor)

class InitialScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Get screen dimensions
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()

        # Create a main layout
        content_layout = QVBoxLayout()
        content_layout.setAlignment(Qt.AlignCenter)  # Center content

        # GIF Label
        self.gif_label = QLabel(self)
        movie = QMovie(GraphicsDictonaryPath("Jarvis.gif"))

        # Set GIF size dynamically
        max_gif_size_W = int(screen_width / 2)  # Increase from 1/4 to 1/3 of the screen
        max_gif_size_H = int(max_gif_size_W / 16 * 9)  # Maintain aspect ratio
        movie.setScaledSize(QSize(max_gif_size_W, max_gif_size_H))

        self.gif_label.setMovie(movie)
        self.gif_label.setAlignment(Qt.AlignCenter)
        movie.start()

        # Status Label
        self.label = QLabel("")
        self.label.setStyleSheet("color: white; font-size: 18px;")
        self.label.setAlignment(Qt.AlignCenter)

        # Mic Button (as QLabel for click event)
        self.icon_label = QLabel()
        pixmap = QPixmap(GraphicsDictonaryPath("Mic_on.png"))
        new_pixmap = pixmap.scaled(40, 40)  # Reduced from 60x60 to 40x40
        self.icon_label.setPixmap(new_pixmap)
        self.icon_label.setFixedSize(60, 60)  # Reduced from 150x150 to 60x60  # Set a fixed size
        self.icon_label.setAlignment(Qt.AlignCenter)  # Ensure it's centered

        # Click event for Mic button
        self.toggled = True
        self.toggle_icon()
        self.icon_label.mousePressEvent = self.toggle_icon

        # Add widgets to layout
        content_layout.addWidget(self.gif_label, alignment=Qt.AlignCenter)
        content_layout.addSpacing(20)  # Space between GIF & status text
        content_layout.addWidget(self.label, alignment=Qt.AlignCenter)
        content_layout.addSpacing(10)  # Space between text & mic button
        content_layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)

        # Apply layout to the widget
        self.setLayout(content_layout)
        self.setFixedHeight(screen_height)
        self.setFixedWidth(screen_width)
        self.setStyleSheet("background-color: black;")

        # Timer for speech recognition text update
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(5)


    def SpeechRecogText(self):
        with open(TempDictonaryPath("Status.data"), "r", encoding="utf-8") as file:
            messages = file.read()
            self.label.setText(messages)

    def load_icon(self, path, width=100, height=100):
        pixmap = QPixmap(path)
        new_pixmap = pixmap.scaled(width, height)
        self.icon_label.setPixmap(new_pixmap)

    def toggle_icon(self, event=None):
        if self.toggled:
            self.load_icon(GraphicsDictonaryPath("Mic_on.png"), 56, 56)
            MicButtonInitialed()
        else:
            self.load_icon(GraphicsDictonaryPath("Mic_off.png"), 56,56 )
            MicButtonClosed()

        self.toggled = not self.toggled

class MessageScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        layout = QVBoxLayout()
        label = QLabel("")
        layout.addWidget(label)
        chat_section = ChatSection()
        layout.addWidget(chat_section)
        self.setLayout(layout)
        self.setStyleSheet("background-color: black;")
        self.setFixedHeight(screen_height)
        self.setFixedWidth(screen_width)

        
class CustomTopBar(QWidget):
    def __init__(self, parent, stack_widget):
        super().__init__(parent)
        self.setMinimumHeight(60)
        self.initUI()
        self.current_screen = None
        self.stack_widget = stack_widget
        self.offset = 0

    def initUI(self):
        self.setFixedHeight(50)

        # Main layout for the top bar
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(10, 0, 10, 0)

        # Left: Assistant name
        title_label = QLabel(f"AI VIRTUAL ASSISTANT")
        title_label.setStyleSheet("color: black; font-size: 18px; background-color: white;")
        title_layout = QHBoxLayout()
        title_layout.addWidget(title_label)
        title_layout.addStretch()  # Push everything to the left

        # Center: Home and Chat buttons
        center_layout = QHBoxLayout()
        center_layout.setAlignment(Qt.AlignCenter)
        home_button = QPushButton()
        home_icon = QIcon(GraphicsDictonaryPath("Home.png"))
        home_button.setIcon(home_icon)
        home_button.setText("  Home")
        home_button.setStyleSheet(
            "height: 40px; line-height: 40px; background-color: white; color: black; "
            "padding: 0 10px; margin: 5px; border: none"
        )
        home_button.setMinimumWidth(100)

        message_button = QPushButton()
        message_icon = QIcon(GraphicsDictonaryPath("Chats.png"))
        message_button.setIcon(message_icon)
        message_button.setText("  Chat")
        message_button.setStyleSheet(
            "height: 40px; line-height: 40px; background-color: white; color: black; "
            "padding: 0 10px; margin: 5px; border: none"
        )
        message_button.setMinimumWidth(100)

        center_layout.addWidget(home_button)
        center_layout.addWidget(message_button)

        # Right: Window control buttons
        minimize_button = QPushButton()
        minimize_icon = QIcon(GraphicsDictonaryPath("Minimize2.png"))
        minimize_button.setIcon(minimize_icon)
        minimize_button.setStyleSheet("background-color: white;")
        minimize_button.clicked.connect(self.minimize_window)

        self.maximize_button = QPushButton()
        self.maximize_icon = QIcon(GraphicsDictonaryPath("Maximize.png"))
        self.restore_icon = QIcon(GraphicsDictonaryPath("Minimize.png"))
        self.maximize_button.setIcon(self.maximize_icon)
        self.maximize_button.setFlat(True)
        self.maximize_button.setStyleSheet("background-color: white;")
        self.maximize_button.clicked.connect(self.maximize_window)

        close_button = QPushButton()
        close_icon = QIcon(GraphicsDictonaryPath("Close.png"))
        close_button.setIcon(close_icon)
        close_button.setStyleSheet("background-color: white;")
        close_button.clicked.connect(self.close_window)

        right_layout = QHBoxLayout()
        right_layout.addStretch()  # Push everything to the right
        right_layout.addWidget(minimize_button)
        right_layout.addWidget(self.maximize_button)
        right_layout.addWidget(close_button)

        # Add all sections to the main layout
        main_layout.addLayout(title_layout)
        main_layout.addLayout(center_layout)
        main_layout.addLayout(right_layout)

        # Set the main layout
        self.setLayout(main_layout)

        # Button functionality
        home_button.clicked.connect(lambda: self.stack_widget.setCurrentIndex(0))
        message_button.clicked.connect(lambda: self.stack_widget.setCurrentIndex(1))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.white)
        super().paintEvent(event)

    def minimize_window(self):
        self.parent().showMinimized()

    def maximize_window(self):
        if self.parent().isMaximized():
            self.parent().showNormal()
            self.maximize_button.setIcon(self.maximize_icon)
        else:
            self.parent().showMaximized()
            self.maximize_button.setIcon(self.restore_icon)

    def close_window(self):
        self.parent().close()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.offset:
            new_pos = event.globalPos() - self.offset
            self.parent().move(new_pos)

    def showMessageScreen(self):
        if self.current_screen is not None:
            self.current_screen.hide()

        message_screen = MessageScreen(self)
        layout = self.parent().layout()
        if layout is not None:
            layout.addWidget(message_screen)
        self.current_screen = message_screen

    def showInitialScreen(self):
        if self.current_screen is not None:
            self.current_screen.hide()

        intial_screen = InitialScreen(self)
        layout = self.parent().layout()
        if layout is not None:
            layout.addWidget(intial_screen)
        self.current_screen = intial_screen

        
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.initUI()

    def initUI(self):
        desktop = QApplication.desktop()
        screeen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        stacked_widget = QStackedWidget(self)
        initial_screen = InitialScreen()
        message_screen = MessageScreen()
        stacked_widget.addWidget(initial_screen)
        stacked_widget.addWidget(message_screen)
        self.setGeometry(0, 0, screeen_width, screen_height)
        self.setStyleSheet("background-color: black;")
        top_bar = CustomTopBar(self, stacked_widget)
        self.setMenuWidget(top_bar)
        self.setCentralWidget(stacked_widget)

def GraphicalUserInterface():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    GraphicalUserInterface()