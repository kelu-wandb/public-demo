import subprocess
import sys
import os

TIMEOUT_SEC = 20


def test_yes_setpgrp_no_import_torch():
    print("Testing YES preexec_fn=os.setpgrp, NO import torch...")
    try:
        proc = subprocess.Popen(
            [
                sys.executable,
                "-c",
                "print('=== SUCCESS: YES os.setpgrp, NO torch import')",
            ],
            preexec_fn=os.setpgrp,
        )

        stdout, stderr = proc.communicate(timeout=TIMEOUT_SEC)
        print("PASS")

    except Exception as e:
        print(f"ERROR: {e}")


def test_no_setpgrp_yes_torch_import():
    print("Testing NO preexec_fn=os.setpgrp, YES import torch...")
    try:
        proc = subprocess.Popen(
            [
                sys.executable,
                "-c",
                "import torch; print('=== SUCCESS: NO os.setpgrp, YES import torch')",
            ]
        )

        stdout, stderr = proc.communicate(timeout=TIMEOUT_SEC)
        print("PASS")

    except Exception as e:
        print(f"ERROR: {e}")


def test_yes_setpgrp_yes_torch_import():
    print("Testing YES preexec_fn=os.setpgrp, YES import torch...")
    try:
        proc = subprocess.Popen(
            [
                sys.executable,
                "-c",
                "import torch; print('=== SUCCESS: YES os.setpgrp, YES import torch')",
            ],
            preexec_fn=os.setpgrp,
        )

        # Wait with timeout
        try:
            stdout, stderr = proc.communicate(timeout=TIMEOUT_SEC)
            print("PASS")
        except subprocess.TimeoutExpired:
            print(f"FAIL: Process timed out after {TIMEOUT_SEC} seconds")
            proc.kill()

    except Exception as e:
        print(f"ERROR: {e}")


if __name__ == "__main__":
    test_yes_setpgrp_no_import_torch()
    test_no_setpgrp_yes_torch_import()
    test_yes_setpgrp_yes_torch_import()
