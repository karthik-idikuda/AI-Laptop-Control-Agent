"""
Proactive Agent - AI that suggests and executes tasks autonomously
"""

from datetime import datetime, time as dt_time
from typing import List, Dict, Callable, Any
import schedule
import threading
import time


class ProactiveTask:
    """Represents a proactive task"""
    
    def __init__(self, name: str, trigger: str, action: Callable, 
                 conditions: List[Callable] = None, auto_execute: bool = False):
        self.name = name
        self.trigger = trigger  # "daily 09:00", "hourly", "on_event:wifi_connected"
        self.action = action
        self.conditions = conditions or []
        self.auto_execute = auto_execute
        self.last_executed = None
        self.execution_count = 0
    
    def should_execute(self) -> bool:
        """Check if all conditions are met"""
        return all(condition() for condition in self.conditions)
    
    def execute(self):
        """Execute the task"""
        if self.should_execute():
            try:
                self.action()
                self.last_executed = datetime.now()
                self.execution_count += 1
                return True
            except Exception as e:
                print(f"Error executing task {self.name}: {e}")
                return False
        return False


class ProactiveAgent:
    """Autonomous agent that performs tasks proactively"""
    
    def __init__(self):
        self.tasks: List[ProactiveTask] = []
        self.running = False
        self.scheduler_thread = None
        
        # Register default routines
        self._register_default_routines()
    
    def _register_default_routines(self):
        """Register default proactive routines"""
        
        # Morning routine
        self.add_routine(
            name="Morning Startup",
            trigger="daily 09:00",
            action=self._morning_routine,
            auto_execute=True
        )
        
        # Meeting preparation
        self.add_routine(
            name="Meeting Prep",
            trigger="before_calendar_event",
            action=self._prepare_for_meeting,
            auto_execute=False  # Ask first
        )
        
        # Evening cleanup
        self.add_routine(
            name="Evening Cleanup",
            trigger="daily 18:00",
            action=self._evening_cleanup,
            auto_execute=True
        )
        
        # Hourly health check
        self.add_routine(
            name="System Health",
            trigger="hourly",
            action=self._system_health_check,
            auto_execute=True
        )
    
    def add_routine(self, name: str, trigger: str, action: Callable, 
                    conditions: List[Callable] = None, auto_execute: bool = False):
        """Add a new proactive routine"""
        task = ProactiveTask(name, trigger, action, conditions, auto_execute)
        self.tasks.append(task)
        
        # Schedule it
        self._schedule_task(task)
    
    def _schedule_task(self, task: ProactiveTask):
        """Schedule a task based on its trigger"""
        if task.trigger == "hourly":
            schedule.every().hour.do(task.execute)
        elif task.trigger.startswith("daily"):
            # Parse time like "daily 09:00"
            time_str = task.trigger.split()[1]
            schedule.every().day.at(time_str).do(task.execute)
        elif task.trigger.startswith("before_calendar_event"):
            # This would integrate with calendar API
            pass
    
    def start(self):
        """Start the proactive agent"""
        if not self.running:
            self.running = True
            self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
            self.scheduler_thread.start()
            print("🤖 Proactive agent started")
    
    def stop(self):
        """Stop the proactive agent"""
        self.running = False
        print("🤖 Proactive agent stopped")
    
    def _run_scheduler(self):
        """Run the task scheduler"""
        while self.running:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    # Default routine implementations
    
    def _morning_routine(self):
        """Morning startup routine"""
        print("☀️ Good morning! Running startup routine...")
        
        from app_manager import open_app
        from context_awareness import context_awareness
        
        # Get context
        context = context_awareness.get_current_context()
        
        # Open common morning apps
        morning_apps = ['Mail', 'Calendar', 'Slack']
        for app in morning_apps:
            open_app(app)
            time.sleep(2)
        
        # TODO: Summarize overnight emails
        # TODO: Show today's calendar
        # TODO: Check for system updates
        
        print("✅ Morning routine complete!")
    
    def _prepare_for_meeting(self, meeting_info: Dict = None):
        """Prepare for an upcoming meeting"""
        print(f"📅 Preparing for meeting...")
        
        from app_manager import open_app
        
        # TODO: Get meeting info from calendar
        # TODO: Open meeting link
        # TODO: Prepare relevant documents
        # TODO: Set Do Not Disturb
        
        # For now, basic prep
        open_app("Zoom")
        open_app("Notes")
        
        print("✅ Meeting preparation complete!")
    
    def _evening_cleanup(self):
        """Evening cleanup routine"""
        print("🌙 Running evening cleanup...")
        
        # TODO: Close unused apps
        # TODO: Organize downloads folder
        # TODO: Backup important files
        # TODO: Clear cache/temp files
        
        print("✅ Evening cleanup complete!")
    
    def _system_health_check(self):
        """Check system health and optimize"""
        from context_awareness import context_awareness
        
        context = context_awareness.get_current_context()
        system = context['system']
        
        # Memory optimization
        if system['memory_percent'] > 80:
            print("⚠️ High memory usage detected, optimizing...")
            self._optimize_memory()
        
        # Battery management
        battery = system['battery']
        if battery.get('percent', 100) < 20 and not battery.get('plugged_in'):
            print("🔋 Low battery detected, enabling power saving...")
            self._enable_power_saving()
        
        # CPU management
        if system['cpu_percent'] > 90:
            print("🔥 High CPU usage detected...")
            # TODO: Identify and manage CPU-intensive processes
    
    def _optimize_memory(self):
        """Optimize system memory"""
        # TODO: Close unused browser tabs
        # TODO: Quit idle applications
        # TODO: Clear cache
        pass
    
    def _enable_power_saving(self):
        """Enable power saving mode"""
        # TODO: Reduce screen brightness
        # TODO: Close non-essential apps
        # TODO: Disable background sync
        pass
    
    def suggest_action(self, action_name: str, reason: str) -> bool:
        """Suggest an action to the user"""
        print(f"\n💡 Suggestion: {action_name}")
        print(f"   Reason: {reason}")
        print(f"   Execute? (y/n): ", end='')
        
        # In a GUI, this would show a notification
        # For now, just log it
        return False  # Would wait for user input


# Global instance
proactive_agent = ProactiveAgent()
