from django.contrib import admin
from .models import Logo, Post, MediaFile, MediaType, CoverImage, Tag, BannerAd, MediaURLS, TalkURLS, ExternalURLS, Category

class MediaFileAdminInline(admin.TabularInline):
  model = MediaFile

class PostAdmin(admin.ModelAdmin):
  inlines = (MediaFileAdminInline, )

# Register your models here.
admin.site.register(Logo)
admin.site.register(Post, PostAdmin)
admin.site.register(CoverImage)
admin.site.register(MediaFile)
admin.site.register(MediaType)
admin.site.register(Tag)
admin.site.register(BannerAd)
admin.site.register(MediaURLS)
admin.site.register(TalkURLS)
admin.site.register(ExternalURLS)
admin.site.register(Category)
