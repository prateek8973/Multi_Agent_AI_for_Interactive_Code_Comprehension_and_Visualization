import subprocess
import os

TIMEOUT = 5

def run_code(file):
    if file.endswith(".py"):
        return subprocess.run(["python3", file], capture_output=True, text=True, timeout=TIMEOUT)

    elif file.endswith(".js"):
        return subprocess.run(["node", file], capture_output=True, text=True, timeout=TIMEOUT)

    elif file.endswith(".java"):
        classname = file.replace(".java", "")
        subprocess.run(["javac", file])
        return subprocess.run(["java", classname], capture_output=True, text=True, timeout=TIMEOUT)

    elif file.endswith(".cpp"):
        subprocess.run(["g++", file, "-o", "a.out"])
        return subprocess.run(["./a.out"], capture_output=True, text=True, timeout=TIMEOUT)

    else:
        return None


if __name__ == "__main__":
    filename = os.environ.get("FILENAME", "generated.py")

    try:
        result = run_code(filename)

        if result:
            print("STDOUT:\n", result.stdout)
            print("\nSTDERR:\n", result.stderr)
        else:
            print("Unsupported language")

    except subprocess.TimeoutExpired:
        print("Execution timed out")
