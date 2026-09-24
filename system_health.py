import platform
import shutil
import socket
import subprocess
import os
from datetime import datetime


REPORT_DIR = "reports"
REPORT_FILE = os.path.join(REPORT_DIR, "system_health_report.txt")


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
            text=True
        )

        line = result.stdout.strip()

        if not line:
            return None

        if "id" in line:
            idle = float(line.split("id")[0].split()[-1])
            return round(100 - idle, 2)

        return None

    except Exception:
        return None


# ==========================================
# MEMORY MONITORING
# ==========================================

def get_memory_usage():
    try:
        result = subprocess.run(
            ["free", "-m"],
            capture_output=True,
            text=True
        )

        lines = result.stdout.splitlines()

        if len(lines) < 2:
            return None

        memory = lines[1].split()

        total = int(memory[1])
        used = int(memory[2])

        if total == 0:
            return None

        return round((used / total) * 100, 2)

    except Exception:
        return None


# ==========================================
# DISK MONITORING
# ==========================================

def get_disk_usage():
    try:
        total, used, free = shutil.disk_usage("/")

        if total == 0:
            return None

        return round((used / total) * 100, 2)

    except Exception:
        return None


# ==========================================
# NETWORK CHECK
# ==========================================

def check_network():
    try:
        socket.create_connection(
            ("8.8.8.8", 53),
            timeout=3
        )
        return True

    except OSError:
        return False


# ==========================================
# DNS CHECK
# ==========================================

def check_dns():
    try:
        socket.gethostbyname("google.com")
        return True

    except socket.error:
        return False


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
    dns
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

    if issues:
        overall = "ATTENTION REQUIRED"
    else:
        overall = "HEALTHY"

    recommendations = get_recommendations(
        cpu_status,
        memory_status,
        disk_status,
        network,
        dns
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

    os.makedirs(REPORT_DIR, exist_ok=True)

    with open(REPORT_FILE, "w") as file:
        file.write(final_report)

    print(f"\nReport saved to: {REPORT_FILE}")


# ==========================================
# PROGRAM ENTRY POINT
# ==========================================

if __name__ == "__main__":
    generate_report()
