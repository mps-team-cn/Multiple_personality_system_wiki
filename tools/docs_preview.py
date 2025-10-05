#!/usr/bin/env python3
"""Plurality Wiki 本地预览辅助脚本。

默认直接启动 Python `http.server`（端口 4173），
如需 docsify-cli 预览可显式指定对应参数。
"""

from __future__ import annotations

import argparse
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path
from typing import Iterable, Optional

DEFAULT_PORT = 4173
DEFAULT_WAIT_SECONDS = 3.0
DOCSIFY_REGISTRIES = (
    "https://registry.npmjs.org",
    "https://registry.npmmirror.com",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Plurality Wiki 本地预览脚本：默认 Python 服务器，可选 docsify。"
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="要预览的目录，默认当前目录。",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help=f"监听端口（默认 {DEFAULT_PORT}）。",
    )
    parser.add_argument(
        "--docsify",
        action="store_true",
        help="启用 docsify-cli 预览（默认关闭）。",
    )
    parser.add_argument(
        "--wait",
        type=float,
        default=DEFAULT_WAIT_SECONDS,
        help=(
            "在启用 docsify 时等待其启动的秒数，用于检测是否成功。"
            f"（默认 {DEFAULT_WAIT_SECONDS} 秒）"
        ),
    )
    return parser.parse_args()


def ensure_directory(path: Path) -> Path:
    resolved = path.expanduser().resolve()
    if not resolved.exists():
        raise SystemExit(f"[错误] 目标目录不存在：{resolved}")
    if not resolved.is_dir():
        raise SystemExit(f"[错误] 目标路径不是目录：{resolved}")
    return resolved


def port_is_available(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind(("127.0.0.1", port))
        except OSError:
            return False
    return True


def try_launch_docsify(
    directory: Path,
    port: int,
    wait_seconds: float,
    registries: Iterable[str],
) -> Optional[subprocess.Popen]:
    npx_path = shutil.which("npx")
    if not npx_path:
        print("[提示] 未检测到 npx，可直接使用 Python 回退方案。")
        return None

    for registry in registries:
        command = [
            npx_path,
            "--yes",
            f"--registry={registry}",
            "docsify-cli@latest",
            "serve",
            str(directory),
            "--port",
            str(port),
        ]
        print(f"[info] 尝试使用 npm registry {registry} 启动 docsify...")
        try:
            process = subprocess.Popen(command, cwd=directory)
        except FileNotFoundError:
            print("[warn] 无法执行 docsify-cli（npx 未安装或权限不足）。")
            return None
        except OSError as exc:
            print(f"[warn] 启动 docsify 失败：{exc}")
            continue

        time.sleep(wait_seconds)
        if process.poll() is None:
            print(
                "[success] docsify-cli 已启动。按 Ctrl+C 结束服务。"
                f" → http://127.0.0.1:{port}/"
            )
            return process

        print(
            "[warn] docsify-cli 进程提前退出。"
            f"（退出码：{process.returncode}）"
        )

    print("[info] docsify 启动失败，将回退到 Python 静态服务器。")
    return None


def launch_python_server(directory: Path, port: int) -> subprocess.Popen:
    if not port_is_available(port):
        raise SystemExit(
            f"[错误] 端口 {port} 已被占用，请使用 --port 指定其他端口。"
        )

    command = [sys.executable, "-m", "http.server", str(port)]
    print(
        "[fallback] 启动 Python 静态服务器。按 Ctrl+C 结束服务。"
        f" → http://127.0.0.1:{port}/"
    )
    return subprocess.Popen(command, cwd=directory)


def wait_for_process(process: subprocess.Popen) -> int:
    try:
        return process.wait()
    except KeyboardInterrupt:
        print("\n[info] 收到中断信号，正在停止服务...")
        process.terminate()
        try:
            return process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            return process.wait()


def main() -> int:
    args = parse_args()
    directory = ensure_directory(Path(args.directory))

    process: Optional[subprocess.Popen]

    if args.docsify:
        process = try_launch_docsify(directory, args.port, args.wait, DOCSIFY_REGISTRIES)

        if process is not None:
            exit_code = wait_for_process(process)
            print(f"[info] docsify 服务已结束（退出码：{exit_code}）。")
            if exit_code == 0:
                return 0
            print("[warn] docsify-cli 未能保持运行，将尝试 Python 静态服务器。")

    process = launch_python_server(directory, args.port)
    exit_code = wait_for_process(process)
    print(f"[info] 服务已结束（退出码：{exit_code}）。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
