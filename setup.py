from setuptools import setup, find_packages

setup(
    name="OpenFrpLib",
    version="1.0.0",
    author="LxHTT",
    author_email="lxhtz.dl@qq.com",
    description="Python Package for OpenFrp OPENAPI",
    python_requires='>=3.6',
    long_description="A Python Package to Use OpenFrp OPENAPI More Easily",
    long_description_content_type="text",
    url="https://github.com/LxHTT/OpenFrpLib",
    packages=find_packages(),
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
