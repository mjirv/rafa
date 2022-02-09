from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'A data transformation tool for analytics teams'
LONG_DESCRIPTION = 'Rafa lets you write templated SQL via Python and run it against your data warehouse to create tables for analytics.'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="rafa", 
    version=VERSION,
    author="Michael Irvine",
    author_email="michael.j.irvine@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["db.py"], # add any additional packages that 
    # needs to be installed along with your package. Eg: 'caer'
    
    keywords=['python', 'first package'],
    classifiers= [
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux"
    ]
)
