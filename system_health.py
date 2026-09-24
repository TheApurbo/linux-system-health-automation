import platform
import shutil
import socket
import subprocess
import os
import datetime
import time


REPORT_DIR = "reports"
REPORT_FILE = os.path.join(REPORT_DIR, "system_health_report.txt")
LOG_FILE = "logs.log"


def get_system_info():
    return {
        "Hostname": socket.gethostname(),
        "OS": platform.system(),
        "Release": platform.release(),
        "Architecture": platform.machine(),
    }


def get_cpu_usage():
    try:
        result = subprocess.check_output(
            "top -bn1 | grep 'Cpu(s)'",
            shell=True,
            text=True
        )

        idle = float(result.split("id,")[0].split()[-1])

        return round(100 - idle, 2)

    except Exception:
        return None


def get_memory_usage():
    try:
        result = subprocess.check_output(
            ["free", "-m"],
            text=True
        )

        lines = result.splitlines()
        memory_line = lines[1].split()

        total = int(memory_line[1])
        used = int(memory_line[2])

        return round((used / total) * 100, 2)

    except Exception:
        return None


def get_disk_usage():
    try:
        usage = shutil.disk_usage("/")

        return round(
            (usage.used / usage.total) * 100,
            2
        )

    except Exception:
        return None


def check_network():
    try:
        connection = socket.create_connection(
            ("8.8.8.8", 53),
            timeout=3
        )

        connection.close()

        return True

    except Exception:
        return False


def check_dns():
    try:
        socket.gethostbyname("google.com")

        return True

    except Exception:
        return False


def get_network_interfaces():
    try:
        result = subprocess.check_output(
            ["ip", "-brief", "addr"],
            text=True
        )

        return result.strip()

    except Exception:
        return "UNAVAILABLE"


def get_default_gateway():
    try:
        result = subprocess.check_output(
            ["ip", "route", "show", "default"],
            text=True
        )

        if result.strip():
            return result.strip()

        return "UNAVAILABLE"

    except Exception:
        return "UNAVAILABLE"


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

        latency = (end - start) * 1000

        return round(latency, 2)

    except (OSError, socket.timeout):
        return None


def get_top_processes():
    try:
        result = subprocess.check_output(
            "ps -eo pid,comm,%cpu,%mem "
            "--sort=-%cpu | head -n 6",
            shell=True,
            text=True
        )

        return result.strip()

    except Exception:
        return "UNAVAILABLE"


def analyze_logs():

    info_count = 0
    warning_count = 0
    error_count = 0

    errors = []

    if not os.path.exists(LOG_FILE):
        return {
            "INFO": 0,
            "WARNING": 0,
            "ERROR": 0,
            "ERROR_MESSAGES": []
        }

    try:

        with open(LOG_FILE, "r") as file:

            for line in file:

                line = line.strip()

                if "INFO" in line:
                    info_count += 1

                if "WARNING" in line:
                    warning_count += 1

                if "ERROR" in line:
                    error_count += 1
                    errors.append(line)

    except Exception:
        pass

    return {
        "INFO": info_count,
        "WARNING": warning_count,
        "ERROR": error_count,
        "ERROR_MESSAGES": errors
    }


def evaluate_usage(
    value,
    warning,
    critical
):

    if value is None:
        return "UNAVAILABLE"

    if value >= critical:
        return "CRITICAL"

    if value >= warning:
        return "WARNING"

    return "HEALTHY"


def get_recommendations(
    cpu_status,
    memory_status,
    disk_status,
    network_ok,
    dns_ok,
    log_data
):

    recommendations = []

    if cpu_status in ["WARNING", "CRITICAL"]:
        recommendations.append(
            "Review high CPU-consuming processes."
        )

    if memory_status in ["WARNING", "CRITICAL"]:
        recommendations.append(
            "Check memory-consuming processes and applications."
        )

    if disk_status in ["WARNING", "CRITICAL"]:
        recommendations.append(
            "Clean unnecessary files or increase disk capacity."
        )

    if not network_ok:
        recommendations.append(
            "Check network connectivity and interface configuration."
        )

    if not dns_ok:
        recommendations.append(
            "Check DNS configuration and resolver connectivity."
        )

    if log_data["ERROR"] > 0:
        recommendations.append(
            "Review ERROR entries in logs.log."
        )

    if log_data["WARNING"] > 0:
        recommendations.append(
            "Review WARNING entries in logs.log."
        )

    if not recommendations:
        recommendations.append(
            "No immediate issues detected."
        )

    return recommendations


def generate_report():

    os.makedirs(
        REPORT_DIR,
        exist_ok=True
    )

    # Collect system information

    system_info = get_system_info()

    cpu = get_cpu_usage()

    memory = get_memory_usage()

    disk = get_disk_usage()

    network_ok = check_network()

    dns_ok = check_dns()

    interfaces = get_network_interfaces()

    gateway = get_default_gateway()

    latency = get_tcp_latency()

    processes = get_top_processes()

    log_data = analyze_logs()


    # Evaluate resource health

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
        75,
        90
    )


    # Overall status

    overall_status = "HEALTHY"

    if (
        cpu_status in ["WARNING", "CRITICAL"]
        or memory_status in ["WARNING", "CRITICAL"]
        or disk_status in ["WARNING", "CRITICAL"]
        or not network_ok
        or not dns_ok
        or log_data["ERROR"] > 0
    ):

        overall_status = "ATTENTION REQUIRED"


    # Recommendations

    recommendations = get_recommendations(
        cpu_status,
        memory_status,
        disk_status,
        network_ok,
        dns_ok,
        log_data
    )


    # Build report

    report = []

    report.append("=" * 60)

    report.append(
        "LINUX SYSTEM HEALTH & TROUBLESHOOTING REPORT"
    )

    report.append("=" * 60)

    report.append(
        "Generated: "
        + datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )

    report.append("")


    # System Information

    report.append("[SYSTEM INFORMATION]")

    report.append(
        f"Hostname         : {system_info['Hostname']}"
    )

    report.append(
        f"Operating System : {system_info['OS']}"
    )

    report.append(
        f"Release          : {system_info['Release']}"
    )

    report.append(
        f"Architecture     : {system_info['Architecture']}"
    )

    report.append("")


    # Resource Usage

    report.append("[RESOURCE USAGE]")

    if cpu is not None:

        report.append(
            f"CPU Usage        : {cpu}% ({cpu_status})"
        )

    else:

        report.append(
            "CPU Usage        : UNAVAILABLE"
        )


    if memory is not None:

        report.append(
            f"Memory Usage     : {memory}% ({memory_status})"
        )

    else:

        report.append(
            "Memory Usage     : UNAVAILABLE"
        )


    if disk is not None:

        report.append(
            f"Disk Usage       : {disk}% ({disk_status})"
        )

    else:

        report.append(
            "Disk Usage       : UNAVAILABLE"
        )

    report.append("")


    # Network Diagnostics

    report.append("[NETWORK DIAGNOSTICS]")

    report.append(
        "Internet Connectivity : "
        + (
            "AVAILABLE"
            if network_ok
            else "UNAVAILABLE"
        )
    )

    report.append(
        "DNS Resolution        : "
        + (
            "WORKING"
            if dns_ok
            else "FAILED"
        )
    )

    report.append("")

    report.append("Network Interfaces:")

    report.append(interfaces)

    report.append("")

    report.append(
        f"Default Gateway       : {gateway}"
    )


    if latency is not None:

        report.append(
            f"Network Latency       : {latency} ms"
        )

        report.append(
            "Latency Method        : TCP Connection"
        )

    else:

        report.append(
            "Network Latency       : UNAVAILABLE"
        )

        report.append(
            "Latency Method        : Unavailable"
        )

    report.append("")


    # Top Processes

    report.append(
        "[TOP PROCESSES BY CPU USAGE]"
    )

    report.append(processes)

    report.append("")


    # Log Analysis

    report.append("[LOG ANALYSIS]")

    report.append(
        f"INFO Entries          : {log_data['INFO']}"
    )

    report.append(
        f"WARNING Entries       : {log_data['WARNING']}"
    )

    report.append(
        f"ERROR Entries         : {log_data['ERROR']}"
    )


    if log_data["ERROR_MESSAGES"]:

        report.append("")

        report.append("Error Messages:")

        for error in log_data["ERROR_MESSAGES"]:

            report.append(
                f"- {error}"
            )

    report.append("")


    # Diagnostic Summary

    report.append("[DIAGNOSTIC SUMMARY]")

    report.append(
        f"Overall Status        : {overall_status}"
    )

    report.append(
        f"CPU Status            : {cpu_status}"
    )

    report.append(
        f"Memory Status         : {memory_status}"
    )

    report.append(
        f"Disk Status           : {disk_status}"
    )

    report.append(
        "Network Connectivity  : "
        + (
            "AVAILABLE"
            if network_ok
            else "UNAVAILABLE"
        )
    )

    report.append(
        "DNS Status            : "
        + (
            "WORKING"
            if dns_ok
            else "FAILED"
        )
    )


    if latency is not None:

        report.append(
            f"Network Latency       : "
            f"{latency} ms (TCP Connection)"
        )

    else:

        report.append(
            "Network Latency       : UNAVAILABLE"
        )

    report.append("")


    # Troubleshooting Recommendations

    report.append(
        "[TROUBLESHOOTING RECOMMENDATIONS]"
    )

    for recommendation in recommendations:

        report.append(
            f"- {recommendation}"
        )

    report.append("")

    report.append("=" * 60)


    # Final report

    final_report = "\n".join(report)


    print(final_report)


    # Save report

    with open(
        REPORT_FILE,
        "w"
    ) as file:

        file.write(final_report)


    print("")

    print(
        f"Report saved to {REPORT_FILE}"
    )


if __name__ == "__main__":

    generate_report()
