#!/usr/bin/env python3
"""Capture exact npm package metadata for the ADR-0001 compatibility snapshot."""
from __future__ import annotations

import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "evidence" / "registry-metadata.json"
# `npm` is a shell script on Unix and `npm.cmd` on Windows; resolve either.
NPM = shutil.which("npm") or shutil.which("npm.cmd") or "npm"
PACKAGES = {
    "@nestjs/common": "12.1.3",
    "@nestjs/core": "12.1.3",
    "@nestjs/platform-express": "12.1.3",
    "@nestjs/testing": "12.1.3",
    "@nestjs/cli": "12.0.8",
    "@nestjs/schematics": "12.0.7",
    "@nestjs/config": "12.0.1",
    "@nestjs/swagger": "12.0.2",
    "rxjs": "7.8.2",
    "reflect-metadata": "0.2.2",
    "typescript": "6.0.3",
    "vite": "8.3.4",
    "vitest": "5.0.5",
    "@vitest/coverage-v8": "5.0.5",
    "@vitest/mocker": "5.0.5",
    "oxlint": "1.88.0",
    "prettier": "3.9.10",
    "supertest": "7.3.1",
    "@types/supertest": "7.2.1",
    "@types/node": "22.20.5",
    "@types/express": "5.0.6",
    "class-validator": "0.15.1",
    "class-transformer": "0.5.1",
    "pg": "8.23.1",
    "@types/pg": "8.23.1",
}


def npm_json(*args: str):
    result = subprocess.run(
        [NPM, "view", *args, "--json"],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def main() -> None:
    packages = {}
    for name, version in PACKAGES.items():
        spec = f"{name}@{version}"
        packages[spec] = npm_json(
            spec, "version", "engines", "peerDependencies", "dependencies"
        )

    dist_tags = {}
    for name in PACKAGES:
        dist_tags[name] = npm_json(name, "dist-tags")

    snapshot = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "registry": subprocess.run(
            [NPM, "config", "get", "registry"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip(),
        "node_runtime_test_matrix": ["22.23.3", "24.22.0"],
        "packages": packages,
        "dist_tags": dist_tags,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(snapshot, indent=2, sort_keys=True) + "\n")
    print(f"Wrote {OUTPUT} ({len(packages)} exact package records)")


if __name__ == "__main__":
    main()
