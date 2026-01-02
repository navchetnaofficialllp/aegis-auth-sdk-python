from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="aegis-auth-navchetna",
    version="1.0.2",
    author="Navchetna Technologies",
    author_email="hello@navchetna.tech",
    description="Aegis Auth is a unified identity management system providing memory-safe Rust-based authentication. Consolidation of disparate identity providers into a single canonical source.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/navchetnaofficialllp/aegis-auth-sdk-python",
    project_urls={
        "Bug Tracker": "https://github.com/navchetnaofficialllp/aegis-auth-sdk-python/issues",
        "Documentation": "https://aegis.navchetna.tech",
        "Source Code": "https://github.com/navchetnaofficialllp/aegis-auth-sdk-python",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Session",
        "Topic :: Security",
        "Topic :: System :: Systems Administration :: Authentication/Directory",
    ],
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
    },
    keywords=[
        "authentication",
        "auth",
        "webauthn",
        "mfa",
        "jwt",
        "aegis",
        "sdk",
        "security",
        "rust",
        "identity",
        "decentralized",
        "navchetna",
    ],
    license="MIT",
)