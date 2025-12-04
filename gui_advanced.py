"""
Professional Modern GUI - Sleek & Functional
Safe positioning (away from corners) to prevent PyAutoGUI fail-safe.
"""

import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QFrame, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QPoint
from PyQt5.QtGui import QFont, QColor, QPalette
import threading
from datetime import datetime

from agent import OSAgent
from intent_analyzer import IntentAnalyzer
from chat_handler import ChatHandler


class ProfessionalGUI(QMainWindow):
    """Sleek professional GUI with modern slate theme"""
    
    log_signal = pyqtSignal(str)
    status_signal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.is_executing = False
        self.drag_pos = QPoint()
        
        self.initUI()
        
        self.agent = OSAgent(logger_callback=self.safe_log)
        self.intent_analyzer = IntentAnalyzer()
        self.chat_handler = ChatHandler()
        
        self.log_signal.connect(self.add_log)
        self.status_signal.connect(self.update_status)
        
    def initUI(self):
        """Modern professional UI"""
        self.setWindowTitle('OS Agent Pro')
        
        # Position: TOP-RIGHT CORNER (macOS style)
        screen = QApplication.desktop().screenGeometry()
        w, h = 360, 500
        x = screen.width() - w - 20  # 20px from right edge
        y = 20  # 20px from top edge (below menu bar)
        
        self.setGeometry(x, y, w, h)
        self.setFixedWidth(w)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.95)  # Slight transparency for macOS style
        
        # Main Container with Shadow
        container = QFrame()
        container.setObjectName("main")
        # Slate 900 background, Slate 700 border
        container.setStyleSheet("""
            #main {
                background-color: #0f172a; 
                border: 1px solid #334155;
                border-radius: 12px;
            }
        """)
        
        # Drop shadow for depth
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(0, 4)
        container.setGraphicsEffect(shadow)
        
        self.setCentralWidget(container)
        layout = QVBoxLayout(container)
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # === HEADER ===
        header = QHBoxLayout()
        
        # Title
        title_box = QVBoxLayout()
        title_box.setSpacing(2)
        
        app_title = QLabel('OS AGENT')
        app_title.setFont(QFont('Helvetica Neue', 12, QFont.Bold))
        app_title.setStyleSheet("color: #f8fafc;") # Slate 50
        title_box.addWidget(app_title)
        
        subtitle = QLabel('Professional Edition')
        subtitle.setFont(QFont('Helvetica Neue', 8))
        subtitle.setStyleSheet("color: #94a3b8;") # Slate 400
        title_box.addWidget(subtitle)
        
        header.addLayout(title_box)
        header.addStretch()
        
        # Status Indicator
        self.status_dot = QLabel('●')
        self.status_dot.setFont(QFont('Arial', 14))
        self.status_dot.setStyleSheet("color: #10b981;") # Emerald 500
        header.addWidget(self.status_dot)
        
        self.status_text = QLabel('Ready')
        self.status_text.setFont(QFont('Helvetica Neue', 9, QFont.Bold))
        self.status_text.setStyleSheet("color: #10b981;")
        header.addWidget(self.status_text)
        
        # Close Button
        close_btn = QPushButton('×')
        close_btn.setFixedSize(24, 24)
        close_btn.clicked.connect(self.close)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #64748b;
                border: none;
                font-size: 20px;
                font-weight: bold;
                padding-bottom: 4px;
            }
            QPushButton:hover { color: #ef4444; }
        """)
        header.addWidget(close_btn)
        
        layout.addLayout(header)
        
        # Separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: #334155; height: 1px; border: none;")
        layout.addWidget(line)
        
        # === LOG AREA ===
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setFont(QFont('Monaco', 9))  # Monaco is macOS default monospace font
        self.log.setStyleSheet("""
            QTextEdit {
                background-color: #1e293b; /* Slate 800 */
                color: #e2e8f0; /* Slate 200 */
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 8px;
            }
        """)
        layout.addWidget(self.log)
        
        # === CONTROLS ===
        controls = QVBoxLayout()
        controls.setSpacing(10)
        
        # Input Field
        self.cmd_input = QLineEdit()
        self.cmd_input.setPlaceholderText('Type a command...')
        self.cmd_input.setFont(QFont('Helvetica Neue', 10))
        self.cmd_input.returnPressed.connect(self.execute)
        self.cmd_input.setStyleSheet("""
            QLineEdit {
                background-color: #1e293b;
                color: white;
                border: 1px solid #475569;
                border-radius: 6px;
                padding: 10px;
            }
            QLineEdit:focus {
                border: 1px solid #38bdf8; /* Sky 400 */
                background-color: #0f172a;
            }
        """)
        controls.addWidget(self.cmd_input)
        
        # Action Buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)
        
        self.go_btn = QPushButton('Execute')
        self.go_btn.clicked.connect(self.execute)
        self.go_btn.setCursor(Qt.PointingHandCursor)
        self.go_btn.setFont(QFont('Helvetica Neue', 9, QFont.Bold))
        self.go_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6; /* Blue 500 */
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px;
            }
            QPushButton:hover { background-color: #2563eb; }
            QPushButton:disabled { background-color: #475569; color: #94a3b8; }
        """)
        btn_row.addWidget(self.go_btn)
        
        self.stop_btn = QPushButton('Stop')
        self.stop_btn.clicked.connect(self.stop)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setCursor(Qt.PointingHandCursor)
        self.stop_btn.setFont(QFont('Helvetica Neue', 9, QFont.Bold))
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #ef4444; /* Red 500 */
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px;
            }
            QPushButton:hover { background-color: #dc2626; }
            QPushButton:disabled { background-color: #475569; color: #94a3b8; }
        """)
        btn_row.addWidget(self.stop_btn)
        
        controls.addLayout(btn_row)
        layout.addLayout(controls)
        
    def execute(self):
        """Execute command"""
        cmd = self.cmd_input.text().strip()
        if not cmd:
            return
        
        self.is_executing = True
        self.go_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.cmd_input.setEnabled(False)
        self.status_signal.emit("running")
        
        self.safe_log(f"▶ {cmd}")
        
        def run():
            try:
                intent = self.intent_analyzer.analyze(cmd)
                self.safe_log(f"  Intent: {intent.get('intent_type')}")
                
                if self.intent_analyzer.is_conversational(intent):
                    response = self.chat_handler.respond(cmd)
                    self.safe_log(f"  💬 {response}")
                else:
                    self.agent.run(cmd, intent)
                
                self.status_signal.emit("done")
            except Exception as e:
                self.safe_log(f"  ❌ Error: {str(e)}")
                self.status_signal.emit("error")
            finally:
                self.is_executing = False
                self.go_btn.setEnabled(True)
                self.stop_btn.setEnabled(False)
                self.cmd_input.setEnabled(True)
                self.cmd_input.clear()
                self.cmd_input.setFocus()
        
        threading.Thread(target=run, daemon=True).start()
    
    def stop(self):
        """Stop execution"""
        if self.agent:
            self.agent.stop_flag = True
        self.safe_log("■ Stopped by user")
    
    def safe_log(self, msg):
        """Thread-safe log"""
        self.log_signal.emit(msg)
    
    def add_log(self, msg):
        """Add to log"""
        t = datetime.now().strftime("%H:%M:%S")
        self.log.append(f"<span style='color: #64748b'>[{t}]</span> {msg}")
        self.log.verticalScrollBar().setValue(
            self.log.verticalScrollBar().maximum()
        )
    
    def update_status(self, status):
        """Update status indicator"""
        # (Color, Text)
        states = {
            "idle":    ("#10b981", "Ready"),    # Emerald
            "running": ("#f59e0b", "Working"),  # Amber
            "error":   ("#ef4444", "Error"),    # Red
            "done":    ("#10b981", "Done")      # Emerald
        }
        
        color, text = states.get(status, ("#10b981", "Ready"))
        
        self.status_dot.setStyleSheet(f"color: {color};")
        self.status_text.setText(text)
        self.status_text.setStyleSheet(f"color: {color};")
    
    def mousePressEvent(self, event):
        """Drag start"""
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
    
    def mouseMoveEvent(self, event):
        """Drag move"""
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_pos)


def main():
    """Launch Professional GUI"""
    app = QApplication(sys.argv)
    
    # Set application-wide font (macOS)
    font = QFont("Helvetica Neue", 9)
    app.setFont(font)
    
    gui = ProfessionalGUI()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
