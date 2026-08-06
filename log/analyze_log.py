#!/usr/bin/env python3

import argparse
import json
import os
import re
from collections import Counter

LOG_PATTERN = re.compile(
    r'^(?P<ip>\S+) \S+ \S+ \[(?P<date>[^\]]+)\] '
    r'"(?P<method>\S+) (?P<url>\S+)(?: [^"]*)?" '
    r'.* (?P<duration>\d+)$'
)

HTTP_METHODS = ("GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD")


def parse_line(line):
    match = LOG_PATTERN.match(line.rstrip("\n"))
    if not match:
        return None
    return {
        "ip": match.group("ip"),
        "date": f"[{match.group('date')}]",
        "method": match.group("method"),
        "url": match.group("url"),
        "duration": int(match.group("duration")),
    }


def update_top_longest(top, entry):
    if len(top) < 3:
        top.append(entry)
        top.sort(key=lambda item: item["duration"], reverse=True)
        return
    if entry["duration"] > top[-1]["duration"]:
        top.append(entry)
        top.sort(key=lambda item: item["duration"], reverse=True)
        del top[3:]


def analyze_log(path):
    ip_counter = Counter()
    method_counter = Counter()
    top_longest = []
    total_requests = 0

    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            if not line.strip():
                continue
            total_requests += 1
            parsed = parse_line(line)
            if not parsed:
                continue

            ip_counter[parsed["ip"]] += 1
            if parsed["method"] in HTTP_METHODS:
                method_counter[parsed["method"]] += 1
            update_top_longest(top_longest, parsed)

    return {
        "top_ips": dict(ip_counter.most_common(3)),
        "top_longest": top_longest,
        "total_stat": dict(method_counter),
        "total_requests": total_requests,
    }


def output_path_for(log_path):
    stem = os.path.splitext(os.path.basename(log_path))[0]
    return f"{stem}.json"


def process_log(log_path):
    stats = analyze_log(log_path)
    text = json.dumps(stats, indent=2, ensure_ascii=False)
    print(text)

    out_name = output_path_for(log_path)
    with open(out_name, "w", encoding="utf-8") as f:
        f.write(text)
        f.write("\n")
    return out_name


def collect_log_files(path):
    if os.path.isfile(path):
        return [path]
    if os.path.isdir(path):
        files = []
        for name in sorted(os.listdir(path)):
            full = os.path.join(path, name)
            if os.path.isfile(full) and name.endswith(".log"):
                files.append(full)
        return files
    raise SystemExit(f"Путь не является файлом или директорией: {path}")


def main():
    parser = argparse.ArgumentParser(
        description="Анализ access-логов веб-сервера"
    )
    parser.add_argument(
        "path",
        help="Путь к лог-файлу или директории с логами",
    )
    args = parser.parse_args()

    log_files = collect_log_files(args.path)
    if not log_files:
        raise SystemExit(f"Лог-файлы не найдены: {args.path}")

    for log_file in log_files:
        process_log(log_file)


if __name__ == "__main__":
    main()
