#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path


def run_command(command, cwd):
    """Runs a command and prints its output in real-time."""
    print(f"▶️  Running: {' '.join(command)}")
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        cwd=cwd,
    )

    output_lines = []
    for line in iter(process.stdout.readline, ""):
        print(f"   {line.strip()}")
        output_lines.append(line)

    process.wait()
    return process.returncode, "".join(output_lines)


def main():
    """
    Runs a series of CI checks: linting, testing, and building.
    Exits with a non-zero code if any step fails.
    """
    project_root = Path(__file__).parent.parent
    print("🚀 Starting CI Checks...")
    print("=" * 40)

    # --- 1. Linting with Pylint ---
    print("\n[Step 1/3]  Linting code with Pylint...")
    lint_return_code, _ = run_command(
        [
            sys.executable,
            "-m",
            "pylint",
            "src",
            "features",
            "scripts",
            "--rcfile=.pylintrc",
            "--exit-zero",
        ],
        cwd=project_root,
    )
    print("✅ Linting check finished.")

    # --- 2. Running Tests with Pytest ---
    print("\n[Step 2/3] Running tests with Pytest...")
    test_return_code, _ = run_command(
        [sys.executable, "-m", "pytest", "-s", "tests/"], cwd=project_root
    )
    if test_return_code != 0:
        print("❌ Pytest failed. Aborting release.")
        sys.exit(1)
    print("✅ All tests passed.")

    # --- 3. Building the Project ---
    print("\n[Step 3/3] Building project with 'build'...")
    subprocess.run(["rm", "-rf", str(project_root / "dist")], check=False)

    build_return_code, _ = run_command(
        [sys.executable, "-m", "build"], cwd=project_root
    )
    if build_return_code != 0:
        print("❌ Build failed. Aborting release.")
        sys.exit(1)

    dist_dir = project_root / "dist"
    artifacts = list(dist_dir.glob("*"))
    if artifacts:
        print("✅ Build successful. Artifacts created:")
        for artifact in artifacts:
            print(f"   📦 {artifact.name}")
    else:
        print("❌ Build process ran but no artifacts were found. Aborting.")
        sys.exit(1)

    print("\n" + "=" * 40)
    print("🎉 All CI checks passed successfully!")
    sys.exit(0)


if __name__ == "__main__":
    main()