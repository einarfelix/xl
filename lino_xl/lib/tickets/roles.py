# Copyright 2015-2017 Luc Saffre
# License: BSD (see file COPYING for details)
"""User roles for `lino_xl.lib.tickets`.

"""

from lino.core.roles import SiteUser

class TicketsUser(SiteUser):
    """A user who can create new tickets.

    """

class Searcher(TicketsUser):    
    """A user who can see all tickets.

    """


class Triager(Searcher):
    """A user who is responsible for triaging new tickets.

    """


class TicketsStaff(Triager):
    """Can configure tickets functionality.

    """

