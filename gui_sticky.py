
"""
Sticky Animated GUI - Always On Top & Brainstorming
Combines sticky positioning with live brainstorming animations
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import threading
import random
import time
import math
from datetime import datetime

from agent import OSAgent
from intent_analyzer import IntentAnalyzer
from chat_handler import ChatHandler

# Solid Color Palette (Cyberpunk Clean)
COLORS = {
    'bg': '#0f0f0f',        # Deep Black
    'header': '#1a1a1a',    # Dark Grey
    'accent': '#00ff9d',    # Neon Green
    'secondary': '#00d2ff', # Neon Blue
    'text': '#ffffff',      # White
    'text_dim': '#888888',  # Grey
    'border': '#333333',    # Dark Border
    'error': '#ff3366',     # Neon Red
}

class GyroCoreEffect(QWidget):
    """3D Robotic Gyroscope Animation"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(100)
        self.active = False
        self.angle_x = 0
        self.angle_y = 0
        self.angle_z = 0
        
        self.particles = []
        for _ in range(15):
            self.particles.append({
                'x': random.randint(0, 300),
                'y': random.randint(0, 100),
                'size': random.randint(1, 3),
                'speed': random.uniform(0.5, 2.0)
            })
            
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(20)  # 50 FPS for smoothness

    def start_thinking(self):
        self.active = True
        
    def stop_thinking(self):
        self.active = False
        self.update()

    def update_animation(self):
        # Smooth rotation
        speed = 2 if self.active else 0.5
        self.angle_x = (self.angle_x + 1 * speed) % 360
        self.angle_y = (self.angle_y + 1.5 * speed) % 360
        self.angle_z = (self.angle_z + 0.5 * speed) % 360
        
        # Update particles
        for p in self.particles:
            p['y'] -= p['speed']
            if p['y'] < 0:
                p['y'] = 100
                p['x'] = random.randint(0, 300)
                
        self.update()

    def project_3d(self, x, y, z, scale):
        """Simple 3D projection"""
        return x, y

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Background
        painter.fillRect(self.rect(), QColor(COLORS['header']))
        
        cx, cy = self.width() // 2, self.height() // 2
        
        # Colors
        core_color = QColor(COLORS['secondary'])
        ring_color = QColor(COLORS['accent'])
        
        if self.active:
            core_color = QColor(COLORS['error']) # Red when active
            
        # Draw Particles (Background)
        painter.setPen(Qt.NoPen)
        for p in self.particles:
            alpha = int(255 * (p['y'] / 100))
            color = QColor(core_color)
            color.setAlpha(alpha)
            painter.setBrush(QBrush(color))
            painter.drawEllipse(int(p['x']), int(p['y']), p['size'], p['size'])
            
        # Draw 3D Rings (Simulated with ellipses)
        painter.setBrush(Qt.NoBrush)
        
        # Ring 1 (X-Axis Rotation)
        pen = QPen(ring_color)
        pen.setWidth(2)
        painter.setPen(pen)
        
        h1 = 30 * math.cos(math.radians(self.angle_x))
        painter.drawEllipse(QPoint(cx, cy), 40, abs(int(h1)) + 10)
        
        # Ring 2 (Y-Axis Rotation)
        pen.setColor(QColor(COLORS['secondary']))
        painter.setPen(pen)
        w2 = 30 * math.cos(math.radians(self.angle_y))
        painter.drawEllipse(QPoint(cx, cy), abs(int(w2)) + 10, 40)
        
        # Ring 3 (Z-Axis / Outer)
        pen.setColor(QColor(COLORS['text_dim']))
        pen.setStyle(Qt.DotLine)
        painter.setPen(pen)
        painter.drawEllipse(QPoint(cx, cy), 50, 50)
        
        # Central Core (Sphere)
        painter.setPen(Qt.NoPen)
        
        # Core Glow
        glow = QRadialGradient(cx, cy, 25)
        glow.setColorAt(0, core_color)
        glow.setColorAt(1, Qt.transparent)
        painter.setBrush(QBrush(glow))
        painter.drawEllipse(QPoint(cx, cy), 25, 25)
        
        # Solid Core
        painter.setBrush(QBrush(Qt.white))
        core_size = 6 + math.sin(math.radians(self.angle_x * 4)) * 2
        painter.drawEllipse(QPointF(cx, cy), core_size, core_size)
        
        # Scanning Laser (if active)
        if self.active:
            painter.setPen(QPen(core_color, 2))
            scan_x = cx + 40 * math.cos(math.radians(self.angle_z * 5))
            painter.drawLine(QPointF(cx, cy), QPointF(scan_x, cy))

class AgentWorker(QThread):
    """Worker thread for agent execution"""
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()
    
    def __init__(self, agent, cmd, intent_analyzer, chat_handler):
        super().__init__()
        self.agent = agent
        self.cmd = cmd
        self.intent_analyzer = intent_analyzer
        self.chat_handler = chat_handler
        
    def run(self):
        try:
            intent = self.intent_analyzer.analyze(self.cmd)
            if self.intent_analyzer.is_conversational(intent):
                response = self.chat_handler.respond(self.cmd)
                self.log_signal.emit(f"<span style='color: {COLORS['secondary']}'>└─ {response}</span>")
            else:
                self.agent.run(self.cmd, intent)
        except Exception as e:
            self.log_signal.emit(f"<span style='color: {COLORS['error']}'>❌ {str(e)}</span>")
        finally:
            self.finished_signal.emit()


class StickyGUI(QMainWindow):
    """Always-on-top, animated, sticky GUI"""
    
    log_signal = pyqtSignal(str)
    status_signal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.is_executing = False
        self.drag_pos = QPoint()
        
        self.agent = OSAgent(logger_callback=self.safe_log)
        self.intent_analyzer = IntentAnalyzer()
        self.chat_handler = ChatHandler()
        
        self.log_signal.connect(self.add_log)
        self.status_signal.connect(self.update_status)
        
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('AI Agent')
        
        # Sticky Top Right
        screen = QApplication.desktop().screenGeometry()
        w, h = 320, 500
        x = screen.width() - w - 20
        y = 30
        
        self.setGeometry(x, y, w, h)
        self.setFixedSize(w, h)
        
        # CRITICAL: Robust Always on Top for macOS
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint | 
            Qt.FramelessWindowHint | 
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        # self.setAttribute(Qt.WA_ShowWithoutActivating)  # Removed to allow focus for typing
        
        # macOS Specific: Force Floating Level
        try:
            import objc
            from AppKit import NSWindow, NSFloatingWindowLevel, NSMainMenuWindowLevel
            
            # Get the NSWindow from the PyQt window ID
            ns_view = objc.objc_object(c_void_p=int(self.winId()))
            ns_window = ns_view.window()
            
            # Set level higher than normal floating windows (like Spotlight)
            ns_window.setLevel_(NSMainMenuWindowLevel + 1)
            
            # Prevent hiding when app deactivates
            ns_window.setHidesOnDeactivate_(False)
            
            # Make it join all spaces (visible on all desktops)
            ns_window.setCollectionBehavior_(1 << 0)  # NSWindowCollectionBehaviorCanJoinAllSpaces
            
        except Exception as e:
            print(f"macOS specific window setup failed: {e}")
            # Fallback is already set by Qt flags
        
        # Lock Position Timer
        self.pos_timer = QTimer()
        self.pos_timer.timeout.connect(self._enforce_position)
        self.pos_timer.start(100)  # Check every 100ms
        
        # Store target position
        self.target_pos = QPoint(x, y)
        
        # Main Container
        container = QFrame()
        container.setStyleSheet(f"""
            QFrame {{
                background: {COLORS['bg']};
                border: 2px solid {COLORS['accent']};
                border-radius: 10px;
            }}
        """)
        
        # Glow Effect
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(20)
        glow.setColor(QColor(COLORS['accent']))
        glow.setOffset(0, 0)
        container.setGraphicsEffect(glow)
        
        self.setCentralWidget(container)
        layout = QVBoxLayout(container)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Header
        header = QHBoxLayout()
        
        self.status_dot = QLabel('●')
        self.status_dot.setFont(QFont('Arial', 14))
        self.status_dot.setStyleSheet(f"color: {COLORS['accent']}; background: transparent; border: none;")
        header.addWidget(self.status_dot)
        
        title = QLabel('AI BRAIN')
        title.setFont(QFont('Helvetica Neue', 12, QFont.Bold))
        title.setStyleSheet(f"color: {COLORS['text']}; background: transparent; border: none;")
        header.addWidget(title)
        
        header.addStretch()
        
        close_btn = QPushButton('×')
        close_btn.setFixedSize(24, 24)
        close_btn.clicked.connect(self.close)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {COLORS['text_dim']};
                border: 1px solid {COLORS['text_dim']};
                border-radius: 12px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                color: {COLORS['error']};
                border-color: {COLORS['error']};
            }}
        """)
        header.addWidget(close_btn)
        layout.addLayout(header)
        
        # Brainstorming Animation
        self.brain = GyroCoreEffect()
        layout.addWidget(self.brain)
        
        # Log Area
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setFont(QFont('Menlo', 10))
        self.log.setStyleSheet(f"""
            QTextEdit {{
                background: {COLORS['header']};
                color: {COLORS['text']};
                border: none;
                border-radius: 4px;
                padding: 5px;
            }}
        """)
        layout.addWidget(self.log)
        
        # Input
        self.cmd_input = QLineEdit()
        self.cmd_input.setPlaceholderText('Ask me anything...')
        self.cmd_input.setFont(QFont('Helvetica Neue', 11))
        self.cmd_input.returnPressed.connect(self.execute)
        self.cmd_input.setStyleSheet(f"""
            QLineEdit {{
                background: {COLORS['header']};
                color: {COLORS['text']};
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                padding: 8px;
            }}
            QLineEdit:focus {{
                border: 1px solid {COLORS['accent']};
            }}
        """)
        layout.addWidget(self.cmd_input)
        
        # Execute Button
        self.exec_btn = QPushButton('⚡ EXECUTE')
        self.exec_btn.clicked.connect(self.execute)
        self.exec_btn.setCursor(Qt.PointingHandCursor)
        self.exec_btn.setFont(QFont('Helvetica Neue', 11, QFont.Bold))
        self.exec_btn.setFixedHeight(36)
        self.exec_btn.setStyleSheet(f"""
            QPushButton {{
                background: {COLORS['accent']};
                color: {COLORS['bg']};
                border: none;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background: {COLORS['secondary']};
            }}
            QPushButton:disabled {{
                background: {COLORS['border']};
                color: {COLORS['text_dim']};
            }}
        """)
        layout.addWidget(self.exec_btn)
        


    def execute(self):
        cmd = self.cmd_input.text().strip()
        if not cmd or self.is_executing: return
        
        self.is_executing = True
        self.exec_btn.setEnabled(False)
        self.cmd_input.setEnabled(False)
        self.brain.start_thinking()
        self.status_signal.emit("thinking")
        
        self.safe_log(f"<span style='color: {COLORS['accent']}'>▶ {cmd}</span>")
        
        # Use QThread Worker
        self.worker = AgentWorker(self.agent, cmd, self.intent_analyzer, self.chat_handler)
        self.worker.log_signal.connect(self.safe_log)
        self.worker.finished_signal.connect(self.on_execution_finished)
        self.worker.start()
        
    def on_execution_finished(self):
        self.is_executing = False
        self.exec_btn.setEnabled(True)
        self.cmd_input.setEnabled(True)
        self.cmd_input.clear()
        self.cmd_input.setFocus()
        self.brain.stop_thinking()
        self.status_signal.emit("idle")
        
    def safe_log(self, msg):
        self.log_signal.emit(msg)
        
    def add_log(self, msg):
        self.log.append(msg)
        self.log.verticalScrollBar().setValue(self.log.verticalScrollBar().maximum())
        
    def update_status(self, status):
        color = COLORS['secondary'] if status == "thinking" else COLORS['accent']
        self.status_dot.setStyleSheet(f"color: {color}; background: transparent; border: none;")

    def _enforce_position(self):
        """Force window to stay at target position"""
        if self.pos() != self.target_pos:
            self.move(self.target_pos)
            self.raise_()  # Keep raising to top

    def mousePressEvent(self, event):
        # Disable dragging to keep it sticky
        pass
    
    def mouseMoveEvent(self, event):
        # Disable dragging
        pass

def main():
    app = QApplication(sys.argv)
    gui = StickyGUI()
    gui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
