from setuptools import find_packages, setup

setup(
    name="markedrss",
    version="2.0.5",
    author="doppelmarker",
    author_email="doppelmarker@gmail.com",
    url="https://github.com/doppelmarker/Homework",
    description="Pure Python command-line RSS reader",
    long_description="Pure Python command-line RSS reader",
    python_requires=">=3.9",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests",
        "pydantic",
        "Jinja2",
    ],
    entry_points={
        "console_scripts": ["markedrss=rss_reader.__main__:main"],
    },
)
