"""
RetailX - End-to-End Business Analytics Pipeline

Runs the complete RetailX workflow:

1. Inventory master generation
2. Data cleaning
3. Business analytics
4. Inventory analytics
5. Visualization

Run:
    py main.py
"""

from pathlib import Path
import subprocess
import sys
import time


# ============================================================
# Configuration
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"


PIPELINE = [
    ("Inventory Master Generation", "inventory_master.py"),
    ("Data Cleaning", "data_cleaning.py"),
    ("Business Analytics", "analytics.py"),
    ("Inventory Analytics", "inventory.py"),
    ("Visualization", "visualization.py"),
    ("MySQL Analytics", "mysql_loader.py"),
]


# ============================================================
# Runner
# ============================================================

def run_module(module_name: str) -> bool:
    """
    Execute one project module and return success/failure.
    """

    module_path = SRC_DIR / module_name

    print()
    print("=" * 70)
    print(f"RUNNING: {module_name}")
    print("=" * 70)

    if not module_path.exists():
        print(
            f"ERROR: Module not found: {module_path}"
        )
        return False

    start_time = time.perf_counter()

    result = subprocess.run(
        [sys.executable, str(module_path)],
        cwd=PROJECT_ROOT,
    )

    elapsed = time.perf_counter() - start_time

    print()
    print(
        f"Execution time: {elapsed:.2f} seconds"
    )

    if result.returncode != 0:

        print(
            f"FAILED: {module_name}"
        )

        return False

    print(
        f"SUCCESS: {module_name}"
    )

    return True


# ============================================================
# Pipeline
# ============================================================

def run_pipeline():
    """
    Run all RetailX modules sequentially.
    """

    pipeline_start = time.perf_counter()

    print()
    print("#" * 70)
    print("#" + " " * 18 + "RETAILX PIPELINE" + " " * 34 + "#")
    print("#" * 70)

    successful_steps = 0

    for step_name, module_name in PIPELINE:

        success = run_module(
            module_name
        )

        if not success:

            print()
            print("=" * 70)
            print("PIPELINE FAILED")
            print("=" * 70)

            print(
                f"Failed step: {step_name}"
            )

            return False

        successful_steps += 1

    total_time = (
        time.perf_counter()
        - pipeline_start
    )

    print()
    print("#" * 70)
    print("#" + " " * 16 + "PIPELINE COMPLETED" + " " * 31 + "#")
    print("#" * 70)

    print()
    print(
        f"Successful steps : "
        f"{successful_steps}/{len(PIPELINE)}"
    )

    print(
        f"Total execution  : "
        f"{total_time:.2f} seconds"
    )

    print()
    print(
        "Reports directory:"
    )

    print(
        PROJECT_ROOT / "reports"
    )

    print()
    print(
        "RetailX pipeline completed successfully."
    )

    return True


# ============================================================
# Entry Point
# ============================================================

if __name__ == "__main__":

    success = run_pipeline()

    if not success:
        sys.exit(1)

    sys.exit(0)