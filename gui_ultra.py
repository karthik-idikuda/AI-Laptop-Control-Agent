
"""
Ultra-Animated AI GUI - Full Real-Time Live Thinking
Solid color palette with maximum animation effects
"""

import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import threading
import random
import time
from datetime import datetime

from agent import OSAgent
from intent_analyzer import IntentAnalyzer
from chat_handler import ChatHandler

# SOLID COLOR PALETTE
COLORS = {
    'bg_dark': '#0a0a0a',
    'bg_medium': '#1a1a1a',
    'bg_light': '#2a2a2a',
    'primary': '#00ff00',      # Bright green
    'secondary': '#0099ff',    # Bright blue
    'accent': '#ff00ff',       # Magenta
    'warning': '#ffaa00',      # Orange
    'error': '#ff0000',        # Red
    'text': '#ffffff',         # White
    'text_dim': '#888888',     # Gray
}


class ParticleEffect(QWidget):
    """Floating particles showing AI activity"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.particles = []
        self.active = False
        
        # Generate particles
        for _ in range(30):
            self.particles.append({
                'x': random.randint(0, 340),
                'y': random.randint(0, 100),
                'vx': random.uniform(-1, 1),
                'vy': random.uniform(-2, -0.5),
                'size': random.randint(2, 5),
                'alpha': random.randint(100, 255),
                'color': random.choice([COLORS['primary'], COLORS['secondary'], COLORS['accent']])
            })
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_particles)
        self.timer.start(33)  # 30 FPS
    
    def start_effect(self):
        self.active = True
    
    def stop_effect(self):
        self.active = False
    
    def update_particles(self):
        if self.active:
            for p in self.particles:
                p['x'] += p['vx']
                p['y'] += p['vy']
                
                # Wrap around
                if p['y'] < 0:
                    p['y'] = 100
                if p['x'] < 0:
                    p['x'] = 340
                if p['x'] > 340:
                    p['x'] = 0
                
                # Pulse alpha
                p['alpha'] = int(128 + 127 * abs(((time.time() * 2 + p['x']/10) % 2) - 1))
        else:
            # Fade out
            for p in self.particles:
                p['alpha'] = int(p['alpha'] * 0.9)
        
        self.update()
    
    def paintEvent(self, event):
        if not any(p['alpha'] > 10 for p in self.particles):
            return
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        for p in self.particles:
            if p['alpha'] > 10:
                color = QColor(p['color'])
                color.setAlpha(p['alpha'])
                painter.setBrush(QBrush(color))
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(int(p['x']), int(p['y']), p['size'], p['size'])


class ThinkingBarGraph(QWidget):
    """Animated bar graph showing thinking intensity"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(60)
        self.bars = [0.0] * 20
        self.thinking = False
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_bars)
        self.timer.start(50)
        
        self.setStyleSheet(f"background: {COLORS['bg_medium']}; border-radius: 8px;")
    
    def start_thinking(self):
        self.thinking = True
    
    def stop_thinking(self):
        self.thinking = False
    
    def update_bars(self):
        if self.thinking:
            # Wave pattern
            for i in range(len(self.bars)):
                wave = abs(((time.time() * 3 + i/2) % 2) - 1)
                self.bars[i] = wave * random.uniform(0.7, 1.0)
        else:
            # Decay
            for i in range(len(self.bars)):
                self.bars[i] *= 0.9
        
        self.update()
    
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        bar_width = self.width() / len(self.bars)
        
        for i, height in enumerate(self.bars):
            # Color based on height
            if height > 0.7:
                color = QColor(COLORS['error'])
            elif height > 0.4:
                color = QColor(COLORS['warning'])
            else:
                color = QColor(COLORS['primary'])
            
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.NoPen)
            
            bar_height = height * (self.height() - 10)
            painter.drawRect(
                int(i * bar_width + 2),
                int(self.height() - bar_height - 5),
                int(bar_width - 4),
                int(bar_height)
            )


class PulsingLabel(QLabel):
    """Label that pulses with color"""
    
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.base_color = COLORS['primary']
        self.pulse_timer = QTimer()
        self.pulse_timer.timeout.connect(self.pulse)
        self.pulse_timer.start(100)
        self.phase = 0
    
    def set_color(self, color):
        self.base_color = color
    
    def pulse(self):
        self.phase += 0.2
        intensity = int(128 + 127 * abs(((self.phase % 2) - 1)))
        color = QColor(self.base_color)
        color.setAlpha(intensity)
        self.setStyleSheet(f"color: rgba({color.red()}, {color.green()}, {color.blue()}, {intensity}); background: transparent;")


class UltraAnimatedGUI(QMainWindow):
    """Ultra-animated AI GUI with solid colors and full real-time effects"""
    
    log_signal = pyqtSignal(str)
    status_signal = pyqtSignal(str)
    thinking_signal = pyqtSignal(bool)
    thought_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        self.is_executing = False
        self.drag_pos = QPoint()
        
        self.initUI()
        
        self.agent = OSAgent(logger_callback=self.safe_log)
        self.intent_analyzer = IntentAnalyzer()
        self.chat_handler = ChatHandler()
        
        # Connect signals
        self.log_signal.connect(self.add_log)
        self.status_signal.connect(self.update_status)
        self.thinking_signal.connect(self.update_thinking)
        self.thought_signal.connect(self.update_thought)
        self.progress_signal.connect(self.update_progress)
        
        # Start ambient animations
        self.start_ambient()
    
    def initUI(self):
        """Build ultra-animated UI"""
        self.setWindowTitle('🤖 AI CORE')
        
        # Position
        screen = QApplication.desktop().screenGeometry()
        w, h = 380, 700
        x = screen.width() - w - 20
        y = 20
        
        self.setGeometry(x, y, w, h)
        self.setFixedWidth(w)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.98)
        
        # Main Container
        container = QFrame()
        container.setStyleSheet(f"""
            QFrame {{
                background: {COLORS['bg_dark']};
                border: 3px solid {COLORS['primary']};
                border-radius: 16px;
            }}
        """)
        
        # Outer glow
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(50)
        glow.setColor(QColor(COLORS['primary']))
        glow.setOffset(0, 0)
        container.setGraphicsEffect(glow)
        
        self.setCentralWidget(container)
        layout = QVBoxLayout(container)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # === HEADER ===
        header = QHBoxLayout()
        
        # Pulsing icon
        self.icon = PulsingLabel('⚡')
        self.icon.setFont(QFont('Arial', 32))
        header.addWidget(self.icon)
        
        # Title
        title_box = QVBoxLayout()
        title = QLabel('AI NEURAL CORE')
        title.setFont(QFont('Helvetica Neue', 16, QFont.Bold))
        title.setStyleSheet(f"color: {COLORS['primary']}; background: transparent;")
        title_box.addWidget(title)
        
        subtitle = QLabel('Real-Time Intelligence')
        subtitle.setFont(QFont('Helvetica Neue', 8))
        subtitle.setStyleSheet(f"color: {COLORS['secondary']}; background: transparent;")
        title_box.addWidget(subtitle)
        
        header.addLayout(title_box)
        header.addStretch()
        
        # Close
        close_btn = QPushButton('×')
        close_btn.setFixedSize(28, 28)
        close_btn.clicked.connect(self.close)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background: {COLORS['bg_medium']};
                color: {COLORS['error']};
                border: 2px solid {COLORS['error']};
                border-radius: 14px;
                font-size: 20px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background: {COLORS['error']};
                color: {COLORS['bg_dark']};
            }}
        """)
        header.addWidget(close_btn)
        
        layout.addLayout(header)
        
        # === STATUS BAR ===
        status_box = QHBoxLayout()
        self.status_dot = PulsingLabel('●')
        self.status_dot.setFont(QFont('Arial', 16))
        status_box.addWidget(self.status_dot)
        
        self.status_label = QLabel('IDLE')
        self.status_label.setFont(QFont('Helvetica Neue', 10, QFont.Bold))
        self.status_label.setStyleSheet(f"color: {COLORS['text_dim']}; background: transparent;")
        status_box.addWidget(self.status_label)
        
        status_box.addStretch()
        
        # Progress
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(6)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                background: {COLORS['bg_medium']};
                border: none;
                border-radius: 3px;
            }}
            QProgressBar::chunk {{
                background: {COLORS['primary']};
                border-radius: 3px;
            }}
        """)
        status_box.addWidget(self.progress_bar)
        
        layout.addLayout(status_box)
        
        # === PARTICLE EFFECTS ===
        self.particle_container = QWidget()
        self.particle_container.setFixedHeight(100)
        particle_layout = QVBoxLayout(self.particle_container)
        particle_layout.setContentsMargins(0, 0, 0, 0)
        
        particle_label = QLabel('⚡ LIVE NEURAL ACTIVITY')
        particle_label.setFont(QFont('Helvetica Neue', 8, QFont.Bold))
        particle_label.setStyleSheet(f"color: {COLORS['primary']}; background: transparent;")
        particle_layout.addWidget(particle_label)
        
        self.particles = ParticleEffect()
        self.particles.setFixedHeight(80)
        particle_layout.addWidget(self.particles)
        
        layout.addWidget(self.particle_container)
        
        # === THINKING BAR GRAPH ===
        graph_label = QLabel('📊 THINKING INTENSITY')
        graph_label.setFont(QFont('Helvetica Neue', 8, QFont.Bold))
        graph_label.setStyleSheet(f"color: {COLORS['secondary']}; background: transparent;")
        layout.addWidget(graph_label)
        
        self.thinking_bars = ThinkingBarGraph()
        layout.addWidget(self.thinking_bars)
        
        # === LIVE THOUGHT ===
        thought_label = QLabel('💭 CURRENT THOUGHT')
        thought_label.setFont(QFont('Helvetica Neue', 8, QFont.Bold))
        thought_label.setStyleSheet(f"color: {COLORS['accent']}; background: transparent;")
        layout.addWidget(thought_label)
        
        self.thought_text = QLabel('Waiting for command...')
        self.thought_text.setFont(QFont('Monaco', 9))
        self.thought_text.setWordWrap(True)
        self.thought_text.setMinimumHeight(50)
        self.thought_text.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['text']};
                background: {COLORS['bg_medium']};
                padding: 10px;
                border-radius: 8px;
                border-left: 3px solid {COLORS['accent']};
            }}
        """)
        layout.addWidget(self.thought_text)
        
        # === LOG ===
        log_label = QLabel('📜 ACTIVITY LOG')
        log_label.setFont(QFont('Helvetica Neue', 8, QFont.Bold))
        log_label.setStyleSheet(f"color: {COLORS['text_dim']}; background: transparent;")
        layout.addWidget(log_label)
        
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setFont(QFont('Monaco', 8))
        self.log.setStyleSheet(f"""
            QTextEdit {{
                background: {COLORS['bg_medium']};
                color: {COLORS['primary']};
                border: 1px solid {COLORS['primary']};
                border-radius: 8px;
                padding: 8px;
            }}
            QScrollBar:vertical {{
                background: {COLORS['bg_dark']};
                width: 8px;
                border-radius: 4px;
            }}
            QScrollBar::handle:vertical {{
                background: {COLORS['primary']};
                border-radius: 4px;
            }}
        """)
        layout.addWidget(self.log)
        
        # === INPUT ===
        input_label = QLabel('⌨️  COMMAND INPUT')
        input_label.setFont(QFont('Helvetica Neue', 8, QFont.Bold))
        input_label.setStyleSheet(f"color: {COLORS['text_dim']}; background: transparent;")
        layout.addWidget(input_label)
        
        self.cmd_input = QLineEdit()
        self.cmd_input.setPlaceholderText('Enter command...')
        self.cmd_input.setFont(QFont('Helvetica Neue', 11))
        self.cmd_input.returnPressed.connect(self.execute)
        self.cmd_input.setStyleSheet(f"""
            QLineEdit {{
                background: {COLORS['bg_medium']};
                color: {COLORS['text']};
                border: 2px solid {COLORS['text_dim']};
                border-radius: 8px;
                padding: 12px;
            }}
            QLineEdit:focus {{
                border: 2px solid {COLORS['primary']};
            }}
        """)
        layout.addWidget(self.cmd_input)
        
        # === BUTTONS ===
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)
        
        self.exec_btn = QPushButton('⚡ EXECUTE')
        self.exec_btn.clicked.connect(self.execute)
        self.exec_btn.setCursor(Qt.PointingHandCursor)
        self.exec_btn.setFont(QFont('Helvetica Neue', 10, QFont.Bold))
        self.exec_btn.setFixedHeight(45)
        self.exec_btn.setStyleSheet(f"""
            QPushButton {{
                background: {COLORS['primary']};
                color: {COLORS['bg_dark']};
                border: none;
                border-radius: 8px;
            }}
            QPushButton:hover {{
                background: {COLORS['secondary']};
            }}
            QPushButton:disabled {{
                background: {COLORS['bg_medium']};
                color: {COLORS['text_dim']};
            }}
        """)
        btn_row.addWidget(self.exec_btn)
        
        self.stop_btn = QPushButton('■ STOP')
        self.stop_btn.clicked.connect(self.stop)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setCursor(Qt.PointingHandCursor)
        self.stop_btn.setFont(QFont('Helvetica Neue', 10, QFont.Bold))
        self.stop_btn.setFixedHeight(45)
        self.stop_btn.setStyleSheet(f"""
            QPushButton {{
                background: {COLORS['bg_medium']};
                color: {COLORS['error']};
                border: 2px solid {COLORS['error']};
                border-radius: 8px;
            }}
            QPushButton:hover {{
                background: {COLORS['error']};
                color: {COLORS['bg_dark']};
            }}
            QPushButton:disabled {{
                border-color: {COLORS['bg_medium']};
                color: {COLORS['text_dim']};
            }}
        """)
        btn_row.addWidget(self.stop_btn)
        
        layout.addLayout(btn_row)
    
    def start_ambient(self):
        """Start ambient animations"""
        # Slowly pulse particles even when idle
        self.ambient_timer = QTimer()
        self.ambient_timer.timeout.connect(self._ambient_pulse)
        self.ambient_timer.start(3000)
    
    def _ambient_pulse(self):
        """Ambient pulse effect"""
        if not self.is_executing:
            # Brief particle burst
            self.particles.start_effect()
            QTimer.singleShot(500, self.particles.stop_effect)
    
    def execute(self):
        """Execute with full animations"""
        cmd = self.cmd_input.text().strip()
        if not cmd:
            return
        
        self.is_executing = True
        self.exec_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.cmd_input.setEnabled(False)
        self.status_signal.emit("thinking")
        self.thinking_signal.emit(True)
        self.progress_signal.emit(10)
        
        self.safe_log(f"<span style='color: {COLORS['primary']}'>▶</span> {cmd}")
        
        def run():
            try:
                self.thought_signal.emit("Analyzing command structure...")
                self.progress_signal.emit(20)
                time.sleep(0.5)
                
                self.thought_signal.emit("Understanding user intent...")
                self.progress_signal.emit(40)
                intent = self.intent_analyzer.analyze(cmd)
                time.sleep(0.5)
                
                self.safe_log(f"<span style='color: {COLORS['secondary']}'>├─</span> Intent: {intent.get('intent_type')}")
                
                if self.intent_analyzer.is_conversational(intent):
                    self.thought_signal.emit("Generating natural response...")
                    self.progress_signal.emit(60)
                    response = self.chat_handler.respond(cmd)
                    self.safe_log(f"<span style='color: {COLORS['accent']}'>└─</span> {response}")
                else:
                    self.thought_signal.emit("Planning execution strategy...") 
                    self.progress_signal.emit(60)
                    time.sleep(0.3)
                    
                    self.thought_signal.emit("Executing automated actions...")
                    self.progress_signal.emit(80)
                    self.agent.run(cmd, intent)
                
                self.progress_signal.emit(100)
                self.status_signal.emit("complete")
                time.sleep(0.5)
                
            except Exception as e:
                self.safe_log(f"<span style='color: {COLORS['error']}'>❌</span> {str(e)}")
                self.status_signal.emit("error")
            finally:
                self.thinking_signal.emit(False)
                self.is_executing = False
                self.exec_btn.setEnabled(True)
                self.stop_btn.setEnabled(False)
                self.cmd_input.setEnabled(True)
                self.cmd_input.clear()
                self.cmd_input.setFocus()
                self.progress_signal.emit(0)
        
        threading.Thread(target=run, daemon=True).start()
    
    def stop(self):
        if self.agent:
            self.agent.stop_flag = True
        self.thinking_signal.emit(False)
        self.safe_log(f"<span style='color: {COLORS['error']}'>■ STOPPED</span>")
    
    def safe_log(self, msg):
        self.log_signal.emit(msg)
    
    def add_log(self, msg):
        t = datetime.now().strftime("%H:%M:%S")
        self.log.append(f"<span style='color: {COLORS['text_dim']}'>[{t}]</span> {msg}")
        self.log.verticalScrollBar().setValue(self.log.verticalScrollBar().maximum())
    
    def update_status(self, status):
        states = {
            "idle": (COLORS['text_dim'], "IDLE"),
            "thinking": (COLORS['warning'], "THINKING"),
            "error": (COLORS['error'], "ERROR"),
            "complete": (COLORS['primary'], "COMPLETE")
        }
        color, text = states.get(status, (COLORS['text_dim'], "IDLE"))
        self.status_dot.set_color(color)
        self.status_label.setText(text)
        self.status_label.setStyleSheet(f"color: {color}; background: transparent;")
    
    def update_thinking(self, thinking):
        if thinking:
            self.particles.start_effect()
            self.thinking_bars.start_thinking()
            self.icon.set_color(COLORS['warning'])
        else:
            self.particles.stop_effect()
            self.thinking_bars.stop_thinking()
            self.icon.set_color(COLORS['primary'])
            self.thought_text.setText("Waiting for command...")
    
    def update_thought(self, thought):
        self.thought_text.setText(f"💭 {thought}")
    
    def update_progress(self, value):
        self.progress_bar.setValue(value)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
    
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_pos)


def main():
    app = QApplication(sys.argv)
    gui = UltraAnimatedGUI()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
