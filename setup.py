import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="psd2",
    version="0.0.4",
    author="Marcos Duarte",
    author_email="duartexyz@gmail.com",
    description="Estimate power spectral density characteristics using Welch's method",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/demotu/psd2",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
