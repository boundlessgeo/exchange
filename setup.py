# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2016 Boundless Spatial
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################
import os
from setuptools import setup, find_packages
from sphinx.setup_command import BuildDoc

os.environ['SPHINX_BUILD'] = 'exchange/static/docs'

cmdclass = {'build_sphinx': BuildDoc}
version = __import__('exchange').semantic_version()


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


setup(
    name="geonode-exchange",
    version=version,
    cmdclass=cmdclass,
    author="Boundless Spatial",
    author_email="contact@boundlessgeo.com",
    description="Exchange, a platform for geospatial collaboration",
    long_description=(read('README.rst')),
    command_options={
        'build_sphinx': {
            'project': ('setup.py', 'exchange'),
            'version': ('setup.py', version),
            'release': ('setup.py', version),
        }},
    classifiers=[
        'Intended Audience :: System Administrators',
        'Environment :: Web Environment',
        'License :: OSI Approved :: GNU General Public License v3 or later '
        '(GPLv3+)',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Framework :: Django :: 1.8',
    ],
    license="GPLv3+",
    keywords="exchange geonode django",
    url='https://github.com/boundlessgeo/exchange',
    packages=find_packages('.'),
    include_package_data=True,
    zip_safe=False
)
