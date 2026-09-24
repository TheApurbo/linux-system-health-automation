import platform
import shutil
import socket
import subprocess
import os
from datetime import datetime


REPORT_DIR = "reports"
REPORT_FILE = os.path.join(REPORT_DIR, "system_health_report.txt")
LOG_FILE = "logs.log"


# ==========================================
# SYSTEM INFORMATION
# ==========================================

def get_system_info():
    return {
        "Hostname": platform.node(),
        "Operating System": platform.system(),
        "OS Release": platform.release(),
        "Architecture": platform.machine()
    }


# ==========================================
# CPU MONITORING
# ==========================================

def get_cpu_usage():
    try:
        result = subprocess.run(
            ["bash", "-c", "top -bn1 | grep 'Cpu(s)'"],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode != 0:
            return None

        line = result.stdout.strip()

        if not line or "id" not in line:
            return None

        idle = float(line.split("id")[0].split()[-1])

        return round(100 - idle, 2)

    except (ValueError, subprocess.SubprocessError, OSError):
        return None


# ==========================================
# MEMORY MONITORING
# ==========================================

def get_memory_usage():
    try:
        result = subprocess.run(
            ["free", "-m"],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode != 0:
            return None

        lines = result.stdout.splitlines()

        if len(lines) < 2:
            return None

        memory = lines[1].split()

        if len(memory) < 3:
            return None

        total = int(memory[1])
        used = int(memory[2])

        if total <= 0:
            return None

        return round((used / total) * 100, 2)

    except (ValueError, subprocess.SubprocessError, OSError):
        return None


# ==========================================
# DISK MONITORING
# ==========================================

def get_disk_usage():
    try:
        total, used, free = shutil.disk_usage("/")

        if total <= 0:
            return None

        return round((used / total) * 100, 2)

    except OSError:
        return None


# ==========================================
# NETWORK CHECK
# ==========================================

def check_network():
    try:
        connection = socket.create_connection(
            ("8.8.8.8", 53),
            timeout=3
        )

        connection.close()
        return True

    except (OSError, socket.timeout):
        return False


# ==========================================
# DNS CHECK
# ==========================================

def check_dns():
    try:
        socket.gethostbyname("google.com")
        return True

    except socket.gaierror:
        return False


# ==========================================
# PROCESS ANALYSIS
# ==========================================

def get_top_processes():
    try:
        result = subprocess.run(
            [
                "bash",
                "-c",
                "ps -eo pid,comm,%cpu,%mem --sort=-%cpu | head -n 6"
            ],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode != 0:
            return "Unable to retrieve process information."

        output = result.stdout.strip()

        if not output:
            return "No process information available."

        return output

    except (subprocess.SubprocessError, OSError):
        return "Unable to retrieve process information."


# ==========================================
# LOG ANALYSIS
# ==========================================

def analyze_logs():

    result = {
        "INFO": 0,
        "WARNING": 0,
        "ERROR": 0,
        "ERROR_MESSAGES": []
    }

    if not os.path.exists(LOG_FILE):
        return result

    try:
        with open(LOG_FILE, "r", encoding="utf-8") as file:

            for line in file:

                line = line.strip()

                if line.startswith("INFO"):
                    result["INFO"] += 1

                elif line.startswith("WARNING"):
                    result["WARNING"] += 1

                elif line.startswith("ERROR"):
                    result["ERROR"] += 1
                    result["ERROR_MESSAGES"].append(line)

    except (OSError, UnicodeError):
        pass

    return result


# ==========================================
# STATUS EVALUATION
# ==========================================

def evaluate_usage(value, warning, critical):

    if value is None:
        return "UNKNOWN"

    if value >= critical:
        return "CRITICAL"

    if value >= warning:
        return "WARNING"

    return "NORMAL"


# ==========================================
# TROUBLESHOOTING RECOMMENDATIONS
# ==========================================

def get_recommendations(
    cpu_status,
    memory_status,
    disk_status,
    network,
    dns,
    log_analysis
):

    recommendations = []

    if cpu_status == "CRITICAL":
        recommendations.append(
            "Check high-CPU processes using: top or htop"
        )

    elif cpu_status == "WARNING":
        recommendations.append(
            "Review running processes and unnecessary services."
        )

    if memory_status == "CRITICAL":
        recommendations.append(
            "Check memory-consuming processes using: ps aux --sort=-%mem"
        )

    elif memory_status == "WARNING":
        recommendations.append(
            "Close unnecessary applications or services."
        )

    if disk_status == "CRITICAL":
        recommendations.append(
            "Find large files using: du -sh /*"
        )

    elif disk_status == "WARNING":
        recommendations.append(
            "Clean unnecessary files, logs, and cached packages."
        )

    if not network:
        recommendations.append(
            "Check network interfaces using: ip addr"
        )

        recommendations.append(
            "Test connectivity using: ping 8.8.8.8"
        )

    if not dns:
        recommendations.append(
            "Check DNS configuration and test with: nslookup google.com"
        )

    if log_analysis["ERROR"] > 0:
        recommendations.append(
            "Review ERROR entries in logs.log for system troubleshooting."
        )

    if log_analysis["WARNING"] > 0:
        recommendations.append(
            "Review WARNING entries in logs.log and monitor affected services."
        )

    if not recommendations:
        recommendations.append(
            "No immediate troubleshooting action required."
        )

    return recommendations


# ==========================================
# REPORT GENERATION
# ==========================================

def generate_report():

    cpu = get_cpu_usage()
    memory = get_memory_usage()
    disk = get_disk_usage()

    network = check_network()
    dns = check_dns()

    log_analysis = analyze_logs()

    cpu_status = evaluate_usage(cpu, 70, 90)
    memory_status = evaluate_usage(memory, 70, 90)
    disk_status = evaluate_usage(disk, 80, 90)

    issues = []

    if cpu_status == "CRITICAL":
        issues.append("CPU usage is critically high.")

    elif cpu_status == "WARNING":
        issues.append("CPU usage is above the recommended level.")

    if memory_status == "CRITICAL":
        issues.append("Memory usage is critically high.")

    elif memory_status == "WARNING":
        issues.append("Memory usage is above the recommended level.")

    if disk_status == "CRITICAL":
        issues.append("Disk usage is critically high.")

    elif disk_status == "WARNING":
        issues.append("Disk usage is above the recommended level.")

    if not network:
        issues.append("Internet connectivity check failed.")

    if not dns:
        issues.append("DNS resolution failed.")

    if log_analysis["ERROR"] > 0:
        issues.append(
            f"{log_analysis['ERROR']} ERROR entry/entries detected in logs."
        )

    if log_analysis["WARNING"] > 0:
        issues.append(
            f"{log_analysis['WARNING']} WARNING entry/entries detected in logs."
        )

    overall = "ATTENTION REQUIRED" if issues else "HEALTHY"

    recommendations = get_recommendations(
        cpu_status,
        memory_status,
        disk_status,
        network,
        dns,
        log_analysis
    )

    # ======================================
    # BUILD REPORT
    # ======================================

    report = []

    report.append("=" * 60)
    report.append("          LINUX SYSTEM HEALTH REPORT")
    report.append("=" * 60)

    report.append(f"Generated: {datetime.now()}")

    report.append("\n[SYSTEM INFORMATION]")

    for key, value in get_system_info().items():
        report.append(f"{key}: {value}")

    report.append("\n[RESOURCE HEALTH]")

    report.append(
        f"CPU Usage    : "
        f"{cpu if cpu is not None else 'UNKNOWN'}% "
        f"[{cpu_status}]"
    )

    report.append(
        f"Memory Usage : "
        f"{memory if memory is not None else 'UNKNOWN'}% "
        f"[{memory_status}]"
    )

    report.append(
        f"Disk Usage   : "
        f"{disk if disk is not None else 'UNKNOWN'}% "
        f"[{disk_status}]"
    )

    report.append("\n[NETWORK HEALTH]")

    report.append(
        "Internet Connectivity : "
        + ("CONNECTED" if network else "FAILED")
    )

    report.append(
        "DNS Resolution        : "
        + ("OK" if dns else "FAILED")
    )

    report.append("\n[TOP PROCESSES BY CPU USAGE]")

    report.append(get_top_processes())

    report.append("\n[LOG ANALYSIS]")

    report.append(
        f"INFO entries    : {log_analysis['INFO']}"
    )

    report.append(
        f"WARNING entries : {log_analysis['WARNING']}"
    )

    report.append(
        f"ERROR entries   : {log_analysis['ERROR']}"
    )

    if log_analysis["ERROR_MESSAGES"]:

        report.append("\nDetected ERROR messages:")

        for message in log_analysis["ERROR_MESSAGES"]:
            report.append(f"- {message}")

    report.append("\n[DIAGNOSTIC SUMMARY]")

    if issues:
        for issue in issues:
            report.append(f"- {issue}")
    else:
        report.append("No major issues detected.")

    report.append(f"\nOverall Status: {overall}")

    report.append("\n[TROUBLESHOOTING RECOMMENDATIONS]")

    for recommendation in recommendations:
        report.append(f"- {recommendation}")

    report.append("\n" + "=" * 60)
    report.append("             END OF HEALTH REPORT")
    report.append("=" * 60)

    final_report = "\n".join(report)

    # ======================================
    # PRINT REPORT
    # ======================================

    print(final_report)

    # ======================================
    # SAVE REPORT
    # ======================================

    try:
        os.makedirs(REPORT_DIR, exist_ok=True)

        with open(REPORT_FILE, "w", encoding="utf-8") as file:
            file.write(final_report)

        print(f"\nReport saved to: {REPORT_FILE}")

    except OSError as error:
        print(f"\nUnable to save report: {error}")


# ==========================================
# PROGRAM ENTRY POINT
# ==========================================

if __name__ == "__main__":
    generate_report()
