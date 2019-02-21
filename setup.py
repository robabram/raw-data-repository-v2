import os
from distutils.core import setup

from setuptools import find_packages

__VERSION__ = "0.1"


def find_package_data_files(dirs):
    paths = []
    for directory in dirs:
        for (path, directories, filenames) in os.walk(directory):
            for filename in filenames:
                paths.append(os.path.join('..', path, filename))
    return paths


def setup_package():
    # Recursively gather all non-python module directories to be included in packaging.
    core_files = find_package_data_files([
        'rdr_server/static',
        'rdr_server/templates',
    ])

    setup(
        name='Raw-Data-Repository-Api',
        version=__VERSION__,
        description='The RDR Api',
        author='VUMC-DRC',
        author_email='robert.m.abram@vumc.com',
        url='https://github.com/all-of-us/raw-data-repository',
        download_url='https://github.com/all-of-us/raw-data-repository/tarball/' + __VERSION__,
        packages=find_packages(exclude=['tests']),
        package_data={
            'rdr_server': core_files,
        },
        keywords=['raw-data-repository', 'api'],  # arbitrary keywords
        classifiers=[
            'Development Status :: 4 - Beta',
            'Programming Language :: Python',
            'Environment :: Web',
            'License :: BSD',
            'Operating System :: POSIX :: Linux',
        ],

        # Do not add additional requirements here, add them to requirements.in.
        install_requires=[],

        entry_points={
            'console_scripts': [
                # Services
                # 'rdr-db-daemon = rdr_server.utilities.services.rdr_daemon:run',
            ],
        },

        tests_require=[
            'pytest',
            'pytest-runner',
            'pytest-pythonpath',
        ],
    )


if __name__ == "__main__":
    setup_package()
