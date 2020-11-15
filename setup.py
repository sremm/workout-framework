import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="workout-framweork",  # Replace with your own username
    version="0.0.1",
    author="Sten Remmelg",
    author_email="sten.remmelg@gmail.com",
    description="Tools to help analys and plan workout data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sremm/workout-framework",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)