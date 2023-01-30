import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="capparser",
    version="1.0.4",
    author="David Araújo",
    author_email="david2araujo5@gmail.com",
    description="Common Alerting Protocol (CAP) parser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=["capparser"],
    package_dir={'': '.'},
)