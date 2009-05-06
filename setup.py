from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='ooo2tools.daemon',
        version=version,
        description="a daemon processing macros using ooo2tools.core",
        long_description="""\
        scan a specified directory. This daemon expects to find tasks created in a define way by some program. tasks contain documents and sequences of instructions as defined in ooo2tools.core""",
        classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        keywords='open office daemon',
        author='Alexandre LE GROS',
        author_email='alexandre_lg@hotmail.fr',
        url='',
        license='',
        extras_require={'test': ['IPython', 'zope.testing', 'mocker']},
        packages=find_packages(exclude=['ez_setup',]),
        packages=find_packages('src'),
        package_dir = {'': 'src'},
        namespace_packages=['ooo2tools'],
        include_package_data=True,
        zip_safe=False,
        install_requires=[
        'ooo2tools.core',
        ],
        entry_points="""
        # -*- Entry points: -*-
        """,
        )
# vim:set et sts=4 ts=4 tw=80:

