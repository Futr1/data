from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from src.periom_dx.model import legacy_ms_swift_root, require_dependency
from src.utils.config import load_yaml, resolve_path
from src.utils.runner import run_command


def _append_arg(command: list[object], flag: str, value: Any) -> None:
    if value is None:
        return
    if isinstance(value, dict):
        command.extend([flag, json.dumps(value)])
        return
    if isinstance(value, list):
        command.append(flag)
        command.extend(value)
        return
    if isinstance(value, bool):
        command.extend([flag, str(value).lower()])
        return
    command.extend([flag, value])


def build_command(config: dict[str, Any]) -> tuple[list[object], Path]:
    working_dir = resolve_path(config.get("working_dir", legacy_ms_swift_root()))
    require_dependency(working_dir, "ms-swift working directory")

    command: list[object] = ["swift", "sft"]
    _append_arg(command, "--model", config.get("model_name_or_path"))
    _append_arg(command, "--model_type", config.get("model_type"))
    _append_arg(command, "--template", config.get("template"))
    _append_arg(command, "--system", config.get("system_prompt"))
    _append_arg(command, "--dataset", resolve_path(config.get("dataset_path")).as_posix())
    _append_arg(command, "--train_type", config.get("train_type"))
    _append_arg(command, "--torch_dtype", config.get("torch_dtype"))
    _append_arg(command, "--target_modules", config.get("target_modules"))
    _append_arg(command, "--num_train_epochs", config.get("num_train_epochs"))
    _append_arg(command, "--per_device_train_batch_size", config.get("per_device_train_batch_size"))
    _append_arg(command, "--per_device_eval_batch_size", config.get("per_device_eval_batch_size"))
    _append_arg(command, "--gradient_accumulation_steps", config.get("gradient_accumulation_steps"))
    _append_arg(command, "--learning_rate", config.get("learning_rate"))
    _append_arg(command, "--freeze_vit", config.get("freeze_vit"))
    _append_arg(command, "--eval_steps", config.get("eval_steps"))
    _append_arg(command, "--save_steps", config.get("save_steps"))
    _append_arg(command, "--save_total_limit", config.get("save_total_limit"))
    _append_arg(command, "--logging_steps", config.get("logging_steps"))
    _append_arg(command, "--max_length", config.get("max_length"))
    _append_arg(command, "--output_dir", resolve_path(config.get("output_dir")).as_posix())
    _append_arg(command, "--logging_dir", resolve_path(config.get("logging_dir")).as_posix())
    _append_arg(command, "--warmup_ratio", config.get("warmup_ratio"))
    _append_arg(command, "--adam_beta2", config.get("adam_beta2"))
    _append_arg(command, "--lr_scheduler_type", config.get("lr_scheduler_type"))
    _append_arg(command, "--weight_decay", config.get("weight_decay"))
    _append_arg(command, "--dataloader_num_workers", config.get("dataloader_num_workers"))
    _append_arg(command, "--report_to", config.get("report_to"))
    _append_arg(command, "--lora_rank", config.get("lora_rank"))
    _append_arg(command, "--lora_alpha", config.get("lora_alpha"))
    _append_arg(command, "--gradient_checkpointing_kwargs", config.get("gradient_checkpointing_kwargs"))
    _append_arg(command, "--deepspeed", config.get("deepspeed"))
    return command, working_dir


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build or run the PerioM-Dx SFT command.")
    parser.add_argument("--config", default="configs/periom_dx_sft.yaml")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    config = load_yaml(args.config)
    command, working_dir = build_command(config)
    return run_command(command, cwd=working_dir, dry_run=args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
