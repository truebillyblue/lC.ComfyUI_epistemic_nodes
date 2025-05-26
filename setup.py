from setuptools import setup, find_packages

setup(
    name="lc_ComfyUI_epistemic_nodes",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "google-adk>=0.1.0",
        "lc_python_core @ git+https://github.com/truebillyblue/lC.pythonCore.git@main"
    ],
    python_requires='>=3.8',
)
