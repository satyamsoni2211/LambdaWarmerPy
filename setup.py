from setuptools import setup

with open("README.md") as fr:
    long_description = fr.read()
setup(
    name="py_lambda_warmer",
    version="0.1.6",
    description="Warmer Utility for Lambda Function",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="satyam soni",
    author_email="satyamsoni@hotmail.co.uk",
    py_modules=["warmer", ],
    url="https://github.com/satyamsoni2211/LambdaWarmerPy.git",
    keywords="lambda cold start warming performance",
    license="mit",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "License :: Freeware",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Utilities"
    ],
    extras_require={
        "dev": [
            "pytest",
            "tox"
        ]
    }
)
