from __future__ import annotations

import argparse
import base64
import subprocess
import time
from pathlib import Path


ROOT = Path(r"D:\Desktop\laingzimuxi")
SCRIPT_PATH = ROOT / "tijiao" / "code" / "qixianghaiyang" / "shiyan" / "exp37_rho_J_weak_fusion_letkf.py"
DATA_DIR = ROOT / "气象海洋" / "气象海洋Day2" / "气象海洋" / "大规模得分验证" / "lorenz96_test_1"
REMOTE_DATA_DIR = "/home/infra/qda_competition/day2_data"
REMOTE_BATCH_DIR = "/home/infra/qda_competition/experiments/day2_exp37_batch"
REMOTE_SCRIPT = "/tmp/day2_exp37_rho_J_weak_fusion_letkf.py"
LAUNCH_STATUS = ROOT / "tijiao" / "day2_exp37_launch_status_clean.txt"
CHECK_STATUS = ROOT / "tijiao" / "day2_exp37_remote_check.txt"
CHUNK_SIZE = 4096
UPLOAD_SPECS = [
    (SCRIPT_PATH, REMOTE_SCRIPT),
    (DATA_DIR / "lorenz96_train.csv", f"{REMOTE_DATA_DIR}/lorenz96_train.csv"),
    (DATA_DIR / "lorenz96_test_1.csv", f"{REMOTE_DATA_DIR}/lorenz96_test_1.csv"),
    (DATA_DIR / "lorenz96_test_2.csv", f"{REMOTE_DATA_DIR}/lorenz96_test_2.csv"),
    (DATA_DIR / "lorenz96_test_3.csv", f"{REMOTE_DATA_DIR}/lorenz96_test_3.csv"),
    (DATA_DIR / "lorenz96_test_4.csv", f"{REMOTE_DATA_DIR}/lorenz96_test_4.csv"),
    (DATA_DIR / "lorenz96_test_5.csv", f"{REMOTE_DATA_DIR}/lorenz96_test_5.csv"),
]


def run_via_jump(commands: list[str], output_path: Path, timeout: float, delay: float = 0.02) -> str:
    proc = subprocess.Popen(
        ["ssh", "-tt", "jump"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=0,
    )
    try:
        # Windows 下从管道阻塞式逐字符等提示符容易卡住，这里改为固定短等待后批量下发命令。
        time.sleep(8.0)
        for cmd in commands:
            proc.stdin.write(cmd + "\n")
            proc.stdin.flush()
            time.sleep(delay)
        proc.stdin.close()
        try:
            out, _ = proc.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            proc.kill()
            out, _ = proc.communicate()
        output_path.write_text(out, encoding="utf-8")
        return out
    finally:
        try:
            proc.kill()
        except Exception:
            pass


def _append_base64_file(commands: list[str], local_path: Path, remote_path: str) -> None:
    encoded = base64.b64encode(local_path.read_bytes()).decode("ascii")
    remote_b64 = f"{remote_path}.b64"
    commands.append(f"rm -f {remote_b64}")
    for i in range(0, len(encoded), CHUNK_SIZE):
        chunk = encoded[i : i + CHUNK_SIZE]
        commands.append(f"printf '%s' '{chunk}' >> {remote_b64}")
    commands.append(f"python3 - <<'PY'")
    commands.append("import base64, pathlib")
    commands.append(f"src = pathlib.Path({remote_b64!r})")
    commands.append(f"dst = pathlib.Path({remote_path!r})")
    commands.append("dst.parent.mkdir(parents=True, exist_ok=True)")
    commands.append("dst.write_bytes(base64.b64decode(src.read_text()))")
    commands.append("print('WROTE', dst)")
    commands.append("PY")


def build_setup_commands() -> list[str]:
    return [
        "stty -echo",
        f"pkill -f {REMOTE_SCRIPT} || true",
        f"mkdir -p {REMOTE_DATA_DIR} {REMOTE_BATCH_DIR}",
        "stty echo",
        "exit",
    ]


def build_upload_file_commands(local_path: Path, remote_path: str) -> list[str]:
    commands = [
        "stty -echo",
        f"mkdir -p {Path(remote_path).parent.as_posix()}",
    ]
    _append_base64_file(commands, local_path, remote_path)
    commands.extend(["stty echo", "exit"])
    return commands


def build_launch_commands() -> list[str]:
    return [
        "stty -echo",
        f"python3 -m py_compile {REMOTE_SCRIPT}",
        (
            "nohup bash -lc '"
            "set -e\n"
            f"BASE={REMOTE_BATCH_DIR}\n"
            f"DATA={REMOTE_DATA_DIR}\n"
            "for i in 1 2 3 4 5; do\n"
            "  OUT=$BASE/test_$i\n"
            "  mkdir -p $OUT\n"
            f"  python3 {REMOTE_SCRIPT} --train-input $DATA/lorenz96_train.csv --test-input $DATA/lorenz96_test_$i.csv --output-dir $OUT > $OUT/run.log 2>&1\n"
            "  cp $OUT/result.csv $BASE/result_test_$i.csv\n"
            "  echo DONE_TEST_$i\n"
            "done\n"
            f"' > {REMOTE_BATCH_DIR}/launcher.log 2>&1 < /dev/null & echo STARTED:$!"
        ),
        "stty echo",
        "exit",
    ]


def build_check_commands() -> list[str]:
    return [
        "stty -echo",
        "echo ==== DAY2_EXP37_CHECK_START ====",
        f"ls -lh {REMOTE_DATA_DIR} || true",
        f"ls -lh {REMOTE_BATCH_DIR} || true",
        f"find {REMOTE_BATCH_DIR} -maxdepth 2 -type f | sort || true",
        f"ps -ef | grep -E '{Path(REMOTE_SCRIPT).name}|day2_exp37_batch' | grep -v grep || true",
        f"tail -n 40 {REMOTE_BATCH_DIR}/launcher.log 2>/dev/null || true",
        "for i in 1 2 3 4 5; do echo ==== TEST:$i ====; tail -n 20 "
        f"{REMOTE_BATCH_DIR}/test_$i/run.log 2>/dev/null || true; done",
        "stty echo",
        "exit",
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="day2 exp37 远端上传与运行工具")
    parser.add_argument("action", choices=["launch", "check"])
    args = parser.parse_args()

    if args.action == "launch":
        all_outputs: list[str] = []
        all_outputs.append(run_via_jump(build_setup_commands(), LAUNCH_STATUS, timeout=60.0))
        for local_path, remote_path in UPLOAD_SPECS:
            all_outputs.append(run_via_jump(build_upload_file_commands(local_path, remote_path), LAUNCH_STATUS, timeout=120.0))
        all_outputs.append(run_via_jump(build_launch_commands(), LAUNCH_STATUS, timeout=60.0))
        LAUNCH_STATUS.write_text("\n".join(all_outputs), encoding="utf-8")
        print(LAUNCH_STATUS)
        return

    out = run_via_jump(build_check_commands(), CHECK_STATUS, timeout=120.0)
    print(CHECK_STATUS)
    print(out)


if __name__ == "__main__":
    main()
