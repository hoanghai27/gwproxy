import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gwproxy",
    version="0.0.1",
    author="Mike",
    author_email="mike@gskynet.vn",
    description="Gateway proxy for Python 3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/hoanghai27/gwproxy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
