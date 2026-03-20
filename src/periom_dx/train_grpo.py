from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from src.periom_dx.model import legacy_r1_v_root, require_dependency
from src.utils.config import load_yaml, resolve_path
from src.utils.runner import run_command


def _append_arg(command: list[object], flag: str, value: Any) -> None:
    if value is None:
        return
    if isinstance(value, list):
        command.append(flag)
        command.extend(value)
        return
    if isinstance(value, dict):
        command.extend([flag, json.dumps(value)])
        return
    if isinstance(value, bool):
        command.extend([flag, str(value).lower()])
        return
    command.extend([flag, value])


def build_command(config: dict[str, Any]) -> tuple[list[object], Path, dict[str, Any]]:
    working_dir = resolve_path(config.get("working_dir", legacy_r1_v_root() / "src" / "r1-v"))
    require_dependency(working_dir, "R1-V working directory")

    torchrun = config.get("torchrun", {})
    script_path = config.get("script", "src/open_r1/grpo.py")
    command: list[object] = [
        "torchrun",
        "--nproc_per_node",
        torchrun.get("nproc_per_node", 1),
        "--nnodes",
        torchrun.get("nnodes", 1),
        "--node_rank",
        torchrun.get("node_rank", 0),
        "--master_addr",
        torchrun.get("master_addr", "127.0.0.1"),
        "--master_port",
        torchrun.get("master_port", "12345"),
        script_path,
    ]

    if config.get("use_vllm"):
        _append_arg(command, "--use_vllm", True)

    _append_arg(command, "--output_dir", resolve_path(config.get("output_dir")).as_posix())
    _append_arg(command, "--model_name_or_path", config.get("model_name_or_path"))
    _append_arg(command, "--dataset_name", config.get("dataset_name"))
    _append_arg(command, "--max_prompt_length", config.get("max_prompt_length"))
    _append_arg(command, "--max_completion_length", config.get("max_completion_length"))
    _append_arg(command, "--per_device_train_batch_size", config.get("per_device_train_batch_size"))
    _append_arg(command, "--gradient_accumulation_steps", config.get("gradient_accumulation_steps"))
    _append_arg(command, "--learning_rate", config.get("learning_rate"))
    _append_arg(command, "--lr_scheduler_type", config.get("lr_scheduler_type"))
    _append_arg(command, "--logging_steps", config.get("logging_steps"))
    _append_arg(command, "--bf16", config.get("bf16"))
    _append_arg(command, "--gradient_checkpointing", config.get("gradient_checkpointing"))
    _append_arg(command, "--attn_implementation", config.get("attn_implementation"))
    _append_arg(command, "--min_pixels", config.get("min_pixels"))
    _append_arg(command, "--max_pixels", config.get("max_pixels"))
    _append_arg(command, "--num_train_epochs", config.get("num_train_epochs"))
    _append_arg(command, "--run_name", config.get("run_name"))
    _append_arg(command, "--save_steps", config.get("save_steps"))
    _append_arg(command, "--save_total_limit", config.get("save_total_limit"))
    _append_arg(command, "--save_only_model", config.get("save_only_model"))
    _append_arg(command, "--report_to", config.get("report_to"))
    _append_arg(command, "--temperature", config.get("temperature"))
    _append_arg(command, "--num_generations", config.get("num_generations"))
    _append_arg(command, "--reward_funcs", config.get("reward_funcs"))
    _append_arg(command, "--deepspeed", config.get("deepspeed"))
    env = config.get("env", {})
    return command, working_dir, env


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build or run the PerioM-Dx GRPO command.")
    parser.add_argument("--config", default="configs/periom_dx_grpo.yaml")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    config = load_yaml(args.config)
    command, working_dir, env = build_command(config)
    return run_command(command, cwd=working_dir, env=env, dry_run=args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
