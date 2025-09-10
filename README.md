# GlobalProtect Debug Collector

A comprehensive Python script to automate the collection of debug logs and system information for troubleshooting GlobalProtect Agent issues on Windows systems.

## 🚀 Features

- **Automated Log Collection**: Automatically runs PanGPSupport.exe and collects all necessary debug information
- **System Information Gathering**: Collects network configuration, system details, running services, and more
- **Comprehensive Log Copying**: Copies GlobalProtect logs, setupapi files, and user-specific logs
- **Professional Logging**: Detailed logging with both console and file output
- **Error Handling**: Robust error handling with graceful fallbacks
- **Customisable Output**: Configurable output directory and logging verbosity
- **Summary Reports**: Generates both text and JSON summary reports
- **Cross-Platform Ready**: Designed for Windows but easily adaptable

## 📋 Prerequisites

- Windows 10/11 (tested on Windows 10)
- Python 3.7 or higher
- GlobalProtect Agent installed
- Administrator privileges (recommended for full functionality)

## 🛠️ Installation

1. **Clone or download** this repository
2. **Ensure Python 3.7+** is installed on your system
3. **Run as Administrator** (recommended) for best results

## 📖 Usage

### Basic Usage

```bash
# Run with default settings
python globalprotect_debug_collector.py

# Run with verbose logging
python globalprotect_debug_collector.py --verbose

# Specify custom output directory
python globalprotect_debug_collector.py --output "C:\MyLogs"

# Combine options
python globalprotect_debug_collector.py --output "C:\MyLogs" --verbose
```

### Command Line Options

| Option | Short | Description |
|--------|-------|-------------|
| `--output` | `-o` | Custom output directory for collected logs |
| `--verbose` | `-v` | Enable verbose logging |
| `--version` | | Display version information |
| `--help` | `-h` | Show help message |

## 🔍 What Gets Collected

### System Information
- Route table information
- Network connections (netstat)
- Network interface configuration
- IP configuration details
- System information
- Running system drivers
- Running services
- Running processes
- Network interface details

### GlobalProtect Logs
- Program directory logs (*.log, *.xml, *.log.old)
- User AppData logs
- PanGPSupport.exe output

### Windows System Files
- Setupapi device installation logs
- Setupapi application logs

## 📁 Output Structure

```
GlobalProtect_Debug_Logs_YYYYMMDD_HHMMSS/
├── Collection_Summary.txt          # Human-readable summary
├── Collection_Summary.json         # Machine-readable summary
├── Route_Table_Information.txt     # Route table data
├── Network_Connections.txt         # Netstat output
├── Network_Interface_Configuration.txt
├── IP_Configuration_Details.txt
├── System_Information.txt
├── Running_System_Drivers.txt
├── Running_Services.txt
├── Running_Processes.txt
├── Network_Interface_Details.txt
├── *.log                           # GlobalProtect log files
├── *.xml                           # GlobalProtect XML files
├── setupapi.dev*.log              # Device installation logs
├── setupapi.app*.log              # Application logs
└── User_*.log                     # User-specific logs
```

## ⚠️ Important Notes

### Administrator Privileges
Some commands may fail without administrator privileges. The script will warn you if it detects you're not running as admin.

### File Paths
The script expects GlobalProtect to be installed in the default location:
```
C:\Program Files\Palo Alto Networks\GlobalProtect\
```

### Timeouts
- PanGPSupport.exe has a 120-second timeout
- System commands have a 60-second timeout
- The script waits 60 seconds after PanGPSupport for logs to generate

## 🐛 Troubleshooting

### Common Issues

1. **"PanGPSupport.exe not found"**
   - Ensure GlobalProtect is installed in the default location
   - Check if the file exists manually

2. **Permission denied errors**
   - Run the script as Administrator
   - Check file/folder permissions

3. **Command timeouts**
   - Some commands may take longer on slower systems
   - Check system performance and resource usage

### Log Files

The script creates a log file `globalprotect_collector.log` in the current directory with detailed execution information.

## 🔧 Customisation

### Adding New Commands

To add new system information commands, modify the `collect_system_info()` method:

```python
commands = [
    # ... existing commands ...
    ("your_command_here", "Description of what it does"),
]
```

### Modifying Output Directory

Change the default output directory in the `_setup_output_directory()` method:

```python
output_path = Path(f"Custom_Prefix_{timestamp}")
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Review the log files for error details
3. Open an issue on GitHub with:
   - Error messages
   - System information
   - Steps to reproduce

## 📊 Version History

- **v1.0.0** - Initial release with core functionality
  - Automated log collection
  - System information gathering
  - Comprehensive error handling
  - Professional logging system

---

**Note**: This script is designed for IT professionals and system administrators. Always review collected logs before sharing them, as they may contain sensitive system information.