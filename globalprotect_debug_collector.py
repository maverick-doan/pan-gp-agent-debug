import logging
from pathlib import Path
from datetime import datetime
import sys
import dotenv
import subprocess
from typing import Tuple
import shutil
import time
import json
import os
import argparse

dotenv.dotenv_values()

gp_path = Path(dotenv.dotenv_values()["GP_PATH"]) if dotenv.dotenv_values()["GP_PATH"] and Path(dotenv.dotenv_values()["GP_PATH"]).exists() else Path("C:\\Program Files\\Palo Alto Networks\\GlobalProtect")
user_appdata = Path(dotenv.dotenv_values()["USER_APPDATA"]) if dotenv.dotenv_values()["USER_APPDATA"] and Path(dotenv.dotenv_values()["USER_APPDATA"]).exists() else Path.home() / "AppData" / "Local" / "Palo Alto Networks" / "GlobalProtect"

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

    def copy_user_logs(self) -> None:
        self.logger.info("Copying user-specific log files...")
        
        if user_appdata.exists():
            log_patterns = ["*.log", "*.log.old"]
            for pattern in log_patterns:
                try:
                    log_files = list(user_appdata.glob(pattern))
                    for log_file in log_files:
                        if log_file.is_file():
                            dest_path = self.output_dir / f"User_{log_file.name}"
                            shutil.copy2(log_file, dest_path)
                            self.logger.debug(f"Copied user log: {log_file.name}")
                except Exception as e:
                    self.logger.warning(f"Failed to copy user {pattern} files: {e}")
        else:
            self.logger.info("User AppData GlobalProtect directory not found")

    def run_pangpsupport(self) -> None:
        self.logger.info("Running PanGPSupport.exe...")
        
        pangpsupport_path = self.globalprotect_path / "PanGPSupport.exe"
        
        if not pangpsupport_path.exists():
            self.logger.error("PanGPSupport.exe not found in GlobalProtect directory")
            self.collection_results["PanGPSupport"] = "Executable not found"
            return
            
        try:
            # Run PanGPSupport with /F (force) and /Q (quiet) flags
            result = subprocess.run(
                [str(pangpsupport_path), "/F", "/Q"],
                capture_output=True,
                text=True,
                timeout=120,
                encoding='utf-8'
            )
            
            if result.returncode == 0:
                self.logger.info("PanGPSupport.exe completed successfully")
                self.collection_results["PanGPSupport"] = "Success"
                
                self.logger.info("Waiting for logs to be generated...")
                time.sleep(60)
            else:
                self.logger.warning(f"PanGPSupport.exe completed with exit code: {result.returncode}")
                self.collection_results["PanGPSupport"] = f"Completed with warnings (exit code: {result.returncode})"
                
        except subprocess.TimeoutExpired:
            self.logger.error("PanGPSupport.exe timed out")
            self.collection_results["PanGPSupport"] = "Timed out"
        except Exception as e:
            self.logger.error(f"PanGPSupport.exe failed: {str(e)}")
            self.collection_results["PanGPSupport"] = f"Failed: {str(e)}"

    def generate_summary_report(self) -> None:
        self.logger.info("Generating summary report...")
        
        report_path = self.output_dir / "Collection_Summary.txt"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("GlobalProtect Debug Collection Summary Report\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Collection Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Output Directory: {self.output_dir.absolute()}\n\n")
            
            f.write("Collection Results:\n")
            f.write("-" * 30 + "\n")
            for item, status in self.collection_results.items():
                f.write(f"{item}: {status}\n")
                
            f.write(f"\nTotal files collected: {len(list(self.output_dir.glob('*')))}")
            
        # Also generate JSON report
        json_report_path = self.output_dir / "Collection_Summary.json"
        with open(json_report_path, 'w', encoding='utf-8') as f:
            json.dump({
                "collection_date": datetime.now().isoformat(),
                "output_directory": str(self.output_dir.absolute()),
                "collection_results": self.collection_results,
                "total_files": len(list(self.output_dir.glob('*')))
            }, f, indent=2)

    def run_collection(self) -> bool:
        self.logger.info("Starting GlobalProtect debug collection...")
        
        try:
            # Step 1: Run PanGPSupport
            self.run_pangpsupport()
            
            # Step 2: Collect system information
            self.collect_system_info()
            
            # Step 3: Copy GlobalProtect logs
            self.copy_globalprotect_logs()
            
            # Step 4: Copy setupapi files
            self.copy_setupapi_files()
            
            # Step 5: Copy user logs
            self.copy_user_logs()
            
            # Step 6: Generate summary report
            self.generate_summary_report()
            
            self.logger.info("Debug collection completed successfully!")
            self.logger.info(f"Output directory: {self.output_dir.absolute()}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Debug collection failed: {str(e)}")
            return False


def main():
    parser = argparse.ArgumentParser(
        description="GlobalProtect Debug Collector - Automated log collection for troubleshooting",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python globalprotect_debug_collector.py
  python globalprotect_debug_collector.py --output "C:\\MyLogs" --verbose
  python globalprotect_debug_collector.py -o "C:\\CustomPath" -v
        """
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Custom output directory for collected logs"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="GlobalProtect Debug Collector v1.0.0"
    )
    
    args = parser.parse_args()
    
    # Check if running as administrator
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        import ctypes
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        
    if not is_admin:
        print("Warning: This script may require administrator privileges for full functionality.")
        print("Some commands may fail if run without elevated permissions.\n")
        
    # Run the collection
    collector = GlobalProtectDebugCollector(
        output_dir=args.output,
        verbose=args.verbose
    )
    
    success = collector.run_collection()
    
    if success:
        print(f"\nDebug collection completed successfully!")
        print(f"Output directory: {collector.output_dir.absolute()}")
        print(f"Check 'Collection_Summary.txt' for detailed results")
    else:
        print("\nDebug collection failed. Check the logs for details.")
        sys.exit(1)


if __name__ == "__main__":
    main()