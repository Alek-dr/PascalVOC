import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="pascal_voc",
    version="0.0.3",
    author="Alexander Barmin",
    author_email="barmin1@mail.ru",
    description="Working with PascalVOC annotations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=["lxml>=4.6.2",
                      "Pillow>=8.1.0"],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
