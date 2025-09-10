# Step 1

cd "C:\Program Files\Palo Alto Networks\GlobalProtect\"

# Step 2

.\PanGPSupport.exe /F /Q

# Step 3

mkdir "C:\Program Files\Palo Alto Networks\GlobalProtect\LogExport\"

# Step 4

route print > "C:\Program Files\Palo Alto Networks\GlobalProtect\LogExport\RoutePrint.txt"
netstat -n > "C:\Program Files\Palo Alto Networks\GlobalProtect\LogExport\NetStat.txt"
wmic nicconfig list full > "C:\Program Files\Palo Alto Networks\GlobalProtect\LogExport\NicConfig.txt"
ipconfig /all > "C:\Program Files\Palo Alto Networks\GlobalProtect\LogExport\IpConfig.txt"
systeminfo > "C:\Program Files\Palo Alto Networks\GlobalProtect\LogExport\SystemInfo.txt"
wmic sysdriver where state='running' list full > "C:\Program Files\Palo Alto Networks\GlobalProtect\LogExport\DriverInfo.txt"
wmic service where state='running' list full > "C:\Program Files\Palo Alto Networks\GlobalProtect\LogExport\ServiceInfo.txt"
wmic process list full > "C:\Program Files\Palo Alto Networks\GlobalProtect\LogExport\ProcessInfo.txt"
netsh interface ipv4 show interfaces level=verbose > "C:\Program Files\Palo Alto Networks\GlobalProtect\LogExport\NicDetais.txt"
copy "C:\Windows\INF\setupapi.dev*" "C:\Program Files\Palo Alto Networks\GlobalProtect\LogExport\"
copy "C:\Program Files\Palo Alto Networks\GlobalProtect\*.log" "C:\Program Files\Palo Alto Networks\GlobalProtect\LogExport\"
copy "C:\Program Files\Palo Alto Networks\GlobalProtect\*.xml" "C:\Program Files\Palo Alto Networks\GlobalProtect\LogExport\"
copy "C:\Program Files\Palo Alto Networks\GlobalProtect\*.log.old" "C:\Program Files\Palo Alto Networks\GlobalProtect\LogExport\"
copy "C:\Users\<REPLACE>\AppData\Local\Palo Alto Networks\GlobalProtect\*.log" "C:\Program Files\Palo Alto Networks\GlobalProtect\LogExport\"
copy "C:\Users\<REPLACE>\AppData\Local\Palo Alto Networks\GlobalProtect\*.log.old" "C:\Program Files\Palo Alto Networks\GlobalProtect\LogExport\"