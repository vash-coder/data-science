import sys
import subprocess
import tempfile
import os


def check_env():
    if sys.prefix == sys.base_prefix:
        raise RuntimeError("Not in virtual environment")


def install_libs():
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write("beautifulsoup4\npytest\n")
        req = f.name

    subprocess.check_call([
        sys.executable, "-m", "pip", "install", "-r", req
    ])

    os.remove(req)


def freeze_and_print():
    result = subprocess.check_output(
        [sys.executable, "-m", "pip", "freeze"],
        text=True
    )

    print(result)

    with open("requirements.txt", "w") as f:
        f.write(result)


def main():
    check_env()
    install_libs()
    freeze_and_print()

if __name__ == "__main__":
    main()
