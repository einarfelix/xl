# -*- coding: UTF-8 -*-
# Copyright 2011-2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""Desktop UI for this plugin.
"""

from __future__ import unicode_literals

from lino import mixins
from lino.api import dd, rt, _



class Milestones(dd.Table):
    """
    .. attribute:: show_closed
    """
    order_by = ['-id']
    # order_by = ['label', '-id']
    model = 'deploy.Milestone'
    detail_layout = """
    site id label expected reached changes_since printed closed
    description
    #TicketsFixed
    tickets.TicketsReported DeploymentsByMilestone
    #clocking.OtherTicketsByMilestone
    """
    insert_layout = dd.InsertLayout("""
    site label
    description
    """, window_size=(50, 15))

    parameters = mixins.ObservedPeriod(
        show_closed=dd.YesNo.field(
            blank=True, default=dd.YesNo.no.as_callable,
            help_text=_("Show milestons which are closed.")))

    params_layout = "start_date end_date show_closed"

    @classmethod
    def get_request_queryset(self, ar):
        qs = super(Milestones, self).get_request_queryset(ar)
        pv = ar.param_values
        if pv.show_closed == dd.YesNo.no:
            qs = qs.filter(closed=False)
        elif pv.show_closed == dd.YesNo.yes:
            qs = qs.filter(closed=True)
        return qs


class MilestonesBySite(Milestones):
    order_by = ['-label', '-id']
    master_key = 'site'
    column_names = "label expected reached closed id *"


class Deployments(dd.Table):
    model = 'deploy.Deployment'
    parameters = mixins.ObservedPeriod(
        show_closed=dd.YesNo.field(
            blank=True, default=dd.YesNo.no.as_callable,
            help_text=_("Show deployments on closed milestones.")))

    params_layout = "start_date end_date show_closed"

    @classmethod
    def get_request_queryset(self, ar):
        qs = super(Deployments, self).get_request_queryset(ar)
        pv = ar.param_values
        if pv.show_closed == dd.YesNo.no:
            qs = qs.filter(milestone__closed=False)
        elif pv.show_closed == dd.YesNo.yes:
            qs = qs.filter(milestone__closed=True)
        return qs


class DeploymentsByMilestone(Deployments):
    label = _("Deployed tickets")
    order_by = ['-ticket__id']
    master_key = 'milestone'
    column_names = "ticket:30 ticket__state:10 remark:30 *"


class DeploymentsByTicket(Deployments):
    order_by = ['-milestone__reached']
    master_key = 'ticket'
    # column_names = "milestone__reached milestone  remark *"
    column_names = "milestone remark *"
