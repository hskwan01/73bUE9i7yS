from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Tag(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def associate_tag(self,tname):
        self.name = tname
        self.save()

    def __str__(self):
        return self.name

class Member(models.Model):
    usr = models.OneToOneField(User, on_delete=models.CASCADE)
    #email = models.EmailField()
    description = models.TextField(default='Hello there I am using ImageX!')
    avatar = models.ImageField(upload_to='userAvatar',blank=True,null=True)
    dailyUploadCount = models.IntegerField()
    totalUploadCount = models.IntegerField()

    def check_quota(self):
        DAILY_UPLOAD_QUOTA = 3
        return (self.dailyUploadCount > DAILY_UPLOAD_QUOTA)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Photo(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(default='Add photo description here.')
    imageFile = models.ImageField(upload_to='userImg')
    uploadTime = models.DateTimeField(default=timezone.now)
    uploadBy = models.ForeignKey(Member, on_delete=models.CASCADE)
    category = models.OneToOneField(Category,on_delete=models.SET_NULL, null=True)
    tag = models.ManyToManyField(Tag)


def match(keyword,filter,sortBy):
    '''
    to start a search for photos, support search gallery in the later version
    input: searching keyword, search category, sorting condition
    output: list of matched Photo objects
    '''
    matchedPhoto = Photo.objects.filter(tag__name__contains = keyword, category__name__iexact=filter)
    sortedPhoto = matchedPhoto.order_by(sortBy)
    return sortedPhoto
