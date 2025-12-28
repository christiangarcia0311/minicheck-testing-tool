from setuptools import setup, find_packages

setup(
    name='minicheck',
    version='0.1.0',
    author='Christian Garcia',
    author_email='',
    description='A minimal python testing tool that makes writing, organizing and executing tests fast and straightforward, keeping development workflows simple and clear.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=[
        'colorama'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
