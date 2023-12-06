from setuptools import setup, find_packages
from typing import List

def get_requirments(file_path:str)->List[str]:
    """
    This function will return the list of requirments
    """
    requirments = []
    with open(file_path) as file_obj:
        requirments = file_obj.readlines()
        requirments = [req.replace("\n","") for req in requirments] # loop over the requirments and remove \
        if "-e ." in requirments:
            requirments.remove("-e .")


setup(
    name="airpollution_model",
    version="0.0.1",
    author="Behzad Valipour Sh.",
    author_email="behzad.valipour@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.9",
    ],
    packages=find_packages(),
    install_requires=get_requirments("requirments.txt")
)