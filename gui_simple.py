"""
Simple Clean GUI - Minimal & Sticky
Small, neat interface that stays at top right and out of the way
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import threading
from datetime import datetime

from agent import OSAgent
from intent_analyzer import IntentAnalyzer
from chat_handler import ChatHandler

# Solid Color Palette (Flat Design)
COLORS = {
    'bg': '#1e1e1e',        # Solid Dark Grey
    'header': '#252526',    # Slightly lighter header
    'accent': '#007acc',    # VS Code Blue (Solid, Professional)
    'text': '#ffffff',      # White
    'text_dim': '#cccccc',  # Light Grey
    'border': '#333333',    # Dark Border
    'success': '#4ec9b0',   # Soft Green
    'error': '#f44747',     # Soft Red
}

class SimpleGUI(QMainWindow):
    """Simple, clean, minimal GUI"""
    
    log_signal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.is_executing = False
        self.drag_pos = QPoint()
        
        self.agent = OSAgent(logger_callback=self.safe_log)
        self.intent_analyzer = IntentAnalyzer()
        self.chat_handler = ChatHandler()
        
        self.log_signal.connect(self.add_log)
        
        self.initUI()
    
    def initUI(self):
        """Build minimal UI"""
        self.setWindowTitle('AI Agent')
        
        # Small size, Top Right
        screen = QApplication.desktop().screenGeometry()
        w, h = 300, 450
        x = screen.width() - w - 20
        y = 20  # Top of screen
        
        self.setGeometry(x, y, w, h)
        self.setFixedSize(w, h)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Main container
        container = QFrame()
        container.setStyleSheet(f"""
            QFrame {{
                background: {COLORS['bg']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
            }}
        """)
        
        self.setCentralWidget(container)
        layout = QVBoxLayout(container)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Header
        header = QHBoxLayout()
        header.setSpacing(8)
        
        # Status Dot
        self.status_dot = QLabel('●')
        self.status_dot.setFont(QFont('Arial', 12))
        self.status_dot.setStyleSheet(f"color: {COLORS['success']}; background: transparent; border: none;")
        header.addWidget(self.status_dot)
        
        title = QLabel('OS Agent')
        title.setFont(QFont('Helvetica Neue', 11, QFont.Bold))
        title.setStyleSheet(f"color: {COLORS['text']}; background: transparent; border: none;")
        header.addWidget(title)
        
        header.addStretch()
        
        # Close button
        close_btn = QPushButton('×')
        close_btn.setFixedSize(20, 20)
        close_btn.clicked.connect(self.close)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {COLORS['text_dim']};
                border: none;
                font-size: 18px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                color: {COLORS['error']};
            }}
        """)
        header.addWidget(close_btn)
        
        layout.addLayout(header)
        
        # Separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet(f"background: {COLORS['border']}; max-height: 1px; border: none;")
        layout.addWidget(line)
        
        # Log Area
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setFont(QFont('Menlo', 10))  # Fixed font warning (was Courier)
        self.log.setStyleSheet(f"""
            QTextEdit {{
                background: {COLORS['bg']};
                color: {COLORS['text_dim']};
                border: none;
            }}
            QScrollBar:vertical {{
                background: {COLORS['bg']};
                width: 6px;
            }}
            QScrollBar::handle:vertical {{
                background: {COLORS['border']};
                border-radius: 3px;
            }}
        """)
        layout.addWidget(self.log)
        
        # Input Area
        input_container = QFrame()
        input_container.setStyleSheet(f"""
            QFrame {{
                background: {COLORS['header']};
                border-radius: 4px;
                border: 1px solid {COLORS['border']};
            }}
        """)
        input_layout = QVBoxLayout(input_container)
        input_layout.setContentsMargins(4, 4, 4, 4)
        input_layout.setSpacing(4)
        
        self.cmd_input = QLineEdit()
        self.cmd_input.setPlaceholderText('Type a command...')
        self.cmd_input.setFont(QFont('Helvetica Neue', 11))
        self.cmd_input.returnPressed.connect(self.execute)
        self.cmd_input.setStyleSheet(f"""
            QLineEdit {{
                background: transparent;
                color: {COLORS['text']};
                border: none;
                padding: 4px;
            }}
        """)
        input_layout.addWidget(self.cmd_input)
        
        layout.addWidget(input_container)
        
        # Execute button
        self.exec_btn = QPushButton('Execute')
        self.exec_btn.clicked.connect(self.execute)
        self.exec_btn.setCursor(Qt.PointingHandCursor)
        self.exec_btn.setFont(QFont('Helvetica Neue', 11, QFont.Bold))
        self.exec_btn.setFixedHeight(32)
        self.exec_btn.setStyleSheet(f"""
            QPushButton {{
                background: {COLORS['accent']};
                color: {COLORS['text']};
                border: none;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background: #006bb3;
            }}
            QPushButton:disabled {{
                background: {COLORS['border']};
                color: {COLORS['text_dim']};
            }}
        """)
        layout.addWidget(self.exec_btn)
    
    def execute(self):
        """Execute command"""
        cmd = self.cmd_input.text().strip()
        if not cmd or self.is_executing:
            return
        
        self.is_executing = True
        self.exec_btn.setEnabled(False)
        self.cmd_input.setEnabled(False)
        self.status_dot.setStyleSheet(f"color: {COLORS['accent']}; background: transparent; border: none;")
        
        self.safe_log(f"<span style='color: {COLORS['text']}'>▶ {cmd}</span>")
        
        def run():
            try:
                intent = self.intent_analyzer.analyze(cmd)
                # self.safe_log(f"<span style='color: {COLORS['text_dim']}'>├─ Intent: {intent.get('intent_type')}</span>")
                
                if self.intent_analyzer.is_conversational(intent):
                    response = self.chat_handler.respond(cmd)
                    self.safe_log(f"<span style='color: {COLORS['success']}'>└─ {response}</span>")
                else:
                    self.agent.run(cmd, intent)
                
            except Exception as e:
                self.safe_log(f"<span style='color: {COLORS['error']}'>❌ {str(e)}</span>")
            finally:
                self.is_executing = False
                self.exec_btn.setEnabled(True)
                self.cmd_input.setEnabled(True)
                self.cmd_input.clear()
                self.cmd_input.setFocus()
                self.status_dot.setStyleSheet(f"color: {COLORS['success']}; background: transparent; border: none;")
        
        threading.Thread(target=run, daemon=True).start()
    
    def safe_log(self, msg):
        """Thread-safe log"""
        self.log_signal.emit(msg)
    
    def add_log(self, msg):
        """Add to log"""
        self.log.append(msg)
        self.log.verticalScrollBar().setValue(self.log.verticalScrollBar().maximum())
    
    def mousePressEvent(self, event):
        """Enable dragging"""
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
    
    def mouseMoveEvent(self, event):
        """Move window"""
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_pos)


def main():
    app = QApplication(sys.argv)
    gui = SimpleGUI()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
