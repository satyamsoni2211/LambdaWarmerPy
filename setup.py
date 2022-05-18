from setuptools import setup

with open("README.md") as fr:
    long_description = fr.read()
setup(
    name="py_lambda_warmer",
    version="0.1.3",
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
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9"
    ]
)
