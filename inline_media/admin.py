from django.contrib import admin

from inline_media.fields import TextFieldWithInlines
from inline_media.models import License, Picture, PictureSet
from inline_media.widgets import TextareaWithInlines


class LicenseAdmin(admin.ModelAdmin):
    list_display = ("name", "homepage")
    list_filter = ("tags",)
    search_fields = ("name", "tags")


class AdminTextFieldWithInlinesMixin(object):
    """Mixin to provide custom widget for ``TextFieldWithInlines`` fields."""
    def formfield_for_dbfield(self, db_field, **kwargs):
        if isinstance(db_field, TextFieldWithInlines):
            return db_field.formfield(widget=TextareaWithInlines)
        sup = super(AdminTextFieldWithInlinesMixin, self)
        return sup.formfield_for_dbfield(db_field, **kwargs)


class PictureAdmin(admin.ModelAdmin):
    list_display = ("thumbnail", "title", "modified")
    list_editable = ("title",)
    list_filter = ("tags", "author", "license")
    search_fields = ("title", "tags", "description", "author")
    date_hierarchy = "uploaded"
    fieldsets = (
        (None, {"fields": (("title", "show_as_link"),
                           "picture",
                           ("description", "show_description_inline"),
                           "tags",
                           ("author", "show_author"),
                           ("license", "show_license"),
                           ("modified", "uploaded"),
                           "sha1",), }),
    )
    readonly_fields = ("modified", "uploaded", "sha1",)
    list_per_page = 50

    class Media:
        css = {"all": ("prettyphoto-3.1.3/css/prettyPhoto.css",)}
        js = ("prettyphoto-3.1.3/js/jquery-1.6.1.min.js",
              "prettyphoto-3.1.3/js/jquery.prettyPhoto.js",
              "admin/inline_media/js/picture.js")


class PictureSetAdmin(admin.ModelAdmin):
    list_display = ("title", "cover_thumbnail",
                    "picture_titles_as_ul", "modified")
    list_filter = ("tags",)
    search_fields = ("title", "tags", "description",
                     "pictures__title", "pictures__description",
                     "pictures__tags")
    date_hierarchy = "modified"
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ("pictures",)
    fieldsets = (
        (None, {'fields': ('title', 'slug',
                           ('description', 'show_description_inline'),
                           'pictures', 'order',
                           'show_counter', 'tags'), }),
    )
    list_per_page = 50

    class Media:
        css = {"all": ("prettyphoto-3.1.3/css/prettyPhoto.css",)}
        js = ("prettyphoto-3.1.3/js/jquery-1.6.1.min.js",
              "prettyphoto-3.1.3/js/jquery.prettyPhoto.js",
              "admin/inline_media/js/pictureset.js")


admin.site.register(License, LicenseAdmin)
admin.site.register(Picture, PictureAdmin)
admin.site.register(PictureSet, PictureSetAdmin)
