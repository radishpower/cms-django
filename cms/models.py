from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.
class Category(models.Model):
  word = models.CharField(max_length=35)
  created = models.DateTimeField(auto_now_add=True)

  def __unicode__(self):
    return self.word
  
  def get_absolute_url(self):
    return reverse('category_permalink', args=(self.word,))


class Tag(models.Model):
  word = models.CharField(max_length=35)
  created = models.DateTimeField(auto_now_add=True)
  category = models.ForeignKey(Category, default=True)

  def __unicode__(self):
    return self.word

class MediaType(models.Model):
  word = models.CharField(max_length=35)
  created = models.DateTimeField(auto_now_add=True)

  def __unicode__(self):
    return self.word

class Logo(models.Model):
  logoimage = models.FileField(upload_to='cms/media/logoimgs/', blank=False, null=False)
  slug = models.SlugField(unique=True, max_length=255)
  created = models.DateTimeField(auto_now_add=True)

  def __unicode__(self):
    return self.slug

class CoverImage(models.Model):
  coverimage = models.FileField(upload_to='cms/media/postcoverimgs/', blank=False, null=False)
  
  def __unicode__(self):
    return self.coverimage.name

class Post(models.Model):
  styleformat = models.ForeignKey(MediaType)
  coverimage = models.ForeignKey(CoverImage)
  title = models.CharField(max_length=255)
  slug = models.SlugField(unique=True, max_length=255)
  description = models.CharField(max_length=255)
  content = models.TextField()
  published = models.BooleanField(default=True)
  created = models.DateTimeField(auto_now_add=False)
  tags = models.ManyToManyField(Tag)
  post_feature = models.CharField(max_length=255, default='#')

  def get_absolute_url(self):
    return reverse('post_permalink', args=(self.slug,))

  def __unicode__(self):
    return self.title

class MediaFile(models.Model):
  associated_post = models.ForeignKey(Post)
  slug = models.SlugField(unique=True, max_length=255)
  image = models.FileField(upload_to='cms/media/%Y/%m/%d')

  def get_absolute_url(self):
    return reverse('media_permalink', args=(self.slug,))

  def __unicode__(self):
    return self.image.name

class BannerAd(models.Model):
  adimage = models.FileField(upload_to='cms/media/ads/', blank=False, null=False)
  slug = models.SlugField(unique=True, max_length=255)
  urldst = models.CharField(default=True, max_length=255)
  created = models.DateTimeField(auto_now_add=True)

class MediaURLS(models.Model):
  name = models.CharField(default=True, max_length = 35)
  urldst = models.CharField(default=True, max_length=255)
  
  def __unicode__(self):
    return self.name

class TalkURLS(models.Model):
  name = models.CharField(default=True, max_length = 35)
  urldst = models.CharField(default=True, max_length=255)

  def __unicode__(self):
    return self.name

class ExternalURLS(models.Model):
  name = models.CharField(default=True, max_length = 35)
  urldst = models.CharField(default=True, max_length=255)

  def __unicode__(self):
    return self.name
