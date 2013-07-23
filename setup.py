# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""setup.py: create executable"""

from distutils.core import setup
import sys
import py2exe


sys.argv.append('py2exe')

setup(
    options= {'py2exe': {'bundle_files': 1, 'compressed': True}},
    windows = [{'script': '__main__.py'}],
    zipfile = None,
)