import subprocess
from typing import List
import streamlit as st


def run_dbt(run_command: List[str], dbt_project_name: str):
    try:
        result = subprocess.run(
            run_command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=f"{dbt_project_name}/",
        )
        print("dbt run successful:")
        print(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print("Error occurred during dbt run:")
        print(e.stderr.decode())


def load_css(file_name: str):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)