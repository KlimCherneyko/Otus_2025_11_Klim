#!/usr/bin/env python3
"""HTTP echo server using only the standard library."""

from __future__ import annotations

import argparse
import socket
from http import HTTPStatus
from urllib.parse import parse_qs, urlparse


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 5000
RECV_SIZE = 4096


def recv_until_headers(conn: socket.socket) -> bytes:
    data = b""
    while b"\r\n\r\n" not in data:
        chunk = conn.recv(RECV_SIZE)
        if not chunk:
            break
        data += chunk
    return data


def parse_request(raw: bytes) -> tuple[str, str, list[tuple[str, str]]]:
    text = raw.decode("iso-8859-1", errors="replace")
    header_block = text.split("\r\n\r\n", 1)[0]
    lines = header_block.split("\r\n")
    if not lines or not lines[0]:
        raise ValueError("Empty request")

    parts = lines[0].split()
    if len(parts) < 2:
        raise ValueError("Malformed request line")

    method, path = parts[0], parts[1]
    headers: list[tuple[str, str]] = []
    for line in lines[1:]:
        if not line or ":" not in line:
            continue
        name, value = line.split(":", 1)
        headers.append((name.strip(), value.strip()))
    return method, path, headers


def resolve_status(path: str) -> HTTPStatus:
    query = parse_qs(urlparse(path).query)
    values = query.get("status", [])
    if not values:
        return HTTPStatus.OK
    raw = values[0]
    try:
        code = int(raw)
        return HTTPStatus(code)
    except (ValueError, KeyError):
        return HTTPStatus.OK


def build_body(
    method: str,
    addr: tuple[str, int],
    status: HTTPStatus,
    headers: list[tuple[str, str]],
) -> str:
    lines = [
        f"Request Method: {method}",
        f"Request Source: {addr}",
        f"Response Status: {status.value} {status.phrase}",
    ]
    for name, value in headers:
        lines.append(f"{name}: {value}")
    return "\r\n".join(lines)


def build_response(status: HTTPStatus, body: str) -> bytes:
    body_bytes = body.encode("utf-8")
    response = (
        f"HTTP/1.1 {status.value} {status.phrase}\r\n"
        f"Content-Type: text/plain\r\n"
        f"Content-Length: {len(body_bytes)}\r\n"
        f"Connection: close\r\n"
        f"\r\n"
    ).encode("utf-8") + body_bytes
    return response


def handle_client(conn: socket.socket, addr: tuple[str, int]) -> None:
    try:
        raw = recv_until_headers(conn)
        if not raw:
            return
        method, path, headers = parse_request(raw)
        status = resolve_status(path)
        body = build_body(method, addr, status, headers)
        conn.sendall(build_response(status, body))
    except Exception:
        error = HTTPStatus.INTERNAL_SERVER_ERROR
        body = f"Response Status: {error.value} {error.phrase}"
        try:
            conn.sendall(build_response(error, body))
        except OSError:
            pass
    finally:
        conn.close()


def run_server(host: str, port: int) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen()
        print(f"Echo server listening on http://{host}:{port}")
        while True:
            conn, addr = server.accept()
            handle_client(conn, addr)


def main() -> None:
    parser = argparse.ArgumentParser(description="HTTP echo server")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    args = parser.parse_args()
    run_server(args.host, args.port)


if __name__ == "__main__":
    main()
