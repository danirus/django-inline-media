python manage.py dumpdata --indent 4 --format json \
	sites.Site \
	auth.User \
	articles.Article \
	inline_media.License \
	taggit.Tag \
	taggit.TaggedItem \
        inline_media.PictureSet \
	inline_media.Picture > initdata.json
