"""
Futuristic Professional GUI - Brain-Storming Aesthetic
macOS optimized with animations and modern design.
"""

import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QFrame, QGraphicsDropShadowEffect,
    QGraphicsOpacityEffect
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QPoint, QPropertyAnimation, QEasingCurve, QSequentialAnimationGroup
from PyQt5.QtGui import QFont, QColor, QPalette, QLinearGradient, QPainter
import threading
from datetime import datetime

from agent import OSAgent
from intent_analyzer import IntentAnalyzer
from chat_handler import ChatHandler


class PulsingWidget(QFrame):
    """Animated pulsing effect widget"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.opacity_effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacity_effect)
        
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(2000)
        self.animation.setStartValue(0.3)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.setLoopCount(-1)  # Infinite loop
        self.animation.start()


class FuturisticGUI(QMainWindow):
    """Futuristic Brain-Storming GUI with animations"""
    
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
        
        # Start pulsing animation
        self.start_ambient_animations()
        
    def initUI(self):
        """Futuristic professional UI"""
        self.setWindowTitle('⚡ AI Agent')
        
        # Position: TOP-RIGHT CORNER (macOS style)
        screen = QApplication.desktop().screenGeometry()
        w, h = 360, 500
        x = screen.width() - w - 20
        y = 20
        
        self.setGeometry(x, y, w, h)
        self.setFixedWidth(w)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.95)
        
        # Main Container - Futuristic Dark Theme
        container = QFrame()
        container.setObjectName("main")
        container.setStyleSheet("""
            #main {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0a0e27, stop:0.5 #16213e, stop:1 #0a0e27);
                border: 2px solid;
                border-image: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 16px;
            }
        """)
        
        # Glow effect
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(30)
        glow.setColor(QColor(102, 126, 234, 80))
        glow.setOffset(0, 0)
        container.setGraphicsEffect(glow)
        
        self.setCentralWidget(container)
        layout = QVBoxLayout(container)
        layout.setSpacing(16)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # === HEADER ===
        header = QHBoxLayout()
        header.setSpacing(12)
        
        # AI Brain Icon
        brain_label = QLabel('🧠')
        brain_label.setFont(QFont('Helvetica Neue', 24))
        brain_label.setStyleSheet("""
            QLabel {
                color: #667eea;
                background: transparent;
            }
        """)
        header.addWidget(brain_label)
        
        # Title with gradient effect
        title_box = QVBoxLayout()
        title_box.setSpacing(2)
        
        app_title = QLabel('NEURAL AGENT')
        app_title.setFont(QFont('Helvetica Neue', 14, QFont.Bold))
        app_title.setStyleSheet("""
            QLabel {
                color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                background: transparent;
            }
        """)
        title_box.addWidget(app_title)
        
        subtitle = QLabel('AI-Powered Automation')
        subtitle.setFont(QFont('Helvetica Neue', 8))
        subtitle.setStyleSheet("color: #8b9dc3; background: transparent;")
        title_box.addWidget(subtitle)
        
        header.addLayout(title_box)
        header.addStretch()
        
        # Animated Status Indicator
        self.status_container = QHBoxLayout()
        self.status_container.setSpacing(8)
        
        self.status_dot = QLabel('●')
        self.status_dot.setFont(QFont('Arial', 16))
        self.status_dot.setStyleSheet("color: #00ff88; background: transparent;")
        self.status_container.addWidget(self.status_dot)
        
        self.status_text = QLabel('READY')
        self.status_text.setFont(QFont('Helvetica Neue', 9, QFont.Bold))
        self.status_text.setStyleSheet("""
            QLabel {
                color: #00ff88;
                background: transparent;
                letter-spacing: 1px;
            }
        """)
        self.status_container.addWidget(self.status_text)
        
        header.addLayout(self.status_container)
        
        # Close Button
        close_btn = QPushButton('×')
        close_btn.setFixedSize(28, 28)
        close_btn.clicked.connect(self.close)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 59, 92, 0.1);
                color: #ff3b5c;
                border: 1px solid rgba(255, 59, 92, 0.3);
                border-radius: 14px;
                font-size: 22px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(255, 59, 92, 0.2);
                border: 1px solid #ff3b5c;
            }
        """)
        header.addWidget(close_btn)
        
        layout.addLayout(header)
        
        # Separator with gradient
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFixedHeight(2)
        line.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(102, 126, 234, 0),
                    stop:0.5 rgba(102, 126, 234, 0.5),
                    stop:1 rgba(102, 126, 234, 0));
                border: none;
            }
        """)
        layout.addWidget(line)
        
        # === LOG AREA ===
        log_label = QLabel('⚡ NEURAL ACTIVITY')
        log_label.setFont(QFont('Helvetica Neue', 9, QFont.Bold))
        log_label.setStyleSheet("color: #667eea; background: transparent; letter-spacing: 1px;")
        layout.addWidget(log_label)
        
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setFont(QFont('Monaco', 9))
        self.log.setStyleSheet("""
            QTextEdit {
                background: rgba(10, 14, 39, 0.6);
                color: #00ff88;
                border: 1px solid rgba(102, 126, 234, 0.3);
                border-radius: 10px;
                padding: 12px;
                selection-background-color: rgba(102, 126, 234, 0.3);
            }
            QScrollBar:vertical {
                background: rgba(10, 14, 39, 0.3);
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: rgba(102, 126, 234, 0.5);
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(102, 126, 234, 0.8);
            }
        """)
        layout.addWidget(self.log)
        
        # === CONTROLS ===
        controls = QVBoxLayout()
        controls.setSpacing(12)
        
        # Input Field
        input_label = QLabel('💭 COMMAND INPUT')
        input_label.setFont(QFont('Helvetica Neue', 9, QFont.Bold))
        input_label.setStyleSheet("color: #8b9dc3; background: transparent; letter-spacing: 1px;")
        controls.addWidget(input_label)
        
        self.cmd_input = QLineEdit()
        self.cmd_input.setPlaceholderText('Enter neural command...')
        self.cmd_input.setFont(QFont('Helvetica Neue', 11))
        self.cmd_input.returnPressed.connect(self.execute)
        self.cmd_input.setStyleSheet("""
            QLineEdit {
                background: rgba(22, 33, 62, 0.8);
                color: #ffffff;
                border: 2px solid rgba(102, 126, 234, 0.3);
                border-radius: 10px;
                padding: 12px 16px;
            }
            QLineEdit:focus {
                border: 2px solid rgba(102, 126, 234, 0.8);
                background: rgba(22, 33, 62, 1);
            }
            QLineEdit::placeholder {
                color: rgba(139, 157, 195, 0.6);
            }
        """)
        controls.addWidget(self.cmd_input)
        
        # Action Buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)
        
        self.go_btn = QPushButton('⚡ EXECUTE')
        self.go_btn.clicked.connect(self.execute)
        self.go_btn.setCursor(Qt.PointingHandCursor)
        self.go_btn.setFont(QFont('Helvetica Neue', 10, QFont.Bold))
        self.go_btn.setFixedHeight(45)
        self.go_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #764ba2, stop:1 #667eea);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5568d3, stop:1 #6a3f8f);
            }
            QPushButton:disabled {
                background: rgba(102, 126, 234, 0.3);
                color: rgba(255, 255, 255, 0.4);
            }
        """)
        btn_row.addWidget(self.go_btn)
        
        self.stop_btn = QPushButton('■ STOP')
        self.stop_btn.clicked.connect(self.stop)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setCursor(Qt.PointingHandCursor)
        self.stop_btn.setFont(QFont('Helvetica Neue', 10, QFont.Bold))
        self.stop_btn.setFixedHeight(45)
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 59, 92, 0.2);
                color: #ff3b5c;
                border: 2px solid rgba(255, 59, 92, 0.5);
                border-radius: 10px;
                padding: 12px;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background: rgba(255, 59, 92, 0.3);
                border: 2px solid #ff3b5c;
            }
            QPushButton:pressed {
                background: rgba(255, 59, 92, 0.4);
            }
            QPushButton:disabled {
                background: rgba(255, 59, 92, 0.1);
                border: 2px solid rgba(255, 59, 92, 0.2);
                color: rgba(255, 59, 92, 0.3);
            }
        """)
        btn_row.addWidget(self.stop_btn)
        
        controls.addLayout(btn_row)
        layout.addLayout(controls)
        
    def start_ambient_animations(self):
        """Start subtle ambient animations"""
        # Pulsing status dot
        self.dot_timer = QTimer()
        self.dot_timer.timeout.connect(self.pulse_status_dot)
        self.dot_timer.start(1000)
        
    def pulse_status_dot(self):
        """Pulse the status dot"""
        if not self.is_executing:
            # Subtle pulse effect for idle state
            current = self.status_dot.styleSheet()
            if 'color: #00ff88' in current:
                self.status_dot.setStyleSheet("color: rgba(0, 255, 136, 0.6); background: transparent;")
            else:
                self.status_dot.setStyleSheet("color: #00ff88; background: transparent;")
    
    def execute(self):
        """Execute command with enhanced logging"""
        cmd = self.cmd_input.text().strip()
        if not cmd:
            return
        
        self.is_executing = True
        self.go_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.cmd_input.setEnabled(False)
        self.status_signal.emit("running")
        
        self.safe_log(f"<span style='color: #667eea'>▶</span> <span style='color: #ffffff'>{cmd}</span>")
        
        def run():
            try:
                intent = self.intent_analyzer.analyze(cmd)
                self.safe_log(f"<span style='color: #8b9dc3'>├─ Intent:</span> <span style='color: #00ff88'>{intent.get('intent_type')}</span>")
                
                if self.intent_analyzer.is_conversational(intent):
                    response = self.chat_handler.respond(cmd)
                    self.safe_log(f"<span style='color: #667eea'>└─ 💬</span> <span style='color: #ffffff'>{response}</span>")
                else:
                    self.safe_log(f"<span style='color: #8b9dc3'>└─ Executing...</span>")
                    self.agent.run(cmd, intent)
                
                self.status_signal.emit("done")
            except Exception as e:
                self.safe_log(f"<span style='color: #ff3b5c'>❌ Error:</span> <span style='color: #ff8fa3'>{str(e)}</span>")
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
        self.safe_log("<span style='color: #ff3b5c'>■ Stopped by user</span>")
    
    def safe_log(self, msg):
        """Thread-safe log"""
        self.log_signal.emit(msg)
    
    def add_log(self, msg):
        """Add to log with timestamp"""
        t = datetime.now().strftime("%H:%M:%S")
        self.log.append(f"<span style='color: #5568d3'>[{t}]</span> {msg}")
        self.log.verticalScrollBar().setValue(
            self.log.verticalScrollBar().maximum()
        )
    
    def update_status(self, status):
        """Update status indicator with animations"""
        states = {
            "idle":    ("#00ff88", "READY", "#00ff88"),
            "running": ("#ffaa00", "PROCESSING", "#ffaa00"),
            "error":   ("#ff3b5c", "ERROR", "#ff3b5c"),
            "done":    ("#00ff88", "COMPLETE", "#00ff88")
        }
        
        color, text, shadow = states.get(status, ("#00ff88", "READY", "#00ff88"))
        
        self.status_dot.setStyleSheet(f"""
            QLabel {{
                color: {color};
                background: transparent;
            }}
        """)
        self.status_text.setText(text)
        self.status_text.setStyleSheet(f"""
            QLabel {{
                color: {color};
                background: transparent;
                letter-spacing: 1px;
            }}
        """)
    
    def mousePressEvent(self, event):
        """Drag start"""
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
    
    def mouseMoveEvent(self, event):
        """Drag move"""
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_pos)


def main():
    """Launch Futuristic GUI"""
    app = QApplication(sys.argv)
    
    # Set application-wide font
    font = QFont("Helvetica Neue", 9)
    app.setFont(font)
    
    gui = FuturisticGUI()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
