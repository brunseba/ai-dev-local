"""Ollama connection management for different deployment modes."""

from enum import Enum
from typing import Optional, List
import subprocess
import os
import requests


class OllamaMode(Enum):
    """Available Ollama connection modes."""
    AUTO = "auto"
    DOCKER = "docker"
    NATIVE = "native"
    REMOTE = "remote"


class OllamaConnection:
    """Manages connections to Ollama in different deployment modes."""
    
    def __init__(self, mode: Optional[str] = None, api_url: Optional[str] = None):
        """
        Initialize Ollama connection.
        
        Args:
            mode: Connection mode (auto, docker, native, remote). If None, uses env var.
            api_url: API URL for remote/custom mode. If None, uses env var.
        """
        # Set attributes before calling _detect_mode (which needs docker_service)
        self.api_url = api_url or os.getenv('OLLAMA_API_URL', 'http://localhost:11434')
        self.docker_compose_file = os.getenv('OLLAMA_DOCKER_COMPOSE_FILE', 'docker-compose.yml')
        self.docker_service = os.getenv('OLLAMA_DOCKER_SERVICE', 'ollama')
        self.mode = self._detect_mode(mode)
    
    def _detect_mode(self, mode: Optional[str]) -> OllamaMode:
        """
        Auto-detect or use specified mode.
        
        Detection order:
        1. Check if Docker service is running
        2. Check if native ollama is available
        3. Default to remote
        
        Args:
            mode: Specified mode or None for auto-detection
            
        Returns:
            Detected or specified OllamaMode
        """
        if mode and mode != 'auto':
            return OllamaMode(mode)
        
        if self._is_docker_available():
            return OllamaMode.DOCKER
        elif self._is_native_available():
            return OllamaMode.NATIVE
        else:
            return OllamaMode.REMOTE
    
    def _is_docker_available(self) -> bool:
        """Check if Docker Ollama service is running."""
        try:
            result = subprocess.run(
                ['docker-compose', 'ps', self.docker_service],
                capture_output=True, text=True, check=True,
                timeout=5
            )
            return 'Up' in result.stdout
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    def _is_native_available(self) -> bool:
        """Check if native ollama command is available."""
        try:
            subprocess.run(
                ['ollama', '--version'],
                capture_output=True, check=True,
                timeout=5
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    def _is_remote_available(self) -> bool:
        """Check if remote Ollama is accessible."""
        try:
            response = requests.get(f"{self.api_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def execute(self, args: List[str], check: bool = True, timeout: Optional[int] = None) -> subprocess.CompletedProcess:
        """
        Execute ollama command based on connection mode.
        
        Args:
            args: Command arguments (e.g., ['list'], ['pull', 'llama3'])
            check: Whether to raise CalledProcessError on non-zero exit
            timeout: Command timeout in seconds
            
        Returns:
            CompletedProcess with stdout, stderr, and returncode
            
        Raises:
            subprocess.CalledProcessError: If check=True and command fails
            NotImplementedError: If command not supported in current mode
        """
        if self.mode == OllamaMode.DOCKER:
            return self._execute_docker(args, check=check, timeout=timeout)
        elif self.mode == OllamaMode.NATIVE:
            return self._execute_native(args, check=check, timeout=timeout)
        else:
            return self._execute_api(args, check=check, timeout=timeout)
    
    def _execute_docker(self, args: List[str], check: bool = True, timeout: Optional[int] = None) -> subprocess.CompletedProcess:
        """Execute via docker-compose."""
        cmd = ['docker-compose', 'exec', '-T', self.docker_service, 'ollama'] + args
        return subprocess.run(cmd, capture_output=True, text=True, check=check, timeout=timeout)
    
    def _execute_native(self, args: List[str], check: bool = True, timeout: Optional[int] = None) -> subprocess.CompletedProcess:
        """Execute via native ollama command."""
        cmd = ['ollama'] + args
        return subprocess.run(cmd, capture_output=True, text=True, check=check, timeout=timeout)
    
    def _execute_api(self, args: List[str], check: bool = True, timeout: Optional[int] = None) -> subprocess.CompletedProcess:
        """
        Execute via API calls (for commands that support it).
        
        This translates CLI commands to HTTP API calls for remote Ollama servers.
        """
        client = OllamaAPIClient(self.api_url)
        
        # Create mock subprocess result
        result = subprocess.CompletedProcess(
            args=['ollama'] + args,
            returncode=0,
            stdout="",
            stderr=""
        )
        
        try:
            if args[0] == 'list':
                data = client.list_models()
                # Format output like CLI
                lines = ["NAME\tID\tSIZE\tMODIFIED"]
                for model in data.get('models', []):
                    name = model.get('name', '')
                    digest = model.get('digest', '')[:12]
                    size = self._format_size(model.get('size', 0))
                    modified = model.get('modified_at', '')
                    lines.append(f"{name}\t{digest}\t{size}\t{modified}")
                result.stdout = '\n'.join(lines) + '\n'
            
            elif args[0] == 'ps':
                data = client.list_running()
                lines = ["NAME\tID\tSIZE\tPROCESSOR\tUNTIL"]
                for model in data.get('models', []):
                    name = model.get('name', '')
                    digest = model.get('digest', '')[:12]
                    size = self._format_size(model.get('size', 0))
                    processor = model.get('details', {}).get('quantization_level', '')
                    expires = model.get('expires_at', '')
                    lines.append(f"{name}\t{digest}\t{size}\t{processor}\t{expires}")
                result.stdout = '\n'.join(lines) + '\n'
            
            elif args[0] == 'pull' and len(args) > 1:
                model_name = args[1]
                for progress in client.pull_model(model_name, stream=True):
                    if 'status' in progress:
                        print(progress['status'], end='\r')
                print()  # New line after progress
                result.stdout = f"success\n"
            
            elif args[0] == 'rm' and len(args) > 1:
                model_name = args[1]
                client.delete_model(model_name)
                result.stdout = f"deleted '{model_name}'\n"
            
            else:
                raise NotImplementedError(f"API execution for '{args[0]}' not implemented")
        
        except requests.HTTPError as e:
            result.returncode = 1
            result.stderr = str(e)
            if check:
                raise subprocess.CalledProcessError(1, result.args, result.stdout, result.stderr)
        except Exception as e:
            result.returncode = 1
            result.stderr = str(e)
            if check:
                raise subprocess.CalledProcessError(1, result.args, result.stdout, result.stderr)
        
        return result
    
    def _format_size(self, size_bytes: int) -> str:
        """Format bytes to human-readable size."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} PB"
    
    def get_api_url(self) -> str:
        """
        Get the API URL for this connection.
        
        Returns:
            API URL string
        """
        if self.mode == OllamaMode.DOCKER:
            return "http://localhost:11434"
        else:
            return self.api_url
    
    def is_available(self) -> bool:
        """
        Check if Ollama is available in current mode.
        
        Returns:
            True if Ollama is accessible, False otherwise
        """
        if self.mode == OllamaMode.DOCKER:
            return self._is_docker_available()
        elif self.mode == OllamaMode.NATIVE:
            return self._is_native_available()
        else:
            return self._is_remote_available()


class OllamaAPIClient:
    """Client for Ollama HTTP API."""
    
    def __init__(self, base_url: str):
        """
        Initialize API client.
        
        Args:
            base_url: Base URL of Ollama API (e.g., http://localhost:11434)
        """
        self.base_url = base_url.rstrip('/')
    
    def list_models(self) -> dict:
        """
        List all models.
        
        Returns:
            Dict with 'models' key containing list of model info
        """
        response = requests.get(f"{self.base_url}/api/tags", timeout=10)
        response.raise_for_status()
        return response.json()
    
    def show_model(self, name: str) -> dict:
        """
        Show model information.
        
        Args:
            name: Model name
            
        Returns:
            Dict with model details
        """
        response = requests.post(
            f"{self.base_url}/api/show",
            json={"name": name},
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    
    def pull_model(self, name: str, stream: bool = True):
        """
        Pull a model.
        
        Args:
            name: Model name to pull
            stream: Whether to stream progress
            
        Yields:
            Progress dicts if stream=True
            
        Returns:
            Final result dict if stream=False
        """
        response = requests.post(
            f"{self.base_url}/api/pull",
            json={"name": name, "stream": stream},
            stream=stream,
            timeout=600  # 10 minutes for large models
        )
        response.raise_for_status()
        
        if stream:
            for line in response.iter_lines():
                if line:
                    import json
                    yield json.loads(line)
        else:
            return response.json()
    
    def delete_model(self, name: str) -> dict:
        """
        Delete a model.
        
        Args:
            name: Model name to delete
            
        Returns:
            Result dict
        """
        response = requests.delete(
            f"{self.base_url}/api/delete",
            json={"name": name},
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    
    def list_running(self) -> dict:
        """
        List running models.
        
        Returns:
            Dict with 'models' key containing list of running models
        """
        response = requests.get(f"{self.base_url}/api/ps", timeout=10)
        response.raise_for_status()
        return response.json()
