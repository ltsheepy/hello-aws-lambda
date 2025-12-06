#!/usr/bin/env python3
"""
Setup script for Terraform AWS Documentation Toolkit
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme = Path(__file__).parent / "README.md"
long_description = readme.read_text() if readme.exists() else ""

setup(
    name="terraform-docs-toolkit",
    version="1.0.0",
    description="Automatically generate comprehensive documentation for Terraform AWS infrastructure",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/YOUR_USERNAME/terraform-docs-toolkit",
    packages=find_packages(),
    install_requires=[
        "diagrams>=0.23.4",
        "graphviz>=0.20.1",
        "boto3>=1.28.0",
        "pyyaml>=6.0",
    ],
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "terraform-docs=bin.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Documentation",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="terraform aws documentation diagrams security compliance",
)
