from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="trashbin",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "trash=trashbin.cli:main",
        ],
    },
    author="Lord J. Hackwell",
    author_email="lordhck@niton.dev",
    description="Trashbin is a utility designed for safer file and directory removal.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://niton.dev/trash",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.8",
    install_requires=[
        "rich==13.7.1",
    ],
    license="MIT",
)
