# -*- coding: UTF-8 -*-
# Copyright 2009-2016 Luc Saffre
#
# License: BSD (see file COPYING for details)

"""Database models for this plugin.

"""

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


from lino.api import dd, rt
from lino import mixins
from lino.modlib.gfks.mixins import Controllable
from lino.modlib.users.mixins import My, UserAuthored
# from lino.modlib.printing.mixins import PrintableType, TypedPrintable
from lino.mixins.periods import CombinedDateTime
from lino.core.requests import BaseRequest


@dd.python_2_unicode_compatible
class EntryType(mixins.BabelNamed):

    templates_group = 'blogs/Entry'

    class Meta:
        app_label = 'blogs'
        verbose_name = _("Blog Entry Type")
        verbose_name_plural = _("Blog Entry Types")

    #~ name = models.CharField(max_length=200)
    important = models.BooleanField(
        verbose_name=_("important"),
        default=False)
    remark = models.TextField(verbose_name=_("Remark"), blank=True)

    def __str__(self):
        return self.name


# def html_text(s):
#     return '<div class="htmlText">' + s + '</div>'


class EntryTypes(dd.Table):
    model = 'blogs.EntryType'
    # column_names = 'name build_method template *'
    order_by = ["name"]

    detail_layout = """
    id name
    # build_method template
    remark:60x5
    blogs.EntriesByType
    """


@dd.python_2_unicode_compatible
class Entry(UserAuthored, Controllable, CombinedDateTime):

    """A blog entry is a short article with a title, published on a given
    date and time by a given user.

    """
    class Meta:
        app_label = 'blogs'
        verbose_name = _("Blog Entry")
        verbose_name_plural = _("Blog Entries")

    title = models.CharField(_("Heading"), max_length=200, blank=True)
    body = dd.RichTextField(_("Body"), blank=True, format='html')

    pub_date = models.DateField(
        _("Publication date"), blank=True, null=True)
    pub_time = models.TimeField(
        _("Publication time"), blank=True, null=True)
    
    entry_type = dd.ForeignKey('blogs.EntryType', blank=True, null=True)
    
    language = dd.LanguageField()
    
    def __str__(self):
        return u'%s #%s' % (self._meta.verbose_name, self.pk)

    def on_create(self, ar):
        """
        Sets the :attr:`pub_date` and :attr:`pub_time` to now.

        """
        if not settings.SITE.loading_from_dump:
            self.set_datetime('pub', timezone.now())
            self.language = ar.get_user().language
        super(Entry, self).on_create(ar)

    # @classmethod
    # def latest_entries(cls, ar, max_num=10, **context):
    #     context = ar.get_printable_context(**context)
    #     qs = cls.objects.filter(pub_date__isnull=False)
    #     qs = qs.order_by("-pub_date")
    #     s = ''
    #     render = dd.plugins.jinja.render_jinja
    #     for num, e in enumerate(qs):
    #         if num >= max_num:
    #             break
    #         context.update(obj=e)
    #         s += render(ar, 'blogs/entry.html', context)
    #     return s
    

class Tagging(dd.Model):
    """A **tag** is the fact that a given entry mentions a given topic.

    """
    class Meta:
        app_label = 'blogs'
        verbose_name = _("Tagging")
        verbose_name_plural = _('Taggings')

    allow_cascaded_delete = ['entry', 'topic']

    topic = dd.ForeignKey(
        'topics.Topic',
        related_name='tags_by_topic')

    entry = dd.ForeignKey(
        'blogs.Entry',
        related_name='tags_by_entry')


class EntryDetail(dd.DetailLayout):
    main = """
    title entry_type:12 id 
    # summary
    pub_date pub_time user:10 language:10 owner
    body:60 TaggingsByEntry:20
    """


class Entries(dd.Table):
    required_roles = set()  # also for anonymous
    model = 'blogs.Entry'
    column_names = "id pub_date user entry_type title * body"
    order_by = ["id"]
    insert_layout = """
    title
    entry_type
    """
    detail_layout = EntryDetail()


class MyEntries(My, Entries):
    required_roles = dd.login_required()
    #~ master_key = 'user'
    column_names = "id pub_date entry_type title body *"
    # order_by = ["-modified"]

class AllEntries(Entries):
    required_roles = dd.login_required(dd.SiteStaff)

#~ class NotesByProject(Notes):
    #~ master_key = 'project'
    #~ column_names = "date subject user *"
    #~ order_by = "date"

#~ class NotesByController(Notes):
    #~ master_key = 'owner'
    #~ column_names = "date subject user *"
    #~ order_by = "date"


class EntriesByType(Entries):
    master_key = 'entry_type'
    column_names = "pub_date title user *"
    order_by = ["pub_date-"]
    #~ label = _("Notes by person")


class EntriesByController(Entries):
    master_key = 'owner'
    column_names = "pub_date title user *"
    order_by = ["pub_date-"]
    #~ label = _("Notes by person")


class LatestEntries(Entries):
    """Show the most recent blog entries."""
    label = _("Latest blog entries")
    column_names = "pub_date title user *"
    order_by = ["-pub_date"]
    filter = models.Q(pub_date__isnull=False)
    slave_grid_format = 'summary'

    @classmethod
    def get_slave_summary(cls, obj, ar, max_num=10, **context):
        
        context = ar.get_printable_context(**context)
        qs = rt.models.blogs.Entry.objects.filter(pub_date__isnull=False)
        qs = qs.order_by("-pub_date")
        s = ''
        render = dd.plugins.jinja.render_jinja
        for num, e in enumerate(qs):
            if num >= max_num:
                break
            context.update(obj=e)
            s += render(ar, 'blogs/entry.html', context)
        return s
    
    
class Taggings(dd.Table):
    model = 'blogs.Tagging'

class AllTaggings(Taggings):
    required_roles = dd.login_required(dd.SiteStaff)

class TaggingsByEntry(Taggings):
    master_key = 'entry'
    column_names = 'topic *'
    
class TaggingsByTopic(Taggings):
    master_key = 'topic'
    column_names = 'entry *'
    
    
