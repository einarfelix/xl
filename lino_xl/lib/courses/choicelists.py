# -*- coding: UTF-8 -*-
# Copyright 2012-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)


from __future__ import unicode_literals
from __future__ import print_function

"""
Choicelists for this plugin.

"""

import logging
logger = logging.getLogger(__name__)

from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino.api import dd

class CourseState(dd.State):
    is_active = True
    is_editable = True
    is_invoiceable = True
    auto_update_calendar = False

class CourseStates(dd.Workflow):
    item_class = CourseState
    required_roles = dd.login_required(dd.SiteAdmin)
    is_exposed = models.BooleanField(_("Exposed"), default=True)
    is_invoiceable = models.BooleanField(_("Invoiceable"), default=True)
    is_editable = models.BooleanField(_("Editable"), default=True)
    auto_update_calendar = models.BooleanField(
        _("Update calendar"), default=False)
    column_names = "value name text is_exposed is_editable is_invoiceable auto_update_calendar"

add = CourseStates.add_item
add('10', _("Draft"), 'draft',
    is_editable=True, is_invoiceable=False, is_exposed=True)
add('20', _("Started"), 'active',
    is_editable=False, is_invoiceable=True, is_exposed=True)
add('30', _("Inactive"), 'inactive',
    is_editable=False, is_invoiceable=False, is_exposed=False)
add('40', _("Closed"), 'closed',
    is_editable=False, is_invoiceable=False, is_exposed=False)



class EnrolmentStates(dd.Workflow):
    """The list of possible states of an enrolment.

    The default implementation has the following values:
    
    .. attribute:: requested
    .. attribute:: confirmed
    .. attribute:: cancelled

        The enrolment was cancelled before it even started.

    .. attribute:: ended

        The enrolment was was successfully ended.

    .. attribute:: abandoned

        The enrolment was abandoned.

    """
    verbose_name_plural = _("Enrolment states")
    required_roles = dd.login_required(dd.SiteAdmin)
    invoiceable = models.BooleanField(_("invoiceable"), default=True)
    uses_a_place = models.BooleanField(_("Uses a place"), default=True)

add = EnrolmentStates.add_item
add('10', _("Requested"), 'requested', invoiceable=False, uses_a_place=False)
add('11', _("Trying"), 'trying', invoiceable=False, uses_a_place=True)
add('20', _("Confirmed"), 'confirmed', invoiceable=True, uses_a_place=True)
add('30', _("Cancelled"), 'cancelled', invoiceable=False, uses_a_place=False)
# add('40', _("Certified"), 'certified', invoiceable=True, uses_a_place=True)
# add('40', _("Started"), 'started')
# add('50', _("Ended"), 'ended', invoiceable=True, uses_a_place=False)
# add('60', _("Award"),'award')
# add('90', _("Abandoned"), 'abandoned', invoiceable=False, uses_a_place=False)


class CourseArea(dd.Choice):

    # force_guest_states = False
    courses_table = 'courses.Courses'
    
    def __init__(
            self, value, text, name,
            courses_table='courses.Courses', **kwargs):
        self.courses_table = courses_table
        super(CourseArea, self).__init__(value, text, name, **kwargs)


class CourseAreas(dd.ChoiceList):
    preferred_width = 10
    # verbose_name = _("Course area")
    # verbose_name_plural = _("Course areas")
    verbose_name = _("Layout")
    verbose_name_plural = _("Course layouts")
    item_class = CourseArea
    column_names = "value name text courses_table #force_guest_states"
    required_roles = dd.login_required(dd.SiteAdmin)
    
    # @dd.virtualfield(models.BooleanField(_("Force guest states")))
    # def force_guest_states(cls, choice, ar):
    #     return choice.force_guest_states

    @dd.virtualfield(models.CharField(_("Table")))
    def courses_table(cls, choice, ar):
        return str(choice.courses_table)


add = CourseAreas.add_item
try:
    add('C', dd.plugins.courses.verbose_name, 'default')
except AttributeError:
    add('C', 'oops, courses not installed', 'default')
# add('J', _("Journeys"), 'journeys')


