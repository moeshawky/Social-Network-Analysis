from setuptools import setup, find_packages

setup(
    name="network_intelligence",
    version="2.0.0",
    packages=find_packages(),
    install_requires=[
        "networkx>=3.0",
        "requests>=2.28",
        "numpy>=1.24",
        "matplotlib>=3.8",
        "python-louvain>=0.16",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "responses>=0.23",
        ]
    },
    entry_points={
        "console_scripts": [
            "network-intelligence=network_intelligence.__main__:main",
        ],
    },
    python_requires=">=3.9",
)
