# Linux System Health & Troubleshooting Automation

A Python-based Linux system monitoring and troubleshooting tool that automates common system health checks and generates a structured diagnostic report.

## Project Overview

Linux system administrators and technical support engineers often need to collect multiple system metrics before troubleshooting an issue.

This project automates that initial diagnostic process by collecting system information, resource usage, network information, running processes, and log statistics.

The tool evaluates system health and provides troubleshooting recommendations based on detected conditions.

## Features

### System Monitoring
- Hostname detection
- Operating system identification
- Kernel/release information
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
- Shows process ID
- Shows CPU usage
- Shows memory usage

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

The tool generates an overall status:

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

## Sample Output

```text
============================================================
LINUX SYSTEM HEALTH & TROUBLESHOOTING REPORT
============================================================

[SYSTEM INFORMATION]

[RESOURCE USAGE]

[NETWORK DIAGNOSTICS]

[TOP PROCESSES BY CPU USAGE]

[LOG ANALYSIS]

[DIAGNOSTIC SUMMARY]

[TROUBLESHOOTING RECOMMENDATIONS]
