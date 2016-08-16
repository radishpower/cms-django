from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader, RequestContext
from .models import Logo, Tag, Post, BannerAd, Category, MediaURLS
from django.conf import settings
from django.core.paginator import Paginator

# Helper functions:
def fromposts_get_tagsimgs (SetOfPosts):
  tags_for_latest_living_posts = len(SetOfPosts)*[None]
  img_urls = len(SetOfPosts)*[None]
  tags = len(SetOfPosts)*[None]
  i = 0
  for post in SetOfPosts:
    post_tags_nonames = Tag.objects.filter(post__id=post.id)
    tags[i] = post_tags_nonames
    imageURL = str(post.coverimage.coverimage.name)
    img_urls[i] = settings.MEDIA_URL + imageURL
    i += 1
  zipped_posts = zip(SetOfPosts, img_urls, tags)

  return zipped_posts

# Create your views here.
def index(request):
 
  feature_tag = Tag.objects.filter(word = 'fashion')
  number_of_posts = 2 
  
  all_categories = Category.objects.all()
  all_mediaurls = MediaURLS.objects.all()
  
  fashion_posts = Post.objects.filter(tags=feature_tag)
  latest_living_posts = fashion_posts.order_by('created').reverse()[:number_of_posts]
  zipped_living_posts = fromposts_get_tagsimgs (latest_living_posts)
  
  number_of_posts = 4+1
  latest_posts = Post.objects.order_by('created').reverse()[:number_of_posts]
  zipped_latest_posts = fromposts_get_tagsimgs (latest_posts)

  number_of_posts = 3
  feature_tag = Tag.objects.filter(word = 'scitech')
  scitech_posts = Post.objects.filter(tags=feature_tag)
  latest_scitech_posts = scitech_posts.order_by('created').reverse()[:number_of_posts]
  zipped_scitech_posts = fromposts_get_tagsimgs (latest_scitech_posts)

  number_of_posts = 4
  feature_tag = Tag.objects.filter(word = 'pioenabled')
  pioenabled_posts = Post.objects.filter(tags=feature_tag)
  latest_pioenabled_posts = pioenabled_posts.order_by('created').reverse()[:number_of_posts]
  zipped_pioenabled_posts = fromposts_get_tagsimgs (latest_pioenabled_posts)


  current_entry = latest_posts[0]
  post_title = current_entry.title
  post_description = current_entry.description
  post_date = current_entry.created
  post_url = current_entry.get_absolute_url()
  post_tags_nonames = Tag.objects.filter(post__id=current_entry.id)
  imageURL = str(current_entry.coverimage.coverimage.name)
  post_imgurl = settings.MEDIA_URL + imageURL

  latest_banner_ad = BannerAd.objects.latest('created')
  banner_filename = settings.MEDIA_URL + latest_banner_ad.adimage.name
  banner_dsturl = latest_banner_ad.urldst

  logo_filename = settings.MEDIA_URL + Logo.objects.latest('created').logoimage.name

  context = RequestContext(request, {
    'post_title': post_title,
    'post_description': post_description,
    'post_date': post_date,
    'post_tags': post_tags_nonames,
    'post_imgurl': post_imgurl,
    'post_url': post_url,
    'all_categories': all_categories,
    'all_mediaurls': all_mediaurls,
    'zipped_living_posts': zipped_living_posts,
    'zipped_latest_posts': zipped_latest_posts,
    'zipped_scitech_posts': zipped_scitech_posts,
    'zipped_pioenabled_posts': zipped_pioenabled_posts,
    'banner_filename': banner_filename,
    'banner_dsturl': banner_dsturl,
    'logo_filename': logo_filename,
  })

  template = loader.get_template('cms/index.html')
  return HttpResponse(template.render(context))

def about(request):
  template = loader.get_template('cms/about.html')
  return HttpResponse(template.render())

def contact(request):
  template = loader.get_template('cms/contact.html')
  return HttpResponse(template.render())

def categories(request, word=None):
  allcategories = Category.objects.all()
  allmediaurls = MediaURLS.objects.all()

  onecategory = Category.objects.get(word = word)
  all_relevant_tags = Tag.objects.filter(category = onecategory)
  filtered_posts = []
  for tag in all_relevant_tags:
    related_posts = Post.objects.filter(tags = tag)
    filtered_posts.extend(related_posts)

  number_of_posts = 4
  latest_post_list = Post.objects.order_by('created').reverse()[:4]
  zipped_latest_posts = fromposts_get_tagsimgs(latest_post_list)

  zipped_filtered_posts = fromposts_get_tagsimgs (filtered_posts)

  template = loader.get_template('cms/categories-1.html')

  latest_banner_ad = BannerAd.objects.latest('created')
  banner_filename = settings.MEDIA_URL + latest_banner_ad.adimage.name
  banner_dsturl = latest_banner_ad.urldst

  context = RequestContext(request, {
    'word': word,
    'zipped_filtered_posts': zipped_filtered_posts,
    'zipped_latest_posts': zipped_latest_posts,
    'banner_filename': banner_filename,
    'banner_dsturl': banner_dsturl,
    'all_categories': allcategories,
    'all_mediaurls': allmediaurls,
  })

  return HttpResponse(template.render(context))

def singlepost(request, slug=None):

  has_previous = False
  has_next = True
  previous_posturl = False
  next_posturl = False
  number_of_posts = 4
  latest_post_list = Post.objects.order_by('created').reverse()

  if slug:
    current_entry = Post.objects.get(slug = slug)
  else:
    current_entry = latest_post_list[0]

  current_id = current_entry.id
  total_posts = len(latest_post_list)
  postids = total_posts*[None]
  foundindex = 0
  for i in range(total_posts):
    onepost = latest_post_list[i]
    postids[i] = onepost.id
    if latest_post_list[i].id == current_id:
      foundindex = i

  if foundindex > 0: has_previous = True
  else: pass

  if foundindex == (total_posts-1): has_next = False
  else: pass

  if has_previous:
    val = postids[foundindex-1]
    previous_post = Post.objects.get(id=val)
    previous_posturl = previous_post.get_absolute_url()

  else: pass

  if has_next: 
    val = postids[foundindex+1]
    next_post = Post.objects.get(id=val)
    next_posturl = next_post.get_absolute_url()
  else: pass


  all_categories = Category.objects.all()
  all_mediaurls = MediaURLS.objects.all()

  latest_post_list = latest_post_list[:(number_of_posts)]
  post_tags_nonames = Tag.objects.filter(post__id=current_entry.id)

  latest_post_list = latest_post_list[1:number_of_posts] #Display most recent 4 latest_posts

  corresponding_tags = (number_of_posts-1)*['']

  for i in range(number_of_posts-1):
    taglist = Tag.objects.filter(post__id=latest_post_list[i].id)
    tagstringlist = len(taglist)*['']
    for j in range(len(taglist)):
      tagstringlist[j] = taglist[j].word
    corresponding_tags[i] = taglist
  zipped_list = zip(latest_post_list, corresponding_tags)

  template_nametype = ''
  if str(current_entry.styleformat) == 'standard':
    template_nametype = 'cms/standard-format.html'
    breadcrumb = 'Standard Format'
    post_feature = '#'
  elif str(current_entry.styleformat) == 'video':
    template_nametype = 'cms/video-format.html'
    post_feature = settings.MEDIA_URL + current_entry.post_feature
    breadcrumb = 'Video Format'
  else:
    pass

  latest_banner_ad = BannerAd.objects.latest('created')
  banner_filename = settings.MEDIA_URL + latest_banner_ad.adimage.name
  banner_dsturl = latest_banner_ad.urldst

  logo_filename = settings.MEDIA_URL + Logo.objects.latest('created').logoimage.name

  context = RequestContext(request, {
    'all_categories': all_categories,
    'all_mediaurls': all_mediaurls,
    'post_title': current_entry.title,
    'post_content': current_entry.content,
    'post_created': current_entry.created,
    'post_tags': post_tags_nonames,
    'post_feature': post_feature,
    'zipped_list': zipped_list,
    'breadcrumb': breadcrumb,
    'banner_filename': banner_filename,
    'banner_dsturl': latest_banner_ad.urldst,
    'logo_filename': logo_filename,
    'previous_posturl': previous_posturl,
    'next_posturl': next_posturl,
  })

  template = loader.get_template(template_nametype)
  return HttpResponse(template.render(context))
