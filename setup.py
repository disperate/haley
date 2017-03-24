import setuptools

setuptools.setup(
    name="haley",
    version="0.1.0",
    url="https://github.com/disperate/haley",

    author="Julian Bigler",
    author_email="julian.bigler@stud.hslu.ch",

    description="Software for autonomous vehicle build during PREN",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=[],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
