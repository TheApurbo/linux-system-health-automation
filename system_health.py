import platform
import shutil
import socket
import subprocess
import os
import re
import time
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

        match = re.search(
            r"([\d.,]+)\s*id",
            result.stdout
        )

        if not match:
            return None

        idle = float(
            match.group(1).replace(",", ".")
        )

        return round(100 - idle, 2)

    except (
        ValueError,
        subprocess.SubprocessError,
        OSError
    ):
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

        values = lines[1].split()

        if len(values) < 3:
            return None

        total = int(values[1])
        used = int(values[2])

        if total <= 0:
            return None

        return round(
            (used / total) * 100,
            2
        )

    except (
        ValueError,
        subprocess.SubprocessError,
        OSError
    ):
        return None


# ==========================================
# DISK MONITORING
# ==========================================

def get_disk_usage():
    try:
        total, used, free = shutil.disk_usage("/")

        if total <= 0:
            return None

        return round(
            (used / total) * 100,
            2
        )

    except OSError:
        return None


# ==========================================
# NETWORK CONNECTIVITY
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

    except (socket.gaierror, OSError):
        return False


# ==========================================
# NETWORK INTERFACES
# ==========================================

def get_network_interfaces():
    try:
        result = subprocess.run(
            ["ip", "-brief", "addr"],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode != 0:
            return "Unable to retrieve network interfaces."

        output = result.stdout.strip()

        if not output:
            return "No network interfaces found."

        return output

    except (
        subprocess.SubprocessError,
        OSError
    ):
        return "Unable to retrieve network interfaces."


# ==========================================
# DEFAULT GATEWAY
# ==========================================

def get_default_gateway():
    try:
        result = subprocess.run(
            ["ip", "route", "show", "default"],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode != 0:
            return "UNKNOWN"

        output = result.stdout.strip()

        if not output:
            return "UNKNOWN"

        parts = output.split()

        if "via" in parts:
            index = parts.index("via") + 1

            if index < len(parts):
                return parts[index]

        return "UNKNOWN"

    except (
        subprocess.SubprocessError,
        OSError
    ):
        return "UNKNOWN"


# ==========================================
# TCP NETWORK LATENCY
# ==========================================

def get_tcp_latency(
    host="8.8.8.8",
    port=53,
    timeout=3
):
    try:
        start = time.perf_counter()

        connection = socket.create_connection(
            (host, port),
            timeout=timeout
        )

        connection.close()

        end = time.perf_counter()

        latency = (
            end - start
        ) * 1000

        return round(latency, 2)

    except (
        OSError,
        socket.timeout
    ):
        return None


# ==========================================
# PROCESS ANALYSIS
# ==========================================

def get_top_processes():
    try:
        result = subprocess.run(
            [
                "bash",
                "-c",
                "ps -eo pid,comm,%cpu,%mem "
                "--sort=-%cpu | head -n 6"
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

    except (
        subprocess.SubprocessError,
        OSError
    ):
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

        with open(
            LOG_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            for line in file:

                line = line.strip()

                if line.startswith("INFO"):
                    result["INFO"] += 1

                elif line.startswith("WARNING"):
                    result["WARNING"] += 1

                elif line.startswith("ERROR"):
                    result["ERROR"] += 1
                    result["ERROR_MESSAGES"].append(line)

    except (
        OSError,
        UnicodeError
    ):
        pass

    return result


# ==========================================
# STATUS EVALUATION
# ==========================================

def evaluate_usage(
    value,
    warning,
    critical
):

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
    log_analysis,
    latency
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
            "Check memory-consuming processes using: "
            "ps aux --sort=-%mem"
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
            "Check external connectivity."
        )


    if not dns:

        recommendations.append(
            "Check DNS configuration and test hostname resolution."
        )


    if latency is not None and latency > 100:

        recommendations.append(
            "High network latency detected. "
            "Check network stability and routing."
        )


    if log_analysis["ERROR"] > 0:

        recommendations.append(
            "Review ERROR entries in logs.log."
        )


    if log_analysis["WARNING"] > 0:

        recommendations.append(
            "Review WARNING entries in logs.log."
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

    network_interfaces = get_network_interfaces()

    gateway = get_default_gateway()

    latency = get_tcp_latency()

    log_analysis = analyze_logs()


    # --------------------------------------
    # RESOURCE STATUS
    # --------------------------------------

    cpu_status = evaluate_usage(
        cpu,
        70,
        90
    )

    memory_status = evaluate_usage(
        memory,
        70,
        90
    )

    disk_status = evaluate_usage(
        disk,
        80,
        90
    )


    # --------------------------------------
    # ISSUE DETECTION
    # --------------------------------------

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


    if latency is not None and latency > 100:

        issues.append(
            f"High network latency detected: {latency} ms."
        )


    if log_analysis["ERROR"] > 0:

        issues.append(
            f"{log_analysis['ERROR']} ERROR entry/entries "
            "detected in logs."
        )


    if log_analysis["WARNING"] > 0:

        issues.append(
            f"{log_analysis['WARNING']} WARNING entry/entries "
            "detected in logs."
        )


    # --------------------------------------
    # OVERALL STATUS
    # --------------------------------------

    overall = (
        "ATTENTION REQUIRED"
        if issues
        else "HEALTHY"
    )


    # --------------------------------------
    # RECOMMENDATIONS
    # --------------------------------------

    recommendations = get_recommendations(
        cpu_status,
        memory_status,
        disk_status,
        network,
        dns,
        log_analysis,
        latency
    )


    # ======================================
    # BUILD REPORT
    # ======================================

    report = []


    report.append("=" * 60)

    report.append(
        "          LINUX SYSTEM HEALTH REPORT"
    )

    report.append("=" * 60)

    report.append(
        f"Generated: {datetime.now()}"
    )


    # ======================================
    # SYSTEM INFORMATION
    # ======================================

    report.append(
        "\n[SYSTEM INFORMATION]"
    )

    for key, value in get_system_info().items():

        report.append(
            f"{key}: {value}"
        )


    # ======================================
    # RESOURCE HEALTH
    # ======================================

    report.append(
        "\n[RESOURCE HEALTH]"
    )

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


    # ======================================
    # NETWORK HEALTH
    # ======================================

    report.append(
        "\n[NETWORK HEALTH]"
    )

    report.append(
        "Internet Connectivity : "
        + (
            "CONNECTED"
            if network
            else "FAILED"
        )
    )

    report.append(
        "DNS Resolution        : "
        + (
            "OK"
            if dns
            else "FAILED"
        )
    )


    # ======================================
    # NETWORK DIAGNOSTICS
    # ======================================

    report.append(
        "\n[NETWORK DIAGNOSTICS]"
    )

    report.append(
        "Default Gateway       : "
        + gateway
    )

    report.append(
        "Network Latency       : "
        + (
            f"{latency} ms"
            if latency is not None
            else "UNAVAILABLE"
        )
    )

    report.append(
        "Latency Method        : "
        + (
            "TCP Connection"
            if latency is not None
            else "Unavailable"
        )
    )

    report.append(
        "\nNetwork Interfaces:"
    )

    report.append(
        network_interfaces
    )


    # ======================================
    # PROCESS ANALYSIS
    # ======================================

    report.append(
        "\n[TOP PROCESSES BY CPU USAGE]"
    )

    report.append(
        get_top_processes()
    )


    # ======================================
    # LOG ANALYSIS
    # ======================================

    report.append(
        "\n[LOG ANALYSIS]"
    )

    report.append(
        f"INFO entries    : "
        f"{log_analysis['INFO']}"
    )

    report.append(
        f"WARNING entries : "
        f"{log_analysis['WARNING']}"
    )

    report.append(
        f"ERROR entries   : "
        f"{log_analysis['ERROR']}"
    )


    if log_analysis["ERROR_MESSAGES"]:

        report.append(
            "\nDetected ERROR messages:"
        )

        for message in log_analysis["ERROR_MESSAGES"]:

            report.append(
                f"- {message}"
            )


    # ======================================
    # DIAGNOSTIC SUMMARY
    # ======================================

    report.append(
        "\n[DIAGNOSTIC SUMMARY]"
    )

    report.append(
        "Internet Connectivity : "
        + (
            "PASS"
            if network
            else "FAIL"
        )
    )

    report.append(
        "DNS Resolution        : "
        + (
            "PASS"
            if dns
            else "FAIL"
        )
    )

    report.append(
        "Network Latency       : "
        + (
            f"{latency} ms (TCP Connection)"
            if latency is not None
            else "UNAVAILABLE"
        )
    )

    report.append(
        f"CPU Health            : {cpu_status}"
    )

    report.append(
        f"Memory Health         : {memory_status}"
    )

    report.append(
        f"Disk Health           : {disk_status}"
    )

    report.append(
        f"Log Errors            : {log_analysis['ERROR']}"
    )

    report.append(
        f"Log Warnings          : {log_analysis['WARNING']}"
    )


    if issues:

        report.append(
            "\nDetected Issues:"
        )

        for issue in issues:

            report.append(
                f"- {issue}"
            )

    else:

        report.append(
            "\nNo major issues detected."
        )


    report.append(
        f"\nOverall Status: {overall}"
    )


    # ======================================
    # TROUBLESHOOTING RECOMMENDATIONS
    # ======================================

    report.append(
        "\n[TROUBLESHOOTING RECOMMENDATIONS]"
    )

    for recommendation in recommendations:

        report.append(
            f"- {recommendation}"
        )


    # ======================================
    # END OF REPORT
    # ======================================

    report.append(
        "\n" + "=" * 60
    )

    report.append(
        "             END OF HEALTH REPORT"
    )

    report.append(
        "=" * 60
    )


    final_report = "\n".join(report)


    # ======================================
    # PRINT REPORT
    # ======================================

    print(final_report)


    # ======================================
    # SAVE REPORT
    # ======================================

    try:

        os.makedirs(
            REPORT_DIR,
            exist_ok=True
        )

        with open(
            REPORT_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(final_report)

        print(
            f"\nReport saved to: {REPORT_FILE}"
        )

    except OSError as error:

        print(
            f"\nUnable to save report: {error}"
        )


# ==========================================
# PROGRAM ENTRY POINT
# ==========================================

if __name__ == "__main__":

    generate_report()
