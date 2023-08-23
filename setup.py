import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="pascal_voc",
    version="2.1.0",
    author="Alexander Barmin",
    author_email="barmin1@mail.ru",
    description="Tool to work with annotation formats",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(
        include=["pascal"],
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"],
    ),
    data_files=[("pascal", ["pascal/fonts/arialmt.ttf"])],
    install_requires=[
        "Pillow>=8.1.0",
        "transliterate>=1.10.2",
        "xmlobj==1.2.0",
        "typing_extensions==4.7.1",
    ],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
