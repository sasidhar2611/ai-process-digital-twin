import os
import sys

def check_env():
    print("Running Health Check...")
    passed = True
    
    # Check Python version (3.8+)
    if sys.version_info < (3, 8):
        print(f"FAIL: Python version {sys.version} is not supported.")
        passed = False
    else:
        print(f"PASS: Python version {sys.version_info.major}.{sys.version_info.minor}")

    # Check directories
    required_dirs = [
        "data", "database", "etl", "src", "api", "frontend", "powerbi", 
        "notebooks", "tests", "docs", "scripts"
    ]
    for d in required_dirs:
        if not os.path.isdir(d):
            print(f"FAIL: Directory '{d}' is missing.")
            passed = False
        else:
            print(f"PASS: Directory '{d}' exists.")

    # Check files
    required_files = [
        ".gitignore", ".env.example", "requirements.txt", "README.md",
        "docs/01_project_overview/problem_statement.md",
        "docs/14_project_log/development_log.md"
    ]
    for f in required_files:
        if not os.path.isfile(f):
            print(f"FAIL: File '{f}' is missing.")
            passed = False
        else:
            print(f"PASS: File '{f}' exists.")

    if passed:
        print("\nSTATUS: PASS")
        sys.exit(0)
    else:
        print("\nSTATUS: FAIL")
        sys.exit(1)

if __name__ == "__main__":
    check_env()
