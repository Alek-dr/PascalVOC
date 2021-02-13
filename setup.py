import setuptools

with open('requirements.txt') as f:
    install_requires = f.read()

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="pascal_voc",
    version="0.0.1",
    author="Alexander Barmin",
    author_email="barmin1@mail.ru",
    description="Working with PascalVOC annotations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
