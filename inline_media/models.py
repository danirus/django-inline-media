#-*- coding: utf-8 -*-

import hashlib
import os
import os.path

from django.db import models
from django.db.models.signals import pre_delete
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core import urlresolvers
from django.utils.translation import ugettext_lazy as _

from sorl.thumbnail import get_thumbnail, ImageField
from sorl.thumbnail.default import Storage
from tagging.fields import TagField


storage = Storage()

#----------------------------------------------------------------------
# InlineType code borrowed from django-basic-apps by Nathan Borror
# https://github.com/nathanborror/django-basic-apps

class InlineType(models.Model):
    """InlineType model"""
    title           = models.CharField(max_length=200)
    content_type    = models.ForeignKey(ContentType)

    class Meta:
        db_table = 'inline_types'

    def __unicode__(self):
        return self.title


#----------------------------------------------------------------------
LICENSES = (('http://artlibre.org/licence/lal/en',
             'Free Art License'),
            ('http://creativecommons.org/licenses/by/2.0/',
             'CC Attribution'),
            ('http://creativecommons.org/licenses/by-nd/2.0/',
             'CC Attribution-NoDerivs'),
            ('http://creativecommons.org/licenses/by-nc-nd/2.0/',
             'CC Attribution-NonCommercial-NoDerivs'),
            ('http://creativecommons.org/licenses/by-nc/2.0/',
             'CC Attribution-NonCommercial'),
            ('http://creativecommons.org/licenses/by-nc-sa/2.0/',
             'CC Attribution-NonCommercial-ShareAlike'),
            ('http://creativecommons.org/licenses/by-sa/2.0/',
             'CC Attribution-ShareAlike'))

class License(models.Model):
    """Licenses under whose terms and conditions media is publicly accesible""" 

    name = models.CharField(max_length=255)
    link = models.URLField(unique=True)
    tags = TagField(help_text=_("family, comercial/non-commercial, etc."))

    class Meta:
        db_table = 'inline_media_licenses'

    def homepage(self):
        return '<a href="%s" target="_new">%s</a>' % tuple([self.link]*2)
    homepage.allow_tags = True

    def __unicode__(self):
        return self.name

#----------------------------------------------------------------------
# find_duplicates idea borrowed from django-filer by Stefan Foulis
# https://github.com/stefanfoulis/django-filer.git

class PictureManager(models.Manager):
    def find_duplicates(self, pic):
        return [ p for p in self.exclude(pk=pic.pk).filter(sha1=pic.sha1) ]
        

class Picture(models.Model):
    """Picture model"""

    title        = models.CharField(max_length=255)
    show_as_link = models.BooleanField(default=True)
    picture      = ImageField(upload_to="pictures/%Y/%b/%d", storage=storage)
    description  = models.TextField(blank=True)
    tags         = TagField()
    author       = models.CharField(blank=True, null=False, max_length=255,
                                    help_text=_("picture's author"))
    show_author  = models.BooleanField(default=False)
    license      = models.ForeignKey("License", blank=True, null=True)
    show_license = models.BooleanField(default=False)
    uploaded     = models.DateTimeField(auto_now_add=True)
    modified     = models.DateTimeField(auto_now=True)
    sha1         = models.CharField(max_length=40, blank=True, default="")

    objects      = PictureManager()

    class Meta:
        db_table = 'inline_media_pictures'

    def save(self, *args, **kwargs):
        try:
            sha = hashlib.sha1()
            self.picture.seek(0)
            sha.update(self.picture.read())
            self.sha1 = sha.hexdigest()
        except Exception, e:
            self.sha1 = ""
        super(Picture, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s' % self.title

    @property
    def url(self):
        return '%s%s' % (settings.MEDIA_URL, self.picture)

    # showing duplicates ala django-filer
    @property
    def duplicates(self):
        return Picture.objects.find_duplicates(self)

    def get_admin_url_path(self):
        return urlresolvers.reverse(
            'admin:%s_%s_change' % (self._meta.app_label,
                                    self._meta.module_name,),
            args=(self.pk,)
        )

    # used in admin 'list_display' to show the thumbnail of self.picture
    def thumbnail(self):
        try:
            im = get_thumbnail(self.picture, "x50")
        except Exception, e:
            return "unavailable"
        return '<div style="text-align:center"><img src="%s"></div>' % im.url
    thumbnail.allow_tags = True


def delete_picture(sender, instance, **kwargs):
    if sender == Picture:
        instance.picture.delete()
pre_delete.connect(delete_picture, sender=Picture)


class PictureSet(models.Model):
    """ PictureSet model """
    title       = models.CharField(max_length=255)
    slug        = models.SlugField()
    description = models.TextField(blank=True)
    tags        = TagField()
    cover       = models.ForeignKey("Picture", blank=True, null=True)
    pictures    = models.ManyToManyField("Picture", related_name="picture_sets")
    order       = models.CommaSeparatedIntegerField(blank=True, max_length=512, help_text=_("Establish the pictures order by typing the comma separated list of their picture IDs."))
    created     = models.DateTimeField(auto_now_add=True)
    modified    = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "inline_media_picture_sets"
  
    def __unicode__(self):
        return "%s" % self.title

    # used in admin 'list_display' to show the thumbnail of self.picture
    def cover_thumbnail(self):
        im = get_thumbnail(self.cover.picture, "x50")
        return '<div style="text-align:center"><img src="%s"></div>' % im.url
    cover_thumbnail.allow_tags = True

    # used in admin 'list_display' to show the list of pictures' titles
    def picture_titles_as_ul(self):
        titles = []
        for picture in self.pictures_in_order():
            if picture == self.cover:
                titles.append("<li>%s (cover)</li>" % picture.title)
            else:
                titles.append("<li>%s</li>" % picture.title)
        return '<ul>%s</ul>' % "".join(titles)
    picture_titles_as_ul.allow_tags = True

    def pictures_in_order(self):
        pictures = self.pictures.all()
        pic_ids = [ pic.id for pic in pictures ]
        ordered = []

        try:
            sorted_ids = [ int(id) for id in self.order.split(",") ]
        except ValueError:
            return pictures
        else:
            for id in sorted_ids:
                try:
                    ordered.append(pictures[pic_ids.index(id)])
                except:
                    pass
            return ordered

