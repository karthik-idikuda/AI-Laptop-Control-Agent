"""
Ultimate Futuristic GUI with Live AI Thinking Animation
Shows real-time AI thought process with robotic animations
"""

import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QFrame, QGraphicsDropShadowEffect,
    QGraphicsOpacityEffect, QProgressBar
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QPoint, QPropertyAnimation, QEasingCurve, QSequentialAnimationGroup, QRect, QSize
from PyQt5.QtGui import QFont, QColor, QPalette, QPainter, QPen, QLinearGradient, QBrush, QRadialGradient
import threading
import random
from datetime import datetime

from agent import OSAgent
from intent_analyzer import IntentAnalyzer
from chat_handler import ChatHandler


class ThinkingVisualization(QFrame):
    """Animated neural network visualization showing AI thinking"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(120)
        self.nodes = []
        self.connections = []
        self.thinking = False
        self.pulse_phase = 0
        
        # Generate neural network structure
        self._generate_network()
        
        # Animation timer
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_animation)
        self.timer.start(50)  # 20 FPS
        
        # Style
        self.setStyleSheet("""
            QFrame {
                background: rgba(10, 14, 39, 0.8);
                border: 1px solid rgba(102, 126, 234, 0.3);
                border-radius: 10px;
            }
        """)
    
    def _generate_network(self):
        """Generate neural network node positions"""
        width = 340
        height = 100
        
        # Input layer (left)
        for i in range(3):
            self.nodes.append({
                'x': 30,
                'y': 20 + i * 30,
                'active': 0.0,
                'layer': 'input'
            })
        
        # Hidden layer (middle)
        for i in range(5):
            self.nodes.append({
                'x': width // 2,
                'y': 10 + i * 20,
                'active': 0.0,
                'layer': 'hidden'
            })
        
        # Output layer (right)
        for i in range(3):
            self.nodes.append({
                'x': width - 30,
                'y': 20 + i * 30,
                'active': 0.0,
                'layer': 'output'
            })
        
        # Generate connections
        for i in range(3):  # Input to hidden
            for j in range(3, 8):
                self.connections.append({
                    'from': i,
                    'to': j,
                    'strength': 0.0
                })
        
        for i in range(3, 8):  # Hidden to output
            for j in range(8, 11):
                self.connections.append({
                    'from': i,
                    'to': j,
                    'strength': 0.0
                })
    
    def start_thinking(self):
        """Start thinking animation"""
        self.thinking = True
    
    def stop_thinking(self):
        """Stop thinking animation"""
        self.thinking = False
        # Fade out all nodes
        for node in self.nodes:
            node['active'] *= 0.9
        for conn in self.connections:
            conn['strength'] *= 0.9
    
    def _update_animation(self):
        """Update animation frame"""
        if self.thinking:
            self.pulse_phase += 0.1
            
            # Activate nodes in wave pattern
            for node in self.nodes:
                # Random activation with wave
                base_active = random.random() * 0.3
                wave = (1 + abs(((self.pulse_phase + node['y']/10) % 2) - 1)) * 0.7
                node['active'] = min(1.0, base_active + wave)
            
            # Activate connections
            for conn in self.connections:
                from_node = self.nodes[conn['from']]
                to_node = self.nodes[conn['to']]
                conn['strength'] = (from_node['active'] + to_node['active']) / 2
        else:
            # Fade out
            self.pulse_phase *= 0.95
            for node in self.nodes:
                node['active'] *= 0.85
            for conn in self.connections:
                conn['strength'] *= 0.85
        
        self.update()  # Trigger repaint
    
    def paintEvent(self, event):
        """Paint the neural network"""
        super().paintEvent(event)
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw connections
        for conn in self.connections:
            from_node = self.nodes[conn['from']]
            to_node = self.nodes[conn['to']]
            
            strength = int(conn['strength'] * 255)
            color = QColor(102, 126, 234, strength // 2)
            pen = QPen(color, 1.5)
            painter.setPen(pen)
            
            painter.drawLine(
                int(from_node['x']), int(from_node['y']),
                int(to_node['x']), int(to_node['y'])
            )
        
        # Draw nodes
        for node in self.nodes:
            # Node glow
            if node['active'] > 0.1:
                glow_radius = 8 + int(node['active'] * 6)
                gradient = QRadialGradient(node['x'], node['y'], glow_radius)
                alpha = int(node['active'] * 100)
                gradient.setColorAt(0, QColor(102, 126, 234, alpha))
                gradient.setColorAt(1, QColor(102, 126, 234, 0))
                painter.setBrush(QBrush(gradient))
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(
                    int(node['x'] - glow_radius),
                    int(node['y'] - glow_radius),
                    glow_radius * 2,
                    glow_radius * 2
                )
            
            # Node core
            alpha = int(50 + node['active'] * 205)
            if node['layer'] == 'input':
                color = QColor(0, 255, 136, alpha)
            elif node['layer'] == 'output':
                color = QColor(255, 59, 92, alpha)
            else:
                color = QColor(102, 126, 234, alpha)
            
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(int(node['x'] - 4), int(node['y'] - 4), 8, 8)


class ThinkingText(QLabel):
    """Animated text showing current thought"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.thoughts = []
        self.current_index = 0
        self.setFont(QFont('Monaco', 9))
        self.setStyleSheet("color: #00ff88; background: transparent;")
        self.setWordWrap(True)
        self.setMinimumHeight(40)
        
        # Typing animation
        self.current_text = ""
        self.target_text = ""
        self.char_index = 0
        
        self.timer = QTimer()
        self.timer.timeout.connect(self._type_next_char)
    
    def set_thought(self, thought: str):
        """Set new thought to display"""
        self.target_text = f"💭 {thought}"
        self.current_text = ""
        self.char_index = 0
        self.timer.start(30)  # Type speed
    
    def _type_next_char(self):
        """Type next character"""
        if self.char_index < len(self.target_text):
            self.current_text += self.target_text[self.char_index]
            self.setText(self.current_text + "▊")  # Cursor
            self.char_index += 1
        else:
            self.setText(self.current_text)  # Remove cursor
            self.timer.stop()


class RoboticGUI(QMainWindow):
    """Ultimate futuristic GUI with live AI thinking visualization"""
    
    log_signal = pyqtSignal(str)
    status_signal = pyqtSignal(str)
    thinking_signal = pyqtSignal(bool)
    thought_signal = pyqtSignal(str)
    
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
        self.thinking_signal.connect(self.update_thinking)
        self.thought_signal.connect(self.update_thought)
        
    def initUI(self):
        """Build ultimate futuristic UI"""
        self.setWindowTitle('🤖 AI Brain')
        
        # Position: TOP-RIGHT CORNER
        screen = QApplication.desktop().screenGeometry()
        w, h = 360, 600
        x = screen.width() - w - 20
        y = 20
        
        self.setGeometry(x, y, w, h)
        self.setFixedWidth(w)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.95)
        
        # Main Container
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #000814, stop:0.5 #001d3d, stop:1 #000814);
                border: 2px solid;
                border-image: linear-gradient(135deg, #00ff88 0%, #667eea 50%, #00ff88 100%);
                border-radius: 16px;
            }
        """)
        
        # Glow
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(40)
        glow.setColor(QColor(0, 255, 136, 100))
        glow.setOffset(0, 0)
        container.setGraphicsEffect(glow)
        
        self.setCentralWidget(container)
        layout = QVBoxLayout(container)
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # === HEADER ===
        header = QHBoxLayout()
        
        # AI Icon
        icon_label = QLabel('🤖')
        icon_label.setFont(QFont('Arial', 28))
        icon_label.setStyleSheet("background: transparent;")
        header.addWidget(icon_label)
        
        # Title
        title_box = QVBoxLayout()
        title = QLabel('AI NEURAL CORE')
        title.setFont(QFont('Helvetica Neue', 13, QFont.Bold))
        title.setStyleSheet("""
            color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #00ff88, stop:1 #667eea);
            background: transparent;
        """)
        title_box.addWidget(title)
        
        subtitle = QLabel('Autonomous Intelligence System')
        subtitle.setFont(QFont('Helvetica Neue', 7))
        subtitle.setStyleSheet("color: #667eea; background: transparent;")
        title_box.addWidget(subtitle)
        
        header.addLayout(title_box)
        header.addStretch()
        
        # Close button
        close_btn = QPushButton('×')
        close_btn.setFixedSize(24, 24)
        close_btn.clicked.connect(self.close)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 59, 92, 0.2);
                color: #ff3b5c;
                border: 1px solid #ff3b5c;
                border-radius: 12px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(255, 59, 92, 0.4);
            }
        """)
        header.addWidget(close_btn)
        
        layout.addLayout(header)
        
        # === THINKING VISUALIZATION ===
        thinking_label = QLabel('⚡ NEURAL ACTIVITY')
        thinking_label.setFont(QFont('Helvetica Neue', 8, QFont.Bold))
        thinking_label.setStyleSheet("color: #00ff88; background: transparent;")
        layout.addWidget(thinking_label)
        
        self.thinking_viz = ThinkingVisualization()
        layout.addWidget(self.thinking_viz)
        
        # === CURRENT THOUGHT ===
        self.thinking_text = ThinkingText()
        layout.addWidget(self.thinking_text)
        
        # === STATUS ===
        status_row = QHBoxLayout()
        status_row.setSpacing(8)
        
        self.status_dot = QLabel('●')
        self.status_dot.setFont(QFont('Arial', 14))
        self.status_dot.setStyleSheet("color: #00ff88; background: transparent;")
        status_row.addWidget(self.status_dot)
        
        self.status_label = QLabel('READY')
        self.status_label.setFont(QFont('Helvetica Neue', 9, QFont.Bold))
        self.status_label.setStyleSheet("color: #00ff88; background: transparent;")
        status_row.addWidget(self.status_label)
        
        status_row.addStretch()
        layout.addLayout(status_row)
        
        # === LOG ===
        log_label = QLabel('📊 ACTIVITY LOG')
        log_label.setFont(QFont('Helvetica Neue', 8, QFont.Bold))
        log_label.setStyleSheet("color: #667eea; background: transparent;")
        layout.addWidget(log_label)
        
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setFont(QFont('Monaco', 8))
        self.log.setStyleSheet("""
            QTextEdit {
                background: rgba(0, 8, 20, 0.8);
                color: #00ff88;
                border: 1px solid rgba(0, 255, 136, 0.3);
                border-radius: 8px;
                padding: 8px;
            }
            QScrollBar:vertical {
                background: rgba(0, 0, 0, 0.3);
                width: 6px;
                border-radius: 3px;
            }
            QScrollBar::handle:vertical {
                background: rgba(0, 255, 136, 0.5);
                border-radius: 3px;
            }
        """)
        layout.addWidget(self.log)
        
        # === INPUT ===
        input_label = QLabel('⚙️ COMMAND INPUT')
        input_label.setFont(QFont('Helvetica Neue', 8, QFont.Bold))
        input_label.setStyleSheet("color: #667eea; background: transparent;")
        layout.addWidget(input_label)
        
        self.cmd_input = QLineEdit()
        self.cmd_input.setPlaceholderText('Enter neural command...')
        self.cmd_input.setFont(QFont('Helvetica Neue', 10))
        self.cmd_input.returnPressed.connect(self.execute)
        self.cmd_input.setStyleSheet("""
            QLineEdit {
                background: rgba(0, 29, 61, 0.8);
                color: #ffffff;
                border: 2px solid rgba(0, 255, 136, 0.3);
                border-radius: 8px;
                padding: 10px 14px;
            }
            QLineEdit:focus {
                border: 2px solid rgba(0, 255, 136, 0.8);
                background: rgba(0, 29, 61, 1);
            }
        """)
        layout.addWidget(self.cmd_input)
        
        # === BUTTONS ===
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)
        
        self.execute_btn = QPushButton('⚡ EXECUTE')
        self.execute_btn.clicked.connect(self.execute)
        self.execute_btn.setCursor(Qt.PointingHandCursor)
        self.execute_btn.setFont(QFont('Helvetica Neue', 9, QFont.Bold))
        self.execute_btn.setFixedHeight(40)
        self.execute_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00ff88, stop:1 #667eea);
                color: #000;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #00ff88);
            }
            QPushButton:disabled {
                background: rgba(102, 126, 234, 0.3);
                color: rgba(0, 0, 0, 0.4);
            }
        """)
        btn_row.addWidget(self.execute_btn)
        
        self.stop_btn = QPushButton('■ STOP')
        self.stop_btn.clicked.connect(self.stop)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setCursor(Qt.PointingHandCursor)
        self.stop_btn.setFont(QFont('Helvetica Neue', 9, QFont.Bold))
        self.stop_btn.setFixedHeight(40)
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 59, 92, 0.3);
                color: #ff3b5c;
                border: 2px solid #ff3b5c;
                border-radius: 8px;
            }
            QPushButton:hover {
                background: rgba(255, 59, 92, 0.5);
            }
            QPushButton:disabled {
                background: rgba(255, 59, 92, 0.1);
                border: 2px solid rgba(255, 59, 92, 0.2);
                color: rgba(255, 59, 92, 0.3);
            }
        """)
        btn_row.addWidget(self.stop_btn)
        
        layout.addLayout(btn_row)
    
    def execute(self):
        """Execute command with live thinking visualization"""
        cmd = self.cmd_input.text().strip()
        if not cmd:
            return
        
        self.is_executing = True
        self.execute_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.cmd_input.setEnabled(False)
        self.status_signal.emit("processing")
        self.thinking_signal.emit(True)
        
        self.safe_log(f"<span style='color: #00ff88'>▶</span> <span style='color: #ffffff'>{cmd}</span>")
        
        def run():
            try:
                # Simulate thinking steps
                self.thought_signal.emit("Analyzing command structure...")
                time.sleep(0.5)
                
                intent = self.intent_analyzer.analyze(cmd)
                self.thought_signal.emit("Understanding user intent...")
                time.sleep(0.5)
                
                self.safe_log(f"<span style='color: #667eea'>├─ Intent:</span> <span style='color: #00ff88'>{intent.get('intent_type')}</span>")
                
                if self.intent_analyzer.is_conversational(intent):
                    self.thought_signal.emit("Generating natural response...")
                    time.sleep(0.3)
                    response = self.chat_handler.respond(cmd)
                    self.safe_log(f"<span style='color: #00ff88'>└─ 💬</span> <span style='color: #ffffff'>{response}</span>")
                else:
                    self.thought_signal.emit("Planning execution strategy...")
                    time.sleep(0.5)
                    self.thought_signal.emit("Executing automated actions...")
                    self.agent.run(cmd, intent)
                
                self.status_signal.emit("complete")
                self.thinking_signal.emit(False)
            except Exception as e:
                self.safe_log(f"<span style='color: #ff3b5c'>❌ Error:</span> <span style='color: #ff8fa3'>{str(e)}</span>")
                self.status_signal.emit("error")
                self.thinking_signal.emit(False)
            finally:
                self.is_executing = False
                self.execute_btn.setEnabled(True)
                self.stop_btn.setEnabled(False)
                self.cmd_input.setEnabled(True)
                self.cmd_input.clear()
                self.cmd_input.setFocus()
        
        threading.Thread(target=run, daemon=True).start()
    
    def stop(self):
        """Stop execution"""
        if self.agent:
            self.agent.stop_flag = True
        self.thinking_signal.emit(False)
        self.safe_log("<span style='color: #ff3b5c'>■ Stopped by user</span>")
    
    def safe_log(self, msg):
        """Thread-safe log"""
        self.log_signal.emit(msg)
    
    def add_log(self, msg):
        """Add to log with timestamp"""
        t = datetime.now().strftime("%H:%M:%S")
        self.log.append(f"<span style='color: #667eea'>[{t}]</span> {msg}")
        self.log.verticalScrollBar().setValue(self.log.verticalScrollBar().maximum())
    
    def update_status(self, status):
        """Update status with animations"""
        states = {
            "idle": ("#00ff88", "READY"),
            "processing": ("#ffaa00", "THINKING"),
            "error": ("#ff3b5c", "ERROR"),
            "complete": ("#00ff88", "COMPLETE")
        }
        
        color, text = states.get(status, ("#00ff88", "READY"))
        
        self.status_dot.setStyleSheet(f"color: {color}; background: transparent;")
        self.status_label.setText(text)
        self.status_label.setStyleSheet(f"color: {color}; background: transparent;")
    
    def update_thinking(self, thinking: bool):
        """Update thinking animation"""
        if thinking:
            self.thinking_viz.start_thinking()
        else:
            self.thinking_viz.stop_thinking()
            self.thinking_text.set_thought("Idle...")
    
    def update_thought(self, thought: str):
        """Update current thought"""
        self.thinking_text.set_thought(thought)
    
    def mousePressEvent(self, event):
        """Drag start"""
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
    
    def mouseMoveEvent(self, event):
        """Drag move"""
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_pos)


def main():
    """Launch Robotic AI GUI"""
    app = QApplication(sys.argv)
    gui = RoboticGUI()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
