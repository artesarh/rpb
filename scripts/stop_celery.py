#!/usr/bin/env python3
"""
Cross-platform script to stop Celery worker and beat scheduler.
Works on Windows, Linux, and macOS.
"""

import subprocess
import platform
import sys
from pathlib import Path


def stop_celery_services():
    """Stop all Celery services"""
    print("🛑 Stopping Celery services...")
    
    is_windows = platform.system() == "Windows"
    stopped_processes = 0
    
    if is_windows:
        # Windows process cleanup
        print("🧹 Stopping Celery processes on Windows...")
        
        try:
            # Kill celery.exe processes
            result = subprocess.run([
                "taskkill", "/F", "/IM", "celery.exe"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                stopped_processes += 1
                print("✅ Stopped celery.exe processes")
            
            # Kill processes with celery in command line
            result = subprocess.run([
                "wmic", "process", "where", 
                "CommandLine like '%celery%project%'", "delete"
            ], capture_output=True, text=True)
            
            if result.returncode == 0 and "deleted" in result.stdout.lower():
                stopped_processes += 1
                print("✅ Stopped Celery project processes")
                
        except Exception as e:
            print(f"⚠️  Warning: Error stopping Windows processes: {e}")
    
    else:
        # Unix-based systems (Linux, macOS)
        print("🧹 Stopping Celery processes on Unix system...")
        
        try:
            # Kill celery processes
            result = subprocess.run([
                "pkill", "-f", "celery.*project"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                stopped_processes += 1
                print("✅ Stopped Celery processes")
            elif result.returncode == 1:
                print("ℹ️  No Celery processes were running")
            else:
                print(f"⚠️  pkill returned code {result.returncode}")
                
        except Exception as e:
            print(f"⚠️  Warning: Error stopping Unix processes: {e}")
    
    # Clean up PID files if they exist
    base_dir = Path(__file__).resolve().parent.parent
    logs_dir = base_dir / "logs"
    
    pid_files = [
        logs_dir / "celery_worker.pid",
        logs_dir / "celery_beat.pid"
    ]
    
    for pid_file in pid_files:
        if pid_file.exists():
            try:
                pid_file.unlink()
                print(f"🗑️  Removed {pid_file.name}")
            except Exception as e:
                print(f"⚠️  Could not remove {pid_file.name}: {e}")
    
    if stopped_processes > 0:
        print("✅ All Celery services stopped!")
    else:
        print("ℹ️  No Celery services were running")
    
    return True


def main():
    """Entry point"""
    if len(sys.argv) > 1 and sys.argv[1] in ['--help', '-h']:
        print("""
Celery Stop Script - Cross-platform Celery service stopper

Usage:
    python scripts/stop_celery.py          # Stop all Celery services
    python scripts/stop_celery.py --help   # Show this help

The script will:
1. Kill all running Celery worker processes
2. Kill all running Celery beat processes  
3. Clean up PID files
4. Work on Windows, Linux, and macOS
        """)
        return
    
    print(f"📍 Platform: {platform.system()}")
    success = stop_celery_services()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main() 