from __future__ import annotations

import argparse
import base64
import pathlib
import subprocess


def main() -> None:
    parser = argparse.ArgumentParser(description="通过 ssh -tt jump + base64 静默上传并远端启动脚本")
    parser.add_argument("--local-path", type=pathlib.Path, required=True)
    parser.add_argument("--status-path", type=pathlib.Path, required=True)
    parser.add_argument("--remote-out", required=True)
    parser.add_argument("--remote-script", required=True)
    parser.add_argument("--kill-pattern", default="")
    args = parser.parse_args()

    encoded = base64.b64encode(args.local_path.read_bytes()).decode("ascii")
    args.status_path.parent.mkdir(parents=True, exist_ok=True)

    cmds = []
    if args.kill_pattern:
        cmds.append(f"pkill -f {args.kill_pattern} || true")
    cmds.extend(
        [
            f"mkdir -p {args.remote_out}",
            "python3 - <<'PY'",
            "import base64, pathlib",
            f"content = base64.b64decode(\"\"\"{encoded}\"\"\")",
            f"path = pathlib.Path('{args.remote_script}')",
            "path.write_bytes(content)",
            "print('WROTE', path)",
            "PY",
            f"python3 -m py_compile {args.remote_script}",
            f"nohup python3 {args.remote_script} --output-dir {args.remote_out} > {args.remote_out}/run.log 2>&1 < /dev/null & echo STARTED:$!",
            "exit",
        ]
    )

    command_input = "\n".join(cmds) + "\n"
    result = subprocess.run(
        ["ssh", "-tt", "jump"],
        input=command_input,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        timeout=180,
    )
    output = result.stdout

    args.status_path.write_text(output, encoding="utf-8")


if __name__ == "__main__":
    main()
