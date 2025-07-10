"""
The setup.py file is an essential part of packaging and 
distributing Python projects. It is used by setuptools 
(or distutils in older Python versions) to define the configuration 
of your project, such as its metadata, dependencies, and more

"""
from setuptools import find_namespace_packages, setup,find_packages
from  typing import List

def get_requirements()->List[str]:
    """
    THis function will return list of requiremnts

    """
    requirement_lst : List[str] = []
    try: 
        with open("requirements.txt","r") as file:
            #Read lines from the files
            lines = file.readlines()
            for line in lines: ##processing each line
                requirement = line.strip()
                #ignoring empty lines
                if requirement and requirement != '-e .':
                   requirement_lst.append(requirement)
    except FileNotFoundError:
        print("requirements.txt not found")

    return requirement_lst
print(get_requirements())

setup(
    name = "NetworkSecurity",
    version = "0.0.1",
    description = "This is a Netowork Security Project",
    author = "DIVYANSH",
    packages= find_packages(),
    install_requires = get_requirements()

)


