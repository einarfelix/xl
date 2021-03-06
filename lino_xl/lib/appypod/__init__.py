# Copyright 2014-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""
Adds functionality for generating printable documents using
LibreOffice and the `appy.pod <http://appyframework.org/pod.html>`__
package.

See also :ref:`lino.admin.appypod` and :doc:`/specs/appypod`.
"""

import six
from lino.api import ad, _


class Plugin(ad.Plugin):
    verbose_name = _("Appy POD")

    def get_requirements(self, site):
        yield "odfpy"
        try:
            import appy
            # leave unchanged if it is already installed
        except ImportError:
            if six.PY3:
                yield "-e svn+https://svn.forge.pallavi.be/appy-dev/dev1#egg=appy"
            else:
                yield "appy"

    def get_used_libs(self, html=None):
        try:
            # ~ import appy
            from appy import version
            version = version.verbose
        except ImportError:
            version = self.site.not_found_msg
        yield ("Appy", version, "http://appyframework.org/pod.html")
