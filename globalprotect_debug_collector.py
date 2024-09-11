import logging
from pathlib import Path
from datetime import datetime
import sys
import dotenv
import subprocess
from typing import Tuple
import shutil

dotenv.dotenv_values()

gp_path = Path(dotenv.dotenv_values()["GP_PATH"]) if dotenv.dotenv_values()["GP_PATH"] and Path(dotenv.dotenv_values()["GP_PATH"]).exists() else Path("C:\\Program Files\\Palo Alto Networks\\GlobalProtect")

class GlobalProtectDebugCollector:

    def __init__(self, output_dir: str = None, verbose: bool = False):
        self.setup_logging(verbose)
        self.globalprotect_path = gp_path
        self.output_dir = self._setup_output_directory(output_dir)
        self.collection_results = {}
        
    def setup_logging(self, verbose: bool) -> None:
        log_level = logging.DEBUG if verbose else logging.INFO
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler('globalprotect_collector.log')
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def _setup_output_directory(self, custom_dir: str = None) -> Path:
        if custom_dir:
            output_path = Path(custom_dir)
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = Path(f"GlobalProtect_Debug_Logs_{timestamp}")
            
        output_path.mkdir(exist_ok=True, parents=True)
        self.logger.info(f"Output directory: {output_path.absolute()}")
        return output_path

    def run_command(self, command: str, description: str, timeout: int = 60) -> Tuple[bool, str]:
        try:
            self.logger.info(f"Executing: {description}")
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                encoding='utf-8'
            )
            
            if result.returncode == 0:
                self.logger.info(f"{description} completed successfully")
                return True, result.stdout
            else:
                self.logger.warning(f"{description} completed with warnings (exit code: {result.returncode})")
                return True, result.stdout + "\n" + result.stderr
                
        except subprocess.TimeoutExpired:
            self.logger.error(f"{description} timed out after {timeout} seconds")
            return False, f"Command timed out after {timeout} seconds"
        except Exception as e:
            self.logger.error(f"{description} failed: {str(e)}")
            return False, str(e)

    def collect_system_info(self) -> None:
        self.logger.info("Collecting system information...")
        
        commands = [
            ("route print", "Route table information"),
            ("netstat -n", "Network connections"),
            ("wmic nicconfig list full", "Network interface configuration"),
            ("ipconfig /all", "IP configuration details"),
            ("systeminfo", "System information"),
            ("wmic sysdriver where state='running' list full", "Running system drivers"),
            ("wmic service where state='running' list full", "Running services"),
            ("wmic process list full", "Running processes"),
            ("netsh interface ipv4 show interfaces level=verbose", "Network interface details")
        ]
        
        for command, description in commands:
            success, output = self.run_command(command, description)
            if success:
                filename = f"{description.replace(' ', '_').replace('(', '').replace(')', '')}.txt"
                filepath = self.output_dir / filename
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(f"Command: {command}\n")
                    f.write(f"Description: {description}\n")
                    f.write(f"Timestamp: {datetime.now().isoformat()}\n")
                    f.write("-" * 80 + "\n")
                    f.write(output)
                self.collection_results[description] = "Success"
            else:
                self.collection_results[description] = f"Failed: {output}"

    def copy_globalprotect_logs(self) -> None:
        self.logger.info("Copying GlobalProtect log files...")
        
        # GlobalProtect program directory logs
        log_patterns = ["*.log", "*.xml", "*.log.old"]
        for pattern in log_patterns:
            try:
                log_files = list(self.globalprotect_path.glob(pattern))
                for log_file in log_files:
                    if log_file.is_file():
                        dest_path = self.output_dir / log_file.name
                        shutil.copy2(log_file, dest_path)
                        self.logger.debug(f"Copied: {log_file.name}")
            except Exception as e:
                self.logger.warning(f"Failed to copy {pattern} files: {e}")

    def copy_setupapi_files(self) -> None:
        self.logger.info("Copying Windows setupapi files...")
        
        setupapi_paths = [
            Path("C:\\Windows\\INF\\setupapi.dev*"),
            Path("C:\\Windows\\INF\\setupapi.app*")
        ]
        
        for pattern in setupapi_paths:
            try:
                setupapi_files = list(Path("C:\\Windows\\INF").glob(pattern.name))
                for file_path in setupapi_files:
                    if file_path.is_file():
                        dest_path = self.output_dir / file_path.name
                        shutil.copy2(file_path, dest_path)
                        self.logger.debug(f"Copied: {file_path.name}")
            except Exception as e:
                self.logger.warning(f"Failed to copy setupapi files: {e}")