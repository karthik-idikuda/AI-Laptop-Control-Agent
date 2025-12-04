"""
Context Awareness System - AI understands current state and predicts needs
"""

import psutil
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from collections import defaultdict, deque
import json
import os


class ContextAwareness:
    """Monitors system context and user activity patterns"""
    
    def __init__(self):
        self.active_app_history = deque(maxlen=100)
        self.activity_patterns = defaultdict(list)
        self.current_context = {}
        self.context_file = os.path.expanduser("~/.osagent/context.json")
        self.load_patterns()
    
    def get_active_application(self) -> Optional[str]:
        """Get currently active/focused application (macOS)"""
        try:
            from AppKit import NSWorkspace
            active_app = NSWorkspace.sharedWorkspace().activeApplication()
            return active_app.get('NSApplicationName', 'Unknown')
        except ImportError:
            # Fallback for systems without AppKit
            return self._get_active_app_cross_platform()
        except Exception as e:
            print(f"Error getting active app: {e}")
            return None
    
    def _get_active_app_cross_platform(self) -> Optional[str]:
        """Cross-platform active app detection"""
        # This is a simplified version - real implementation would use platform-specific APIs
        for proc in psutil.process_iter(['name', 'status']):
            try:
                # Heuristic: high CPU or lots of threads = likely active
                if proc.info['status'] == 'running':
                    return proc.info['name']
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return None
    
    def track_activity(self):
        """Record current activity"""
        app = self.get_active_application()
        if app:
            timestamp = datetime.now()
            self.active_app_history.append({
                'app': app,
                'time': timestamp.isoformat(),
                'hour': timestamp.hour,
                'day_of_week': timestamp.weekday()
            })
            
            # Update patterns
            hour_key = f"{timestamp.weekday()}_{timestamp.hour}"
            self.activity_patterns[hour_key].append(app)
    
    def get_current_context(self) -> Dict[str, Any]:
        """Get comprehensive current context"""
        now = datetime.now()
        
        context = {
            'time': {
                'hour': now.hour,
                'day_of_week': now.weekday(),
                'is_weekend': now.weekday() >= 5,
                'is_work_hours': 9 <= now.hour <= 17,
            },
            'system': {
                'cpu_percent': psutil.cpu_percent(interval=0.1),
                'memory_percent': psutil.virtual_memory().percent,
                'battery': self._get_battery_status(),
                'network': self._get_network_status(),
            },
            'activity': {
                'active_app': self.get_active_application(),
                'recent_apps': self._get_recent_apps(limit=5),
            },
            'predictions': {
                'likely_next_app': self.predict_next_app(),
                'workflow_state': self.detect_workflow_state(),
            }
        }
        
        self.current_context = context
        return context
    
    def _get_battery_status(self) -> Dict[str, Any]:
        """Get battery information"""
        try:
            battery = psutil.sensors_battery()
            if battery:
                return {
                    'percent': battery.percent,
                    'plugged_in': battery.power_plugged,
                    'time_left': battery.secsleft if not battery.power_plugged else None
                }
        except Exception:
            pass
        return {'available': False}
    
    def _get_network_status(self) -> Dict[str, Any]:
        """Get network information"""
        try:
            net_io = psutil.net_io_counters()
            return {
                'bytes_sent': net_io.bytes_sent,
                'bytes_recv': net_io.bytes_recv,
                'connected': True
            }
        except Exception:
            return {'connected': False}
    
    def _get_recent_apps(self, limit: int = 5) -> List[str]:
        """Get recently used applications"""
        if not self.active_app_history:
            return []
        
        recent = []
        seen = set()
        for entry in reversed(self.active_app_history):
            app = entry['app']
            if app not in seen:
                recent.append(app)
                seen.add(app)
                if len(recent) >= limit:
                    break
        return recent
    
    def predict_next_app(self) -> Optional[str]:
        """Predict next likely application based on patterns"""
        if not self.active_app_history:
            return None
        
        now = datetime.now()
        hour_key = f"{now.weekday()}_{now.hour}"
        
        # Get patterns for this time
        patterns = self.activity_patterns.get(hour_key, [])
        if not patterns:
            return None
        
        # Find most common app at this time
        from collections import Counter
        counter = Counter(patterns)
        if counter:
            return counter.most_common(1)[0][0]
        
        return None
    
    def detect_workflow_state(self) -> str:
        """Detect current workflow state"""
        recent_apps = self._get_recent_apps(limit=3)
        
        # Define workflow patterns
        workflows = {
            'coding': ['Visual Studio Code', 'Terminal', 'Chrome', 'iTerm', 'PyCharm'],
            'design': ['Figma', 'Photoshop', 'Sketch', 'Illustrator'],
            'communication': ['Slack', 'Mail', 'Messages', 'Zoom', 'Teams'],
            'research': ['Safari', 'Chrome', 'Firefox', 'Notes'],
            'media': ['Spotify', 'Music', 'Photos', 'QuickTime Player'],
        }
        
        # Score each workflow
        scores = {}
        for workflow, apps in workflows.items():
            score = sum(1 for app in recent_apps if app in apps)
            if score > 0:
                scores[workflow] = score
        
        if scores:
            return max(scores, key=scores.get)
        
        return 'general'
    
    def should_suggest_action(self, action: str) -> bool:
        """Determine if an action should be suggested based on context"""
        context = self.get_current_context()
        
        # Rules-based suggestions
        if action == 'take_break':
            # Suggest break after 2 hours of continuous work
            return len(self.active_app_history) > 50
        
        elif action == 'save_battery':
            battery = context['system']['battery']
            if battery.get('percent', 100) < 20 and not battery.get('plugged_in'):
                return True
        
        elif action == 'optimize_memory':
            if context['system']['memory_percent'] > 80:
                return True
        
        return False
    
    def save_patterns(self):
        """Save learned patterns to disk"""
        try:
            os.makedirs(os.path.dirname(self.context_file), exist_ok=True)
            data = {
                'patterns': dict(self.activity_patterns),
                'last_saved': datetime.now().isoformat()
            }
            with open(self.context_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving patterns: {e}")
    
    def load_patterns(self):
        """Load learned patterns from disk"""
        if os.path.exists(self.context_file):
            try:
                with open(self.context_file, 'r') as f:
                    data = json.load(f)
                    self.activity_patterns = defaultdict(list, data.get('patterns', {}))
            except Exception as e:
                print(f"Error loading patterns: {e}")


# Global instance
context_awareness = ContextAwareness()
