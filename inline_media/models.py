from __future__ import unicode_literals

import hashlib

from django.db import models
from django.db.models.signals import pre_delete
from django.core import urlresolvers
from django.core.validators import validate_comma_separated_integer_list
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from sorl.thumbnail import get_thumbnail, ImageField
from sorl.thumbnail.default import Storage
from taggit.managers import TaggableManager

from inline_media.conf import settings


storage = Storage()


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


@python_2_unicode_compatible
class License(models.Model):
    """Licenses under whose terms and conditions media is publicly accesible"""

    name = models.CharField(max_length=255)
    link = models.URLField(unique=True)
    tags = TaggableManager(blank=True)

    class Meta:
        db_table = 'inline_media_licenses'

    def homepage(self):
        return '<a href="%s" target="_new">%s</a>' % tuple([self.link]*2)
    homepage.allow_tags = True

    def __str__(self):
        return self.name

# ---------------------------------------------------------------------
# find_duplicates idea borrowed from django-filer by Stefan Foulis
# https://github.com/stefanfoulis/django-filer.git


class PictureManager(models.Manager):
    def find_duplicates(self, pic):
        return [p for p in self.exclude(pk=pic.pk).filter(sha1=pic.sha1)]


@python_2_unicode_compatible
class Picture(models.Model):
    """Picture model"""

    title = models.CharField(max_length=255)
    picture = ImageField(upload_to="pictures/%Y/%b/%d", storage=storage)
    show_as_link = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    show_description_inline = models.BooleanField(_("Show description inline"),
                                                  default=True)
    author = models.CharField(blank=True, null=False, max_length=255,
                              help_text=_("picture's author"))
    show_author = models.BooleanField(default=False)
    license = models.ForeignKey(License, blank=True, null=True)
    show_license = models.BooleanField(default=False)
    uploaded = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    sha1 = models.CharField(max_length=40, db_index=True,
                            blank=True, default="")
    tags = TaggableManager(blank=True)

    objects = PictureManager()

    class Meta:
        ordering = ('-uploaded',)
        db_table = 'inline_media_pictures'

    def save(self, *args, **kwargs):
        try:
            sha = hashlib.sha1()
            self.picture.seek(0)
            sha.update(self.picture.read())
            self.sha1 = sha.hexdigest()
        except Exception:
            self.sha1 = ""
        super(Picture, self).save(*args, **kwargs)

    def __str__(self):
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
        except Exception:
            return "unavailable"
        return '<div style="text-align:center"><img src="%s"></div>' % im.url
    thumbnail.allow_tags = True


def delete_picture(sender, instance, **kwargs):
    if sender == Picture:
        instance.picture.delete()


pre_delete.connect(delete_picture, sender=Picture)


@python_2_unicode_compatible
class PictureSet(models.Model):
    """ PictureSet model """
    title = models.CharField(
        help_text=_("Visible at the top of the gallery slider that shows up "
                    "when clicking on cover's picture."), max_length=255)
    slug = models.SlugField()
    description = models.TextField(
        help_text=_("Only visible in the inline under sizes "
                    "small, medium, large or full."), blank=True)
    show_description_inline = models.BooleanField(default=True)
    pictures = models.ManyToManyField("Picture", related_name="picture_sets")
    order = models.CharField(
        blank=True, max_length=512,
        validators=[validate_comma_separated_integer_list],
        help_text=_("Establish pictures order by typing the comma "
                    "separated list of their picture IDs."))
    show_counter = models.BooleanField(
        default=False, help_text=_("Whether to show how many pictures "
                                   "contains the pictureset."))
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    tags = TaggableManager(blank=True)

    class Meta:
        db_table = "inline_media_picture_sets"

    def __str__(self):
        return self.title

    # used in admin 'list_display' to show the thumbnail of self.picture
    def cover_thumbnail(self):
        im = get_thumbnail(self.cover().picture, "x50")
        return '<div style="text-align:center"><img src="%s"></div>' % im.url
    cover_thumbnail.allow_tags = True

    # used in admin 'list_display' to show the list of pictures' titles
    def picture_titles_as_ul(self):
        titles = []
        for picture in self.next_picture():
            if picture == self.cover():
                titles.append("<li>%s (cover)</li>" % picture.title)
            else:
                titles.append("<li>%s</li>" % picture.title)
        return '<ul>%s</ul>' % "".join(titles)
    picture_titles_as_ul.allow_tags = True

    def next_picture(self):
        picids = [p.id for p in self.pictures.all()]
        for elem in self.order.split(','):
            try:
                pid = int(elem)
                picids.remove(pid)
            except ValueError:
                break
            yield self.pictures.get(pk=pid)
        for pid in picids:
            yield self.pictures.get(pk=pid)

    def cover(self):
        if self.order:
            first_pic_id = int(self.order.split(',', 1)[0])
            try:
                return self.pictures.get(pk=first_pic_id)
            except:
                pass
        return self.pictures.all()[0]
