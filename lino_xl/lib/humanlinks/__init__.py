# Copyright 2014-2015 Luc Saffre
#
# This file is part of Lino XL.
#
# Lino XL is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Lino XL is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with Lino XL.  If not, see
# <http://www.gnu.org/licenses/>.

"""Defines "parency links" between two "persons", and a user interface
to manage them.

This module is probably useful in combination with
:mod:`lino_xl.lib.households`.

.. autosummary::
   :toctree:

    choicelists
    models

"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    "Extends :class:`lino.core.plugin.Plugin`."
    verbose_name = _("Parency links")

    ## settings
    person_model = 'contacts.Person'
    """
    A string referring to the model which represents a human in your
    application.  Default value is ``'contacts.Person'`` (referring to
    :class:`lino_xl.lib.contacts.Person`).
    """

    def setup_explorer_menu(config, site, profile, m):
        p = site.plugins.contacts
        m = m.add_menu(p.app_label, p.verbose_name)
        m.add_action('humanlinks.Links')
        m.add_action('humanlinks.LinkTypes')


