python manage.py dumpdata --indent 4 --format json \
	sites.Site \
	auth.User \
	articles.Article \
	inline_media.InlineType \
	inline_media.License \
	tagging.Tag \
	tagging.TaggedItem \
        inline_media.PictureSet \
	inline_media.Picture > initial_data.json
