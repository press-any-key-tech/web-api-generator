from pathlib import Path
import shutil
import subprocess

SUCCESS = "\x1b[1;32m [SUCCESS]: "
TERMINATOR = "\x1b[0m"
INFO = "\x1b[1;33m [INFO]: "


def remove_files_and_folders(*args: str):
    for path in args:
        p = Path(path)
        if p.is_dir():
            shutil.rmtree(p)
        else:
            p.unlink()


def main():

    if "{{ cookiecutter.use_docker }}" != "y":
        remove_files_and_folders("Dockerfile")

    # # try to format the code
    # try:
    #     print(INFO + "Formatting with black" + TERMINATOR)
    #     subprocess.run(("black", "."), capture_output=True)
    #     print(INFO + "Formatting with isort" + TERMINATOR)
    #     subprocess.run(("isort", "."), capture_output=True)
    # except FileNotFoundError:
    #     print("Fail formatting")

    print(SUCCESS + "Project initialized, keep up the good work!" + TERMINATOR)
    print(
        INFO
        + "If you are using linux or mac, run the following script to configure github actions:"
        + TERMINATOR
    )
    print(
        INFO
        + "If you are using Windows (Powershell), run the following script to configure github actions:"
        + TERMINATOR
    )


if __name__ == "__main__":
    main()
