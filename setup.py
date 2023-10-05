from setuptools import setup

with open('requirements.txt', encoding='utf-8') as requs:
    requirements_list = [requ.strip('\n \r') for requ in requs.readlines()]

setup(
    name="tttg_utils",
    version="0.1",
    description="Utilities for various projects",
    url="https://github.com/TomTomToGo-Github/tttg_utils",
    author="Thomas Haid",
    author_email="thomas@gmx.net",
    install_requires=requirements_list,
    license="MIT",
    packages=[
        "tttg_utils",
        "tttg_utils.connectors",
    ],
    # zip_safe=False
)
