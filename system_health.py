import platform
import shutil
import socket
import subprocess
from datetime import datetime


# ==============================
# SYSTEM INFORMATION
# ==============================

def get_system_info():
    return {
        "Hostname": platform.node(),
        "Operating System": platform.system(),
        "OS Release": platform.release(),
        "Architecture": platform.machine()
    }


# ==============================
# CPU MONITORING
# ==============================

def get_cpu_usage():
    try:
        result = subprocess.run(
            ["bash", "-c", "top -bn1 | grep 'Cpu(s)'"],
            capture_output=True,
            text=True
        )

        line = result.stdout.strip()

        if "id" in line:
            idle = float(line.split("id")[0].split()[-1])
            return round(100 - idle, 2)

        return None

    except Exception:
        return None


# ==============================
# MEMORY MONITORING
# ==============================

def get_memory_usage():
    try:
        result = subprocess.run(
            ["free", "-m"],
            capture_output=True,
            text=True
        )

        lines = result.stdout.splitlines()

        memory = lines[1].split()

        total = int(memory[1])
        used = int(memory[2])

        usage = (used / total) * 100

        return round(usage, 2)

    except Exception:
        return None


# ==============================
# DISK MONITORING
# ==============================

def get_disk_usage():
    try:
        total, used, free = shutil.disk_usage("/")

        usage = (used / total) * 100

        return round(usage, 2)

    except Exception:
        return None


# ==============================
# NETWORK CHECK
# ==============================

def check_network():
    try:
        socket.create_connection(
            ("8.8.8.8", 53),
            timeout=3
        )

        return True

    except OSError:
        return False


# ==============================
# DNS CHECK
# ==============================

def check_dns():
    try:
        socket.gethostbyname("google.com")
        return True

    except socket.error:
        return False


# ==============================
# STATUS EVALUATION
# ==============================

def evaluate_usage(value, warning, critical):

    if value is None:
        return "UNKNOWN"

    if value >= critical:
        return "CRITICAL"

    if value >= warning:
        return "WARNING"

    return "NORMAL"


# ==============================
# REPORT GENERATION
# ==============================

def generate_report():

    cpu = get_cpu_usage()
    memory = get_memory_usage()
    disk = get_disk_usage()

    network = check_network()
    dns = check_dns()

    cpu_status = evaluate_usage(cpu, 70, 90)
    memory_status = evaluate_usage(memory, 70, 90)
    disk_status = evaluate_usage(disk, 80, 90)

    print("=" * 55)
    print("        LINUX SYSTEM HEALTH REPORT")
    print("=" * 55)

    print(f"Generated: {datetime.now()}")

    print("\n[SYSTEM INFORMATION]")

    for key, value in get_system_info().items():
        print(f"{key}: {value}")

    print("\n[RESOURCE HEALTH]")

    print(
        f"CPU Usage    : {cpu}%  [{cpu_status}]"
    )

    print(
        f"Memory Usage : {memory}%  [{memory_status}]"
    )

    print(
        f"Disk Usage   : {disk}%  [{disk_status}]"
    )

    print("\n[NETWORK HEALTH]")

    print(
        f"Internet Connectivity : "
        f"{'CONNECTED' if network else 'FAILED'}"
    )

    print(
        f"DNS Resolution        : "
        f"{'OK' if dns else 'FAILED'}"
    )

    print("\n[DIAGNOSTIC SUMMARY]")

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

    if not issues:
        print("No major issues detected.")
        overall = "HEALTHY"

    else:

        for issue in issues:
            print(f"- {issue}")

        overall = "ATTENTION REQUIRED"

    print("\nOverall Status:", overall)

    print("=" * 55)


# ==============================
# MAIN
# ==============================

if __name__ == "__main__":
    generate_report()
