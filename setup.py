from setuptools import setup, find_packages

setup(
    name='hatespeech',
    version='0.0',
    keywords='hate speech',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(),

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        'numpy',
        'pandas',
        'scipy'
    ]
)
