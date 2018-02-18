from django.contrib import admin

from image.models import Album, Picture, FavoriteAlbum, FavoritePicture


class AlbumAdmin(admin.ModelAdmin):
    filter_horizontal = ("pictures",)


admin.site.register(Album, AlbumAdmin)
admin.site.register(FavoriteAlbum)
admin.site.register(Picture)
admin.site.register(FavoritePicture)
