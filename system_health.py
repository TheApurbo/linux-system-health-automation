import platform
import shutil
import subprocess
from datetime import datetime


def get_cpu_info():
    try:
        result = subprocess.run(
            ["bash", "-c", "top -bn1 | grep 'Cpu(s)'"],
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"CPU check failed: {e}"


def get_memory_info():
    try:
        result = subprocess.run(
            ["free", "-h"],
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Memory check failed: {e}"


def get_disk_info():
    try:
        total, used, free = shutil.disk_usage("/")
        used_percent = (used / total) * 100

        return {
            "total": round(total / (1024**3), 2),
            "used": round(used / (1024**3), 2),
            "free": round(free / (1024**3), 2),
            "used_percent": round(used_percent, 2)
        }
    except Exception as e:
        return f"Disk check failed: {e}"


def get_system_info():
    return {
        "hostname": platform.node(),
        "system": platform.system(),
        "release": platform.release(),
        "architecture": platform.machine()
    }


def generate_report():
    print("=" * 50)
    print("LINUX SYSTEM HEALTH REPORT")
    print("=" * 50)
    print(f"Generated: {datetime.now()}")

    print("\n[SYSTEM]")
    for key, value in get_system_info().items():
        print(f"{key}: {value}")

    print("\n[CPU]")
    print(get_cpu_info())

    print("\n[MEMORY]")
    print(get_memory_info())

    print("\n[DISK]")
    print(get_disk_info())

    print("\n" + "=" * 50)


if __name__ == "__main__":
    generate_report()
