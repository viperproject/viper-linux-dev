#!/usr/bin/python3


from scripts.utils import License


LICENSES = {
    'APACHE': License(
        'Apache-2.0',
        'The Apache Software License, Version 2.0',
        'http://www.apache.org/licenses/LICENSE-2.0.txt',
        ),
    'BSD-scala': License(
        'Scala',
        'Scala',
        'http://www.scala-lang.org/license.html'
        ),
    'BSD3': License(
        'BSD',
        'BSD 3-clause',
        'http://opensource.org/licenses/BSD-3-Clause'
        ),
    'BSD': License(
        'BSD',
        'The BSD License',
        'http://www.opensource.org/licenses/bsd-license.php'
        ),
    'LGPL2.1': License(
        'LGPL-2.1',
        'GNU Lesser General Public License Version 2.1, February 1999',
        'http://jgrapht.sourceforge.net/LGPL.html'
        ),
    'LGPL3.0': License(
        'LGPL-3.0',
        'LGPL 3.0 license',
        'http://www.opensource.org/licenses/lgpl-3.0.html'
        ),
    'MIT': License(
        'MIT',
        'MIT',
        'http://opensource.org/licenses/MIT'
        ),
    'MPL': License(
        'MPL-2.0',
        'Mozilla Public License Version 2.0',
        'http://www.mozilla.org/MPL/2.0/'
        ),
    'Ms-PL': License(
        'MS-PL',
        'Microsoft Public License',
        'http://opensource.org/licenses/ms-pl'
        )
    }
