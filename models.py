from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Tag(models.Model):
    tagName = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.tagName

class Member(models.Model):
    usr = models.OneToOneField(User, on_delete=models.CASCADE)
    #email = models.EmailField()
    description = models.TextField(default='Hello there I am using ImageX!')
    avatar = models.ImageField(upload_to='userAvatar', blank=True, null=True)
    dailyUploadCount = models.IntegerField(default=0)
    totalUploadCount = models.IntegerField(default=0)

    def check_quota(self):
        DAILY_UPLOAD_QUOTA = 3
        TOTAL_UPLOAD_QUOTA = 4
        return (self.dailyUploadCount < DAILY_UPLOAD_QUOTA and self.totalUploadCount < TOTAL_UPLOAD_QUOTA)

    def __str__(self):
        return self.usr.username

class Category(models.Model):
    categoryName = models.CharField(max_length=30)

    def __str__(self):
        return self.categoryName

class Photo(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(default='Add photo description here.')
    ###imageFile = models.ImageField(upload_to='userImg')
    uploadTime = models.DateTimeField(default=timezone.now)
    uploadBy = models.ForeignKey(Member, on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag)

    # this function add tags to the photo
    def associate_tag(self, tag_info):
        MAX_TAG_NUMBER = 10
        tagList = tag_info.split()
        if len(tagList) + self.tags.count() > MAX_TAG_NUMBER:
            return False
        else:
            for tag in tagList:
                if Tag.objects.filter(tagName=tag).exists():
                    tmp_tag = Tag.objects.get(tagName=tag)
                    self.tags.add(tmp_tag)
                else:
                    tmp_tag = Tag.objects.create(tagName=tag)
                    self.tags.add(tmp_tag)
        return True

    def __str__(self):
    	return self.title


def match(keyword,filter,sortBy):
	'''
	to start a search for photos, support search gallery in the later version
	input: searching keyword, search category, sorting condition
	output: list of matched Photo objects
	'''
	matchedPhoto = Photo.objects.filter(tag__name__contains = keyword, category__name__iexact=filter)
	sortedPhoto = matchedPhoto.order_by(sortBy)
	return sortedPhoto


