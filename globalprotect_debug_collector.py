import logging
from pathlib import Path
from datetime import datetime
import sys
import dotenv

# commands = [
#     ("route print", "Route table information"),
#     ("netstat -n", "Network connections"),
#     ("wmic nicconfig list full", "Network interface configuration"),
#     ("ipconfig /all", "IP configuration details"),
#     ("systeminfo", "System information"),
#     ("wmic sysdriver where state='running' list full", "Running system drivers"),
#     ("wmic service where state='running' list full", "Running services"),
#     ("wmic process list full", "Running processes"),
#     ("netsh interface ipv4 show interfaces level=verbose", "Network interface details")
# ]

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