import platform
import psutil
import subprocess
import socket
import json
import logging
import threading
import time
from typing import Dict, Optional, List, Union
from dataclasses import dataclass, asdict
from datetime import datetime

class SystemControlLogger:
    """Advanced logging system for system control operations."""
    def __init__(self, log_file='system_control.log'):
        self.logger = logging.getLogger('SystemControlService')
        self.logger.setLevel(logging.DEBUG)
        
        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

@dataclass
class ProcessInfo:
    """Detailed process information data class."""
    pid: int
    name: str
    cpu_percent: float
    memory_percent: float
    status: str
    start_time: str
    username: Optional[str] = None
    command_line: Optional[List[str]] = None

class SystemControlService:
    """Comprehensive system management service with advanced features."""
    
    def __init__(self):
        """Initialize the system control service with logging and monitoring."""
        self.logger = SystemControlLogger().logger
        self.monitoring_threads = {}
        self.critical_processes = { 
            'system': ['systemd', 'launchd', 'explorer.exe'],
            'security': ['antivirus', 'firewall', 'security']
        }
    
    def open_application(self, app_name: str, arguments: Optional[List[str]] = None) -> Dict[str, Union[str, bool]]:
        """
        Advanced application opening with more robust handling and logging.
        
        Args:
            app_name (str): Name of the application to open
            arguments (Optional[List[str]]): Optional arguments to pass to the application
        
        Returns:
            Dict with operation details
        """
        try:
            # Validate application name
            if not app_name:
                raise ValueError("Application name cannot be empty")
            
            # Determine launch command based on OS
            os_commands = {
                "Windows": f"start {app_name}",
                "Darwin": f"open -a '{app_name}'",
                "Linux": f"{app_name}"
            }
            
            current_os = platform.system()
            if current_os not in os_commands:
                raise OSError(f"Unsupported operating system: {current_os}")
            
            # Construct full command with arguments
            full_command = os_commands[current_os]
            if arguments:
                full_command += " " + " ".join(arguments)
            
            # Execute with subprocess for better control
            process = subprocess.Popen(
                full_command, 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
            
            # Log the operation
            self.logger.info(f"Opened application: {app_name} with PID {process.pid}")
            
            return {
                "success": True,
                "message": f"{app_name} opened successfully",
                "pid": process.pid
            }
        
        except Exception as e:
            self.logger.error(f"Failed to open {app_name}: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }
    def capture_screenshot(self, output_file: str = 'screenshot.png') -> Dict[str, Union[str, bool]]:
        """
        Capture a screenshot of the current desktop.
        
        Args:

            output_file (str): Output file path for the screenshot
            (default: 'screenshot.png')
            
        Returns:
            Dict with operation details
        """
        try:
            # Get the current operating system
            current_os = platform.system()
            
            # Construct command based on OS
            if current_os == "Darwin":  # macOS
                command = f"screencapture {output_file}"
            elif current_os == "Windows":
                command = f"powershell -command \"Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('{{}}'); Start-Sleep -Milliseconds 250; Get-Clipboard -Format Image | ForEach-Object {{$_.Save('{output_file}')}}\"" 
            elif current_os == "Linux":
                command = f"import -window root {output_file}"
            else:
                raise OSError(f"Unsupported operating system: {current_os}")

            # Execute the command
            process = subprocess.Popen(
                command, 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
            code = process.wait()
            
            if code == 0:
                self.logger.info(f"Screenshot captured: {output_file}")
                return {
                    "success": True,
                    "message": f"Screenshot captured: {output_file}"
                }
            else:
                raise OSError("Failed to capture screenshot")

        except Exception as e:
            self.logger.error(f"Failed to capture screenshot: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }
    def system_info(self) -> Dict[str, Union[str, int, float]]:
        """
        Get basic system information like CPU, memory, and disk usage.
        
        Returns:
            Dict with system information
        """
        cpu_percent = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        
        return {
            "cpu_percent": cpu_percent,
            "memory_percent": memory.percent,
            "disk_percent": disk.percent,
            "ip_address": socket.gethostbyname(socket.gethostname()),
            "network_info": psutil.net_if_addrs(),
            "boot_time": datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"),
            "system_info": platform.uname(),
            "battery_info": psutil.sensors_battery() if psutil.sensors_battery() else None,
            "disk_usage": disk_usage('/'),
            "memory_usage": memory_usage(),
            "cpu_usage": cpu_usage()
            
            
            
        }
    def lock_computer(self) -> Dict[str, Union[str, bool]]:
        """
        Lock the computer screen.
        
        Returns:
            Dict with operation details
        """
        try:
            # Get the current operating system
            current_os = platform.system()
            
            # Construct command based on OS
            if current_os == "Darwin":  # macOS
                command = "pmset displaysleepnow"
            elif current_os == "Windows":
                command = "rundll32.exe user32.dll,LockWorkStation"
            elif current_os == "Linux":
                command = "gnome-screensaver-command -l"
            else:
                raise OSError(f"Unsupported operating system: {current_os}")

            # Execute the command
            process = subprocess.Popen(
                command, 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
            code = process.wait()
            
            if code == 0:
                self.logger.info("Computer locked")
                return {
                    "success": True,
                    "message": "Computer locked"
                }
            else:
                raise OSError("Failed to lock computer")

        except Exception as e:
            self.logger.error(f"Failed to lock computer: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }
    def get_system_info(self) -> Dict[str, Union[str, int, float]]:
        """
        Get basic system information like CPU, memory, and disk usage.
        
        Returns:
            Dict with system information
        """
        cpu_percent = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            "cpu_percent": cpu_percent,
            "memory_percent": memory.percent,
            "disk_percent": disk.percent
        }
    def network_diagnostics( self) -> Dict[str, Union[str, Dict[str, List[str]]]]:
        """
        Perform network diagnostics to check the network status.
        
        Returns:
            Dict with network diagnostic information
        """
        try:
            # Get the IP address and network interface information
            ip_address = socket.gethostbyname(socket.gethostname())
            network_info = psutil.net_if_addrs()
            
            # Get the network interface details
            interfaces = {}
            for interface, addrs in network_info.items():
                addresses = [addr.address for addr in addrs]
                interfaces[interface] = addresses
            
            return {
                "ip_address": ip_address,
                "network_interfaces": interfaces
            }
        
        except Exception as e:
            return {
                "error": str(e)
            }
        


# Example usage
def main():
    system_control = SystemControlService()
    
    # Open a browser    
    browser_result = system_control.open_application('chrome', ['https://www.example.com'])
    print(json.dumps(browser_result, indent=2))
    
    # List running processes
    processes = system_control.list_running_processes({'status': 'running'})
    for process in processes:
        print(asdict(process))
    
    # Start monitoring critical processes
    system_control.monitor_critical_processes(interval=120)
    
    # Run network diagnostics
    network_info = system_control.network_diagnostics()
    print(json.dumps(network_info, indent=2))

if __name__ == "__main__":
    main()