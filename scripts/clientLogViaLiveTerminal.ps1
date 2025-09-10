Set-Location -Path "C:\Program Files\Palo Alto Networks\GlobalProtect\"; 
.\PanGPSupport.exe -Force -Silent; 
Start-Sleep -Seconds 30;

$testLogsPath = "C:\Users\Roni.Khalil\Downloads\Test Logs";

if (Test-Path $testLogsPath) { Remove-Item -Force -Path $testLogsPath -Recurse };

Start-Sleep -Seconds 5 |

New-Item -ItemType Directory -Path $testLogsPath;

Start-Sleep -Seconds 5 |

route print > "$testLogsPath\RoutePrint.txt";
netstat -n > "$testLogsPath\NetStat.txt";
wmic nicconfig list full > "$testLogsPath\NicConfig.txt";
ipconfig /all > "$testLogsPath\IpConfig.txt";
systeminfo > "$testLogsPath\SystemInfo.txt";
wmic sysdriver where state='running' list full > "$testLogsPath\DriverInfo.txt";
wmic service where state='running' list full > "$testLogsPath\ServiceInfo.txt";
wmic process list full > "$testLogsPath\ProcessInfo.txt";
netsh interface ipv4 show interfaces level=verbose > "$testLogsPath\NicDetails.txt";

Copy-Item "C:\Windows\INF\setupapi.dev*" "$testLogsPath" -ErrorAction SilentlyContinue;
Copy-Item "C:\Program Files\Palo Alto Networks\GlobalProtect\*.log" "$testLogsPath" -ErrorAction SilentlyContinue;
Copy-Item "C:\Program Files\Palo Alto Networks\GlobalProtect\*.xml" "$testLogsPath" -ErrorAction SilentlyContinue;
Copy-Item "C:\Program Files\Palo Alto Networks\GlobalProtect\*.log.old" "$testLogsPath" -ErrorAction SilentlyContinue;
Copy-Item "C:\Users\Roni.Khalil\AppData\Local\Palo Alto Networks\GlobalProtect\*.log" "$testLogsPath" -ErrorAction SilentlyContinue;
Copy-Item "C:\Users\Roni.Khalil\AppData\Local\Palo Alto Networks\GlobalProtect\*.log.old" "$testLogsPath" -ErrorAction SilentlyContinue;
Copy-Item "C:\Windows\INF\setupapi.app*" "$testLogsPath" -ErrorAction SilentlyContinue;
