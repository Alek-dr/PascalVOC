import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="pascal_voc",
    version="2.0.1",
    author="Alexander Barmin",
    author_email="barmin1@mail.ru",
    description="Tool to work with annotation formats",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=["tests"]),
    install_requires=["lxml>=4.6.2", "Pillow>=8.1.0", "xmlobj"],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
