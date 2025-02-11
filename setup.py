from setuptools import setup, find_packages

setup(
    name="SocketPy",
    version="0.1.0",
    author="Andrew Hernandez",
    author_email="andromedeyz@hotmail.com",
    description="A lightweight Python library for streamlined network programming, making it easier to build servers and functional clients.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="http://localhost:3000/pi/SocketPy",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: System :: Networking",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Networking :: Monitoring",
        "Natural Language :: English"
    ],
    python_requires=">=3.9",
)