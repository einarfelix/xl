# -*- coding: UTF-8 -*-
# Copyright 2011-2017 Luc Saffre
# License: BSD (see file COPYING for details)
"""Database models for this plugin.



"""

from __future__ import unicode_literals

from django.db import models

from lino.api import dd, rt, _

from lino.mixins import Sequenced

from lino_xl.lib.excerpts.mixins import Certifiable


@dd.python_2_unicode_compatible
class Milestone(Certifiable):  # mixins.Referrable):
    """A **Milestone** is a named step of evolution on a given Site.  For
    software projects we usually call them a "release" and they are
    named by a version number.

    .. attribute:: closed

       Closed milestones are hidden in most lists.

    """
    class Meta:
        app_label = 'deploy'
        verbose_name = _("Milestone")
        verbose_name_plural = _('Milestones')

    project = dd.ForeignKey(
        'tickets.Project',
        related_name='milestones_by_project', blank=True, null=True)
    site = dd.ForeignKey(
        'tickets.Site',
        related_name='milestones_by_site', blank=True, null=True)
    label = models.CharField(_("Label"), max_length=20, blank=True)
    expected = models.DateField(_("Expected for"), blank=True, null=True)
    reached = models.DateField(_("Reached"), blank=True, null=True)
    description = dd.RichTextField(_("Description"), blank=True)
    changes_since = models.DateField(
        _("Changes since"), blank=True, null=True,
        help_text=_("In printed document include a list of "
                    "other changes since this date"))
    closed = models.BooleanField(_("Closed"), default=False)

    #~ def __unicode__(self):
        #~ return self.label

    def __str__(self):
        label = self.label
        if not label:
            if self.reached:
                label = self.reached.isoformat()
            else:
                label = "#{0}".format(self.id)
        return "{0}@{1}".format(label, self.project or self.site)



@dd.python_2_unicode_compatible
class Deployment(Sequenced):
    """A **wish** (formerly deployment) is the fact that a given ticket is
    being fixed (or installed or activated) by a given milestone (to a
    given site).

    .. attribute:: milestone

       The milestone (and site) of this deployment.

    """
    class Meta:
        app_label = 'deploy'
        verbose_name = _("Wish")
        verbose_name_plural = _('Wishes')

    ticket = dd.ForeignKey(
        'tickets.Ticket', related_name="deployments_by_ticket")
    milestone = dd.ForeignKey('deploy.Milestone')
    remark = dd.RichTextField(_("Remark"), blank=True, format="plain")
    # remark = models.CharField(_("Remark"), blank=True, max_length=250)

    def get_siblings(self):
        "Overrides :meth:`lino.mixins.Sequenced.get_siblings`"
        qs = self.__class__.objects.filter(
                milestone=self.milestone).order_by('seqno')
        # print(20170321, qs)
        return qs
    
    @dd.chooser()
    def milestone_choices(cls, ticket):
        # if not ticket:
        #     return []
        # if ticket.site:
        #     return ticket.site.milestones_by_site.all()
        return rt.models.deploy.Milestone.objects.order_by('label')

    def __str__(self):
        return "{}@{}".format(self.seqno, self.milestone)

    @classmethod
    def quick_search_filter(cls, search_text, prefix=''):
        """Overrides the default behaviour defined in
        :meth:`lino.core.model.Model.quick_search_filter`. For
        Deployment objects, when quick-searching for a text containing
        only digits, the user usually means the :attr:`label` and *not*
        the primary key.

        """
        if search_text.isdigit():
            return models.Q(**{prefix+'label__contains': search_text})
        return super(Deployment, cls).quick_search_filter(search_text, prefix)

    


from lino.modlib.system.choicelists import (ObservedEvent)
from lino_xl.lib.tickets.choicelists import TicketEvents, T24, combine


class TicketEventToDo(ObservedEvent):
    text = _("To do")

    def add_filter(self, qs, pv):
        if pv.start_date:
            pass
        if pv.end_date:
            qs = qs.exclude(
                deployment__milestone__reached__lte=combine(
                    pv.end_date, T24))
        return qs


TicketEvents.add_item_instance(TicketEventToDo('todo'))


    
