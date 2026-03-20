from __future__ import annotations

import os
import shlex
import subprocess
from pathlib import Path
from typing import Iterable


def shell_join(command: Iterable[object]) -> str:
    return shlex.join(str(part) for part in command)


def run_command(
    command: list[object],
    cwd: str | Path | None = None,
    env: dict[str, object] | None = None,
    dry_run: bool = False,
) -> int:
    pretty_command = shell_join(command)
    if cwd:
        print(f"[cwd] {Path(cwd)}")
    if env:
        for key, value in env.items():
            print(f"[env] {key}={value}")
    print(f"[cmd] {pretty_command}")

    if dry_run:
        return 0

    merged_env = os.environ.copy()
    if env:
        merged_env.update({key: str(value) for key, value in env.items()})

    subprocess.run(
        [str(part) for part in command],
        cwd=str(cwd) if cwd else None,
        env=merged_env,
        check=True,
    )
    return 0
