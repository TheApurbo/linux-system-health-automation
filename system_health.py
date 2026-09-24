import platform
import shutil
import socket
import subprocess
from datetime import datetime


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
            usage = 100 - idle
            return round(usage, 2)

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

        usage = (used / total) * 100

        return round(usage, 2)

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

        usage = (used / total) * 100

        return round(usage, 2)

    except Exception:
        return None


# ==========================================
# NETWORK CONNECTIVITY CHECK
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
# USAGE STATUS EVALUATION
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

    # CPU recommendations
    if cpu_status == "CRITICAL":
        recommendations.append(
            "Check high-CPU processes using: top or htop"
        )

    elif cpu_status == "WARNING":
        recommendations.append(
            "Review running processes and unnecessary services."
        )

    # Memory recommendations
    if memory_status == "CRITICAL":
        recommendations.append(
            "Check memory-consuming processes using: ps aux --sort=-%mem"
        )

    elif memory_status == "WARNING":
        recommendations.append(
            "Close unnecessary applications or services."
        )

    # Disk recommendations
    if disk_status == "CRITICAL":
        recommendations.append(
            "Find large files using: du -sh /*"
        )

    elif disk_status == "WARNING":
        recommendations.append(
            "Clean unnecessary files, logs, and cached packages."
        )

    # Network recommendations
    if not network:
        recommendations.append(
            "Check network interfaces using: ip addr"
        )

        recommendations.append(
            "Test connectivity using: ping 8.8.8.8"
        )

    # DNS recommendations
    if not dns:
        recommendations.append(
            "Check DNS configuration and test with: nslookup google.com"
        )

    # No problems
    if not recommendations:
        recommendations.append(
            "No immediate troubleshooting action required."
        )

    return recommendations


# ==========================================
# REPORT GENERATION
# ==========================================

def generate_report():

    # Collect system data
    cpu = get_cpu_usage()
    memory = get_memory_usage()
    disk = get_disk_usage()

    network = check_network()
    dns = check_dns()

    # Evaluate system health
    cpu_status = evaluate_usage(cpu, 70, 90)
    memory_status = evaluate_usage(memory, 70, 90)
    disk_status = evaluate_usage(disk, 80, 90)

    # ======================================
    # REPORT HEADER
    # ======================================

    print("=" * 60)
    print("          LINUX SYSTEM HEALTH REPORT")
    print("=" * 60)

    print(f"Generated: {datetime.now()}")

    # ======================================
    # SYSTEM INFORMATION
    # ======================================

    print("\n[SYSTEM INFORMATION]")

    system_info = get_system_info()

    for key, value in system_info.items():
        print(f"{key}: {value}")

    # ======================================
    # RESOURCE HEALTH
    # ======================================

    print("\n[RESOURCE HEALTH]")

    if cpu is not None:
        print(
            f"CPU Usage    : {cpu}%  [{cpu_status}]"
        )
    else:
        print("CPU Usage    : UNKNOWN")

    if memory is not None:
        print(
            f"Memory Usage : {memory}%  [{memory_status}]"
        )
    else:
        print("Memory Usage : UNKNOWN")

    if disk is not None:
        print(
            f"Disk Usage   : {disk}%  [{disk_status}]"
        )
    else:
        print("Disk Usage   : UNKNOWN")

    # ======================================
    # NETWORK HEALTH
    # ======================================

    print("\n[NETWORK HEALTH]")

    print(
        "Internet Connectivity : "
        + ("CONNECTED" if network else "FAILED")
    )

    print(
        "DNS Resolution        : "
        + ("OK" if dns else "FAILED")
    )

    # ======================================
    # DIAGNOSTIC SUMMARY
    # ======================================

    print("\n[DIAGNOSTIC SUMMARY]")

    issues = []

    if cpu_status == "CRITICAL":
        issues.append(
            "CPU usage is critically high."
        )

    elif cpu_status == "WARNING":
        issues.append(
            "CPU usage is above the recommended level."
        )

    if memory_status == "CRITICAL":
        issues.append(
            "Memory usage is critically high."
        )

    elif memory_status == "WARNING":
        issues.append(
            "Memory usage is above the recommended level."
        )

    if disk_status == "CRITICAL":
        issues.append(
            "Disk usage is critically high."
        )

    elif disk_status == "WARNING":
        issues.append(
            "Disk usage is above the recommended level."
        )

    if not network:
        issues.append(
            "Internet connectivity check failed."
        )

    if not dns:
        issues.append(
            "DNS resolution failed."
        )

    # ======================================
    # OVERALL STATUS
    # ======================================

    if not issues:

        print("No major issues detected.")
        overall = "HEALTHY"

    else:

        for issue in issues:
            print(f"- {issue}")

        overall = "ATTENTION REQUIRED"

    print("\nOverall Status:", overall)

    # ======================================
    # TROUBLESHOOTING
    # ======================================

    print("\n[TROUBLESHOOTING RECOMMENDATIONS]")

    recommendations = get_recommendations(
        cpu_status,
        memory_status,
        disk_status,
        network,
        dns
    )

    for recommendation in recommendations:
        print(f"- {recommendation}")

    # ======================================
    # REPORT FOOTER
    # ======================================

    print("\n" + "=" * 60)
    print("             END OF HEALTH REPORT")
    print("=" * 60)


# ==========================================
# PROGRAM ENTRY POINT
# ==========================================

if __name__ == "__main__":
    generate_report()
