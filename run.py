from backend.app import create_app, socketio
import time
import sys
import subprocess
import os

app = create_app()

def kill_port_5000():
    """Kill any process using port 5000"""
    try:
        # Find process using port 5000
        result = subprocess.run(
            ['netstat', '-ano'],
            capture_output=True,
            text=True,
            shell=True
        )
        
        for line in result.stdout.split('\n'):
            if ':5000' in line and 'LISTENING' in line:
                parts = line.split()
                if parts:
                    pid = parts[-1]
                    if pid.isdigit() and int(pid) > 0:
                        print(f"Killing process {pid} on port 5000...")
                        subprocess.run(['taskkill', '/F', '/PID', pid], 
                                      capture_output=True, shell=True)
                        time.sleep(1)
                        return True
        return False
    except Exception as e:
        print(f"Warning: Could not auto-kill port: {e}")
        return False

def run_server():
    """Run server with auto port cleanup"""
    # First, kill anything on port 5000
    kill_port_5000()
    time.sleep(1)
    
    print(f"\n{'='*60}")
    print(f"Starting Flask-SocketIO server on http://127.0.0.1:5000")
    print(f"{'='*60}\n")
    
    try:
        socketio.run(
            app, 
            host='127.0.0.1',
            port=5000,
            debug=True,
            use_reloader=False
        )
    except OSError as e:
        if "10048" in str(e) or "Address already in use" in str(e):
            print("\n✗ Port 5000 still in use after cleanup.")
            print("   Run manually: Get-Process python | Stop-Process -Force")
            sys.exit(1)
        else:
            raise

if __name__ == "__main__":
    try:
        run_server()
    except KeyboardInterrupt:
        print("\n\nServer shut down by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        sys.exit(1)
