from setuptools import setup, find_packages
setup(
    name="producer",
    version="0.0.2",
    author = "olena babenko",
    author_email = "to.helen.babenko@gmail.com",
    description = ("This is hometast project"),
    python_requires='>=3.7.0',
    url = "https://www.python.org/doc/",
    license='MIT',
    packages=find_packages(exclude=["docs", "examples", "dist"]),
    entry_points={
        "console_scripts": [
            "runproducer = producer.__main__:main"
        ]
    }
)