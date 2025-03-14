import subprocess
from typing import List


def compile_run_dbt(compile_command: List[str], run_command: List[str]):

    try:
        result = subprocess.run(
            compile_command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd="healthy_blue/",
        )
        print("dbt compile successful:")
        print(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print("Error occurred during dbt compile:")
        print(e.stderr.decode())

    try:
        result = subprocess.run(
            run_command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd="healthy_blue/",
        )
        print("dbt run successful:")
        print(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print("Error occurred during dbt run:")
        print(e.stderr.decode())
