from setuptools import setup, find_packages

setup(
    name='zgitignore',
    version='1.0.0',
    description='Check if a file is ignored by a .zgitignore file, compatible with .gitignore syntax',
    long_description=open('./README.rst').read(),
    url='https://github.com/zb3/zgitignore',
    author='zb3',
    author_email='sgv@o2.pl',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development',
    ],
    keywords='gitignore exclude pattern',
    py_modules=['zgitignore'],
    test_suite='test.test_zgitignore'
)
