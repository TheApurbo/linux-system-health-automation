# Linux System Health & Troubleshooting Automation

A Python-based Linux system monitoring and troubleshooting tool that automates common system health checks and generates a structured diagnostic report.

## Project Overview

Linux system administrators and technical support engineers often need to collect multiple system metrics before troubleshooting an issue.

This project automates that initial diagnostic process by collecting system information, resource usage, network information, running processes, and log statistics.

The tool evaluates system health and provides troubleshooting recommendations based on detected conditions.

## Key Features

### System Monitoring

- Hostname detection
- Operating system identification
- Linux release information
- System architecture detection
- CPU usage monitoring
- Memory usage monitoring
- Disk usage monitoring

### Network Diagnostics

- Internet connectivity check
- DNS resolution check
- Network interface detection
- Default gateway detection
- TCP connectivity testing

### Process Analysis

- Displays top CPU-consuming processes
- Process ID monitoring
- CPU usage monitoring
- Memory usage monitoring

### Log Analysis

- Counts INFO entries
- Counts WARNING entries
- Counts ERROR entries
- Extracts detected error messages

### Automated Health Assessment

The system evaluates resource usage using configurable thresholds:

| Resource | Warning | Critical |
|----------|---------|----------|
| CPU | 70% | 90% |
| Memory | 70% | 90% |
| Disk | 75% | 90% |

The tool generates an overall system status:

- HEALTHY
- ATTENTION REQUIRED

### Troubleshooting Recommendations

The tool automatically generates recommendations when it detects:

- High CPU usage
- High memory usage
- High disk usage
- Network connectivity problems
- DNS failures
- Warning log entries
- Error log entries

## Project Structure

```text
linux-system-health-automation/
│
├── README.md
├── system_health.py
├── logs.log
├── .gitignore
│
├── reports/
│   └── system_health_report.txt
│
└── docs/
    └── troubleshooting.md
## Technologies

- Python 3
- Linux
- Bash / Linux CLI utilities
- Git
- GitHub

## Linux Commands and Utilities Used

The project integrates several Linux utilities and system interfaces, including:

- `top`
- `free`
- `ip`
- `ps`
- `grep`
- `head`
- Python `shutil.disk_usage()`
- Python socket networking

## What This Project Demonstrates

This project demonstrates practical skills in:

- Linux system administration
- Technical troubleshooting
- Python automation
- System monitoring
- Network diagnostics
- DNS troubleshooting
- Process analysis
- Log analysis
- Error handling
- Threshold-based health evaluation
- Automated reporting
- Command-line tools
- Git/GitHub workflow

## Diagnostic Workflow

The tool follows a practical initial troubleshooting workflow:

1. Collect system information
2. Check CPU, memory, and disk usage
3. Check network connectivity
4. Verify DNS resolution
5. Inspect network interfaces and default gateway
6. Review resource-consuming processes
7. Analyze log entries
8. Identify potential issues
9. Generate troubleshooting recommendations
10. Produce a structured diagnostic report

## Sample Output

============================================================
LINUX SYSTEM HEALTH & TROUBLESHOOTING REPORT
============================================================

[SYSTEM INFORMATION]

Hostname         : linux-system
Operating System : Linux
Release          : Linux Release
Architecture     : x86_64

[RESOURCE USAGE]

CPU Usage        : 25.4% (HEALTHY)
Memory Usage     : 48.2% (HEALTHY)
Disk Usage       : 42.1% (HEALTHY)

[NETWORK DIAGNOSTICS]

Internet Connectivity : AVAILABLE
DNS Resolution        : WORKING

Network Interfaces:
eth0             UP             172.x.x.x/xx

Default Gateway       : default via 172.x.x.x

Network Latency       : UNAVAILABLE
Latency Method        : Unavailable

[TOP PROCESSES BY CPU USAGE]

PID    COMMAND        %CPU    %MEM

[LOG ANALYSIS]

INFO Entries          : 1
WARNING Entries       : 1
ERROR Entries         : 1

[DIAGNOSTIC SUMMARY]

Overall Status        : ATTENTION REQUIRED
CPU Status            : HEALTHY
Memory Status         : HEALTHY
Disk Status           : HEALTHY
Network Connectivity  : AVAILABLE
DNS Status            : WORKING

[TROUBLESHOOTING RECOMMENDATIONS]

- Review ERROR entries in logs.log.
- Review WARNING entries in logs.log.

============================================================

## Testing Environment

The project was developed and tested in a Linux-based GitHub Codespaces environment.

Some network-level diagnostic capabilities can behave differently inside containerized development environments. The application therefore handles unavailable diagnostic values gracefully instead of causing the entire health report to fail.

## Error Handling

The application uses exception handling to prevent individual diagnostic failures from stopping the complete health-check process.

If a particular system metric or diagnostic method is unavailable, the tool reports it as `UNAVAILABLE` and continues collecting the remaining information.

## Future Improvements

Possible future improvements include:

- ICMP latency monitoring
- Historical health reports
- JSON report generation
- CSV export
- Alert notifications
- Configurable thresholds
- Linux service health checks
- Remote host monitoring
- Web-based monitoring dashboard

## Purpose

This project was developed as a practical Linux support and system administration portfolio project.

It demonstrates how Python automation and Linux command-line tools can be combined to reduce repetitive diagnostic tasks and provide structured information for technical troubleshooting.

## Status

**Completed — Portfolio Project**

The project can be extended with additional monitoring, alerting, reporting, and remote diagnostic capabilities.
