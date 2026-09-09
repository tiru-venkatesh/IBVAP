"""
Run this ONCE, immediately after `pip install -r requirements.txt`, every time
you (re)install dependencies.

Why this exists:
  ultralytics depends on plain `opencv-python` (unpinned, not something we
  control from requirements.txt). That package and opencv-python-headless
  install into the same `cv2` folder on disk, and pip does not guarantee our
  pinned headless version installs *after* ultralytics pulls in its own copy.
  Whichever one installs last silently overwrites the other. This script
  removes the conflicting plain build and force-reinstalls the pinned
  headless build with no extra dependency resolution, so the outcome is
  deterministic instead of "whatever order pip felt like today".

Usage:
    python -m pip install -r requirements.txt
    python fix_opencv.py
"""
import subprocess
import sys

HEADLESS_VERSION = "4.11.0.86"


def run(cmd):
    print(f"$ {' '.join(cmd)}")
    subprocess.run(cmd, check=False)


def main():
    py = sys.executable

    # Remove the conflicting plain build if ultralytics pulled it in.
    run([py, "-m", "pip", "uninstall", "-y", "opencv-python"])
    run([py, "-m", "pip", "uninstall", "-y", "opencv-contrib-python"])

    # Force the correct headless build back in, ignoring its own dependency
    # resolution so it can't reintroduce plain opencv-python.
    run([
        py, "-m", "pip", "install",
        "--force-reinstall", "--no-deps",
        f"opencv-python-headless=={HEADLESS_VERSION}",
    ])

    # Verify.
    result = subprocess.run(
        [py, "-c", "import cv2; print(cv2.__version__); print(hasattr(cv2, 'CascadeClassifier'))"],
        capture_output=True, text=True,
    )
    print(result.stdout.strip())
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        print("cv2 import failed after fix - see error above.", file=sys.stderr)
        sys.exit(1)

    if HEADLESS_VERSION in result.stdout and "True" in result.stdout:
        print(f"\ncv2 is now correctly on opencv-python-headless {HEADLESS_VERSION}.")
    else:
        print("\nWARNING: cv2 version/CascadeClassifier check did not match expected output. "
              "Re-run this script, or check for another package reinstalling opencv-python.")


if __name__ == "__main__":
    main()
