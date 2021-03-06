# -*- coding: UTF-8 -*-
# Copyright 2008-2017 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from builtins import str
from django.conf import settings

from lino.api import dd, rt, _
from etgen.html import E

# from lino.modlib.notify.mixins import ChangeNotifier
# from lino_xl.lib.contacts.mixins import ContactRelated
from lino_xl.lib.clients.mixins import ClientBase

from .utils import only_active_coachings_filter


class Coachable(ClientBase):

    class Meta:
        abstract = True

    def get_coachings(self, period=None, *args, **flt):
        qs = self.coachings_by_client.filter(*args, **flt)
        if period is not None:
            qs = qs.filter(only_active_coachings_filter(period))
        return qs

    def get_primary_coaching(self):
        # qs = self.coachings_by_client.filter(primary=True).distinct()
        # 20170303 : wondering why i added distinct() here...
        qs = self.coachings_by_client.filter(primary=True)
        # logger.info("20140725 qs is %s", qs)
        if qs.count() == 1:
            return qs[0]
        
    def get_primary_coach(self):
        obj = self.get_primary_coaching()
        if obj is not None:
            return obj.user

    def setup_auto_event(self, evt):
        d = evt.start_date
        coachings = self.get_coachings(
            (d, d), type__does_integ=True, user=evt.user)
        if not coachings.exists():
            coachings = self.get_coachings((d, d), type__does_integ=True)
            if coachings.count() == 1:
                evt.user = coachings[0].user

    @dd.displayfield(_('Primary coach'))
    def primary_coach(self, ar=None):
        if ar is None:
            return ''
        pc = self.get_primary_coach()
        if pc is None:
            return ''
        return ar.obj2html(pc)

    # primary_coach = property(get_primary_coach)

    @dd.displayfield(_("Coaches"))
    def coaches(self, ar):
        today = dd.today()
        period = (today, today)
        items = [str(obj.user) for obj in self.get_coachings(period)]
        return ', '.join(items)

    # def get_notify_message_type(self):
    #     return rt.models.notify.MessageTypes.coachings
    
    def get_change_observers(self, ar=None):
        # implements lino.modlib.notify.mixins.ChangeNotifier
        for x in super(Coachable, self).get_change_observers(ar):
            yield x
        for u in settings.SITE.user_model.objects.filter(
                coaching_supervisor=True):
            yield (u, u.mail_mode)
        today = dd.today()
        period = (today, today)
        for obj in self.get_coachings(period):
            if obj.user_id:
                yield (obj.user, obj.user.mail_mode)


    @dd.displayfield(_("Find appointment"))
    def find_appointment(self, ar):
        if ar is None:
            return ''
        CalendarPanel = rt.models.extensible.CalendarPanel
        elems = []
        for obj in self.coachings_by_client.all():
            sar = CalendarPanel.request(
                subst_user=obj.user, current_project=self.pk)
            elems += [ar.href_to_request(sar, obj.user.username), ' ']
        return E.div(*elems)


