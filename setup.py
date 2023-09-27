from setuptools import setup, find_packages

setup(
    name='ade_enseirb',
    version='0.1.0',
    author='Arthur Le Floch',
    author_email='alf.github@gmail.com',
    description='ADE API for ENSEIRB-MATMECA students',
    long_description='ADE API for ENSEIRB-MATMECA students',
    url='https://github.com/ArthurLeFloch/ADE-ENSEIRB',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
