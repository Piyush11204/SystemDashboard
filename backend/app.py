import os
import sys
import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import psutil
import socket


# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import your services
from services.voice_service import VoiceService
from services.ai_service import AIService
from services.system_control import SystemControlService
from utils.helpers import LoggerHelper, ConfigManager

# Load environment variables
load_dotenv()

# Setup logging
logger = LoggerHelper.setup_logger()

# Initialize the Flask application
app = Flask(__name__)
CORS(app)

# Load configuration
try:
    config = ConfigManager.load_config()
except Exception as e:
    logger.error(f"Configuration load error: {e}")
    config = {}

# Initialize services
try:
    voice_service = VoiceService()
    ai_service = AIService(api_key=config.get('openai_api_key'))
    system_service = SystemControlService()
except Exception as e:
    logger.error(f"Service initialization error: {e}")
    raise

# Voice-related routes
@app.route('/listen', methods=['GET'])
def listen_voice():
    try:
        text = voice_service.listen()
        return jsonify({'text': text or ''})
    except Exception as e:
        logger.error(f"Voice listening error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/speak', methods=['POST'])
def speak_text():
    try:
        data = request.json
        text = data.get('text', '')
        voice_type = data.get('voice_type', 'default')
        result = voice_service.speak(text, voice_type)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Text-to-speech error: {e}")
        return jsonify({'error': str(e)}), 500

# AI-related routes
@app.route('/ai-chat', methods=['POST'])
def ai_chat():
    try:
        data = request.json
        logger.info(f"Received AI Chat request: {data}")  # Log the incoming data
        prompt = data.get('prompt', '')
        messages = [
            {"role": "system", "content": "You are a helpful AI assistant named Jarvis."},
            {"role": "user", "content": prompt}
        ]
        response = ai_service.chat_completion(messages)
        logger.info(f"AI Response: {response}")  # Log the response
        return jsonify({'response': response})
    except Exception as e:
        logger.error(f"AI chat error: {e}")
        return jsonify({'error': str(e)}), 500

# System control routes
@app.route('/api/system-control', methods=['POST'])
def system_control():
    try:
        data = request.json
        command = data.get('command', '').lower()

        # Define system control mappings with more advanced actions
        control_actions = {
            'open browser': lambda: system_service.open_application('chrome'),
            'close browser': lambda: system_service.close_application('chrome'),
            'open edge': lambda: system_service.open_application('msedge'),
            'open firefox': lambda: system_service.open_application('firefox'),
            'open notepad': lambda: system_service.open_application('notepad'),
            'open terminal': lambda: system_service.open_application('terminal'),
            'open vscode': lambda: system_service.open_application('code'),
            'system info': lambda: system_service.get_system_info(),
            'get processes': lambda: system_service.list_running_processes(),
            'network status': lambda: system_service.network_diagnostics(),
            'restart computer': lambda: system_service.restart_system(),
            'shutdown': lambda: system_service.shutdown_system(),
            'sleep': lambda: system_service.sleep_system(),
            'clear memory cache': lambda: system_service.clear_memory_cache(),
            'end high cpu process': lambda: system_service.terminate_high_cpu_process(),
            'take screenshot': lambda: system_service.capture_screenshot(),
            'show desktop': lambda: system_service.show_desktop(),
            'lock computer': lambda: system_service.lock_computer()
        }

        # Fuzzy matching for more flexible command recognition
        matched_commands = [
            action for key, action in control_actions.items() 
            if key in command
        ]

        if matched_commands:
            # Execute the first matched command
            result = matched_commands[0]()
            return jsonify({
                'success': True, 
                'result': result,
                'message': f"Executed command matching: {command}"
            }), 200

        return jsonify({
            'success': False,
            'error': 'Command not recognized', 
            'available_commands': list(control_actions.keys())
        }), 400

    except Exception as e:
        logger.error(f"System control error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Error handler
@app.errorhandler(Exception)
def handle_error(e):
    logger.error(f"Unhandled exception: {e}")
    logger.error(traceback.format_exc())
    return jsonify({'error': 'An unexpected error occurred'}), 500

@app.route('/api/system/network', methods=['GET'])
def get_network_info():
    try:
        # Get IP address and network interface information
        ip_address = socket.gethostbyname(socket.gethostname())
        network_info = psutil.net_if_addrs()
        
        # Get the network interface details
        interfaces = {}
        for interface, addrs in network_info.items():
            for addr in addrs:
                if addr.family == psutil.AF_INET:  # IPv4 address
                    interfaces[interface] = {
                        'ip': addr.address,
                        'netmask': addr.netmask,
                        'broadcast': addr.broadcast
                    }

        return jsonify({
            'ip': ip_address,
            'interfaces': interfaces,
            'hostname': socket.gethostname(),
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/system/processes', methods=['GET'])
def get_processes_info():
    try:
        processes = []
        # Loop through all running processes
        for proc in psutil.process_iter(['pid', 'name', 'status', 'username']):
            processes.append({
                'pid': proc.info['pid'],
                'name': proc.info['name'],
                "status": proc.info['status'],
                "username": proc.info['username'],
                
            })

        return jsonify(processes)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
