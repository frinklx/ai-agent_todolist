from setuptools import setup, find_packages

setup(
    name="taskagent",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click>=8.1.7",
        "rich>=13.7.0",
        "nltk>=3.8.1",
        "python-dateutil>=2.8.2",
        "parsedatetime>=2.6",
        "tabulate>=0.9.0",
        "colorama>=0.4.6",
    ],
    entry_points={
        "console_scripts": [
            "taskagent=taskagent.cli:cli",
        ],
    },
) 