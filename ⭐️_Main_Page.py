from importlib.metadata import distribution
import eptr2
import os
import importlib.util
import runpy
import streamlit as st
import shutil


st.write("Running main.py after sourcing app.py")

script_path = distribution("eptr2").locate_file(
    "eptr2/tutorials/composite/⭐️_Main_Page.py"
)

pages_path = os.path.dirname(script_path) + "/pages"

if os.path.exists(pages_path):
    shutil.copytree(pages_path, "pages", dirs_exist_ok=True)
else:
    st.warning(f"Source pages directory not found: {pages_path}")

# globals()["__name__"] = "__main__"
# with open(script_path, "r") as file:
#     exec(file.read(), globals())

runpy.run_path(script_path, run_name="__main__")
# Your other Streamlit code in main.py
print("End")
