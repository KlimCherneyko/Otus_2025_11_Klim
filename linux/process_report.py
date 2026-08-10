#!/usr/bin/env python3

import subprocess
from collections import Counter
from datetime import datetime


def get_ps_aux_output():
    result = subprocess.run(
        ["ps", "aux"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def parse_processes(ps_output):
    lines = ps_output.strip().splitlines()
    processes = []
    for line in lines[1:]:
        parts = line.split(None, 10)
        if len(parts) < 11:
            continue
        processes.append({
            "user": parts[0],
            "cpu": float(parts[2]),
            "mem": float(parts[3]),
            "command": parts[10],
        })
    return processes


def truncate_name(name, max_len=20):
    return name[:max_len] if len(name) > max_len else name


def build_report(processes):
    users = sorted({p["user"] for p in processes})
    users_str = ", ".join(f"'{u}'" for u in users)

    per_user = Counter(p["user"] for p in processes)
    user_lines = "\n".join(
        f"{user}: {count}" for user, count in per_user.most_common()
    )

    total_mem = sum(p["mem"] for p in processes)
    total_cpu = sum(p["cpu"] for p in processes)

    max_mem = max(processes, key=lambda p: p["mem"])
    max_cpu = max(processes, key=lambda p: p["cpu"])

    return (
        "Отчёт о состоянии системы:\n"
        f"Пользователи системы: {users_str}\n"
        f"Процессов запущено: {len(processes)}\n"
        "\n"
        "Пользовательских процессов:\n"
        f"{user_lines}\n"
        "\n"
        f"Всего памяти используется: {total_mem:.1f}%\n"
        f"Всего CPU используется: {total_cpu:.1f}%\n"
        f"Больше всего памяти использует: {truncate_name(max_mem['command'])}\n"
        f"Больше всего CPU использует: {truncate_name(max_cpu['command'])}\n"
    )


def save_report(report):
    filename = datetime.now().strftime("%d-%m-%Y-%H:%M-scan.txt")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(report)
    return filename


def main():
    processes = parse_processes(get_ps_aux_output())
    report = build_report(processes)
    print(report, end="")
    save_report(report)


if __name__ == "__main__":
    main()
