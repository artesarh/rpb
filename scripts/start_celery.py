#!/usr/bin/env python3
"""
Cross-platform script to start Celery worker and beat scheduler.
Works on Windows, Linux, and macOS.
"""

import os
import sys
import time
import signal
import subprocess
import platform
from pathlib import Path
from typing import Optional, List


class CeleryManager:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent.parent
        self.logs_dir = self.base_dir / "logs"
        self.is_windows = platform.system() == "Windows"
        self.worker_process: Optional[subprocess.Popen] = None
        self.beat_process: Optional[subprocess.Popen] = None
        
        # Ensure directories exist
        self.logs_dir.mkdir(exist_ok=True)
        (self.base_dir / "celery" / "queue").mkdir(parents=True, exist_ok=True)
        (self.base_dir / "celery" / "processed").mkdir(parents=True, exist_ok=True)

    def get_python_executable(self) -> str:
        """Get the appropriate Python executable"""
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            # We're in a virtual environment
            return sys.executable
        else:
            # Try to find python in PATH
            return "python" if self.is_windows else "python3"

    def kill_existing_processes(self):
        """Kill any existing Celery processes"""
        print("🧹 Cleaning up existing Celery processes...")
        
        if self.is_windows:
            # Windows process cleanup
            try:
                subprocess.run([
                    "taskkill", "/F", "/IM", "celery.exe"
                ], capture_output=True, check=False)
                subprocess.run([
                    "wmic", "process", "where", 
                    "CommandLine like '%celery%project%'", "delete"
                ], capture_output=True, check=False)
            except Exception as e:
                print(f"⚠️  Warning: Could not kill existing processes: {e}")
        else:
            # Unix-based systems
            try:
                subprocess.run([
                    "pkill", "-f", "celery.*project"
                ], capture_output=True, check=False)
            except Exception as e:
                print(f"⚠️  Warning: Could not kill existing processes: {e}")

    def start_worker(self) -> bool:
        """Start Celery worker"""
        print("📦 Starting Celery worker...")
        
        python_exe = self.get_python_executable()
        worker_log = self.logs_dir / "celery_worker.log"
        
        cmd = [
            python_exe, "-m", "celery", "-A", "project", "worker",
            "--loglevel=info",
            "--concurrency=2"
        ]
        
        try:
            if self.is_windows:
                # Windows doesn't support proper daemonization, so we'll run in background
                self.worker_process = subprocess.Popen(
                    cmd,
                    cwd=str(self.base_dir),
                    stdout=open(worker_log, 'w'),
                    stderr=subprocess.STDOUT,
                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if self.is_windows else 0
                )
            else:
                # Unix systems - run in background
                self.worker_process = subprocess.Popen(
                    cmd,
                    cwd=str(self.base_dir),
                    stdout=open(worker_log, 'w'),
                    stderr=subprocess.STDOUT,
                    preexec_fn=os.setsid
                )
            
            time.sleep(2)  # Give it time to start
            
            if self.worker_process.poll() is None:
                print(f"✅ Celery worker started (PID: {self.worker_process.pid})")
                return True
            else:
                print("❌ Failed to start Celery worker")
                return False
                
        except Exception as e:
            print(f"❌ Error starting worker: {e}")
            return False

    def start_beat(self) -> bool:
        """Start Celery beat scheduler"""
        print("⏰ Starting Celery Beat scheduler...")
        
        python_exe = self.get_python_executable()
        beat_log = self.logs_dir / "celery_beat.log"
        
        cmd = [
            python_exe, "-m", "celery", "-A", "project", "beat",
            "--loglevel=info",
            "--scheduler=django_celery_beat.schedulers:DatabaseScheduler"
        ]
        
        try:
            if self.is_windows:
                self.beat_process = subprocess.Popen(
                    cmd,
                    cwd=str(self.base_dir),
                    stdout=open(beat_log, 'w'),
                    stderr=subprocess.STDOUT,
                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if self.is_windows else 0
                )
            else:
                self.beat_process = subprocess.Popen(
                    cmd,
                    cwd=str(self.base_dir),
                    stdout=open(beat_log, 'w'),
                    stderr=subprocess.STDOUT,
                    preexec_fn=os.setsid
                )
            
            time.sleep(2)  # Give it time to start
            
            if self.beat_process.poll() is None:
                print(f"✅ Celery Beat started (PID: {self.beat_process.pid})")
                return True
            else:
                print("❌ Failed to start Celery Beat")
                return False
                
        except Exception as e:
            print(f"❌ Error starting beat: {e}")
            return False

    def stop_services(self):
        """Stop all Celery services"""
        print("🛑 Stopping Celery services...")
        
        if self.worker_process:
            try:
                if self.is_windows:
                    self.worker_process.terminate()
                else:
                    os.killpg(os.getpgid(self.worker_process.pid), signal.SIGTERM)
                self.worker_process.wait(timeout=10)
                print("✅ Worker stopped")
            except Exception as e:
                print(f"⚠️  Force killing worker: {e}")
                if self.is_windows:
                    self.worker_process.kill()
                else:
                    os.killpg(os.getpgid(self.worker_process.pid), signal.SIGKILL)
        
        if self.beat_process:
            try:
                if self.is_windows:
                    self.beat_process.terminate()
                else:
                    os.killpg(os.getpgid(self.beat_process.pid), signal.SIGTERM)
                self.beat_process.wait(timeout=10)
                print("✅ Beat stopped")
            except Exception as e:
                print(f"⚠️  Force killing beat: {e}")
                if self.is_windows:
                    self.beat_process.kill()
                else:
                    os.killpg(os.getpgid(self.beat_process.pid), signal.SIGKILL)

    def check_status(self):
        """Check if services are running"""
        worker_running = self.worker_process and self.worker_process.poll() is None
        beat_running = self.beat_process and self.beat_process.poll() is None
        
        print("\n📋 Status:")
        print(f"   Worker: {'🟢 Running' if worker_running else '🔴 Stopped'}")
        print(f"   Beat: {'🟢 Running' if beat_running else '🔴 Stopped'}")
        print(f"\n📄 Log files:")
        print(f"   Worker: {self.logs_dir}/celery_worker.log")
        print(f"   Beat: {self.logs_dir}/celery_beat.log")

    def run(self):
        """Main execution method"""
        print("🚀 Starting Celery services...")
        print(f"📍 Platform: {platform.system()}")
        print(f"📁 Working directory: {self.base_dir}")
        
        # Check if Django is available
        try:
            os.chdir(self.base_dir)
            subprocess.run([
                self.get_python_executable(), "manage.py", "check"
            ], check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Django check failed: {e}")
            return False
        
        # Clean up existing processes
        self.kill_existing_processes()
        
        # Start services
        worker_started = self.start_worker()
        if not worker_started:
            print("❌ Failed to start worker, aborting...")
            return False
        
        beat_started = self.start_beat()
        if not beat_started:
            print("❌ Failed to start beat scheduler")
            self.stop_services()
            return False
        
        # Setup signal handlers for graceful shutdown
        def signal_handler(signum, frame):
            print(f"\n🛑 Received signal {signum}, shutting down...")
            self.stop_services()
            sys.exit(0)
        
        if not self.is_windows:
            signal.signal(signal.SIGINT, signal_handler)
            signal.signal(signal.SIGTERM, signal_handler)
        
        self.check_status()
        
        print("\n✅ Celery services started successfully!")
        print("🔥 Press Ctrl+C to stop all services")
        
        try:
            # Keep the script running
            while True:
                time.sleep(5)
                
                # Check if processes are still alive
                if self.worker_process and self.worker_process.poll() is not None:
                    print("❌ Worker process died, restarting...")
                    self.start_worker()
                
                if self.beat_process and self.beat_process.poll() is not None:
                    print("❌ Beat process died, restarting...")
                    self.start_beat()
                    
        except KeyboardInterrupt:
            print("\n🛑 Shutting down...")
            self.stop_services()
            return True


def main():
    """Entry point"""
    if len(sys.argv) > 1:
        if sys.argv[1] in ['--help', '-h']:
            print("""
Celery Manager - Cross-platform Celery worker and beat scheduler

Usage:
    python scripts/start_celery.py          # Start services
    python scripts/start_celery.py --help   # Show this help

The script will:
1. Check Django configuration
2. Kill any existing Celery processes
3. Start Celery worker and beat scheduler
4. Monitor processes and restart if they die
5. Gracefully shutdown on Ctrl+C

Log files are saved in: logs/celery_worker.log and logs/celery_beat.log
            """)
            return
    
    manager = CeleryManager()
    success = manager.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main() 