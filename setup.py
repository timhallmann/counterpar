import setuptools

from counterpar import __version__

setuptools.setup(
    name="counterpar",
    description="counterpar finds paragraphs that are missing the counterpart of a symbol.",
    version=__version__,
    author="Tim Hallmann",
    author_email="tim@t8w.de",
    license="MIT",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/timhallmann/counterpar",
    packages=setuptools.find_packages(),
    python_requires='>=3.6'
)
