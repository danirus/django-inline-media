from django.contrib import admin

# from inline_media.admin import AdminWysihtml5TextFieldWithInlinesMixin
from wysihtml5.admin import AdminWysihtml5TextFieldMixin

from demo_wysihtml5.articles.models import Article

class ArticleAdmin(AdminWysihtml5TextFieldMixin, admin.ModelAdmin):
    list_display  = ('title', 'publish')
    list_filter   = ('publish',)
    search_fields = ('title', 'abstract', 'body')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = ((None, 
                  {'fields': ('title', 'slug', 'abstract', 'body', 
                              'publish',)}),)

admin.site.register(Article, ArticleAdmin)
