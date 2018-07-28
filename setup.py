import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="osmRoad",
    version="0.1",
    author="Zhongpu Chen",
    author_email="chenloveit@gmail.com",
    description="Parse OSM Data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ChenZhongPu/",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
