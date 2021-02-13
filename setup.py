import setuptools

setuptools.setup(
    name="pascal_voc",
    version="0.0.1",
    author="Alexander Barmin",
    author_email="barmin1@mail.ru",
    description="Working with PascalVOC annotations",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
