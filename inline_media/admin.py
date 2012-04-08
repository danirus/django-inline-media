#-*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin
from django.contrib.admin.util import unquote

from inline_media.fields import TextFieldWithInlines
from inline_media.models import InlineType, License, Picture, PictureSet
from inline_media.widgets import TextareaWithInlines


class LicenseAdmin(admin.ModelAdmin):
    list_display = ("name", "tags", "homepage")
    list_editable = ("tags",)
    list_filter = ("tags",)
    search_fields = ("name", "tags")


class AdminTextFieldWithInlinesMixin(object):
    """Mixin for ModelAdmin subclasses to provide custom widget for ``TextFieldWithInlines`` fields."""
    def formfield_for_dbfield(self, db_field, **kwargs):
        if isinstance(db_field, TextFieldWithInlines):
            return db_field.formfield(widget=TextareaWithInlines)
        sup = super(AdminTextFieldWithInlinesMixin, self)
        return sup.formfield_for_dbfield(db_field, **kwargs)


class PictureAdmin(admin.ModelAdmin):
    list_display = ("thumbnail", "title", "tags", "modified")
    list_editable = ("title", "tags")
    list_filter  = ("tags", "author", "license")
    search_fields = ("title", "tags", "description", "author")
    date_hierarchy = "modified"
    fieldsets = (
        (None, {"fields": (("title", "show_as_link"),
                           "picture", "description", "tags",
                           ("author", "show_author"), 
                           ("license", "show_license"),
                           ("modified", "uploaded"),
                           "sha1",),
        }),
    )
    readonly_fields = ("modified", "uploaded", "sha1",)
    list_per_page = 50

    class Media:
        css = { "all": ("prettyphoto-3.1.3/css/prettyPhoto.css",) }
        js = ("prettyphoto-3.1.3/js/jquery-1.6.1.min.js",
              "prettyphoto-3.1.3/js/jquery.prettyPhoto.js",
              settings.STATIC_URL + "admin/inline_media/js/picture.js")


class PictureSetAdmin(admin.ModelAdmin):
    list_display = ("title", "cover_thumbnail", 
                    "picture_titles_as_ul", "modified")
    list_filter  = ("tags",)
    date_hierarchy = "modified"
    search_fields = ("title", "tags", "description", 
                     "pictures__title", "pictures__description", 
                     "pictures__tags")
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ("pictures",)
    raw_id_fields = ("cover",)
    list_per_page = 50

    class Media:
        css = { "all": ("prettyphoto-3.1.3/css/prettyPhoto.css",) }
        js = ("prettyphoto-3.1.3/js/jquery-1.6.1.min.js",
              "prettyphoto-3.1.3/js/jquery.prettyPhoto.js",
              settings.STATIC_URL + "admin/inline_media/js/pictureset.js")

    def change_view(self, request, object_id, extra_context=None):
        response = super(PictureSetAdmin, self).change_view(
            request, object_id, extra_context=extra_context)
        obj = self.get_object(request, unquote(object_id))
        if obj.cover not in obj.pictures.all():
            obj.pictures.add(obj.cover)
        return response


admin.site.register(InlineType)
admin.site.register(License,    LicenseAdmin)
admin.site.register(Picture,    PictureAdmin)
admin.site.register(PictureSet, PictureSetAdmin)
