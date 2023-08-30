from django.db import models
from django.contrib.auth.models import User

# from django.utils.timesince import timesince ??

class Profile (models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic = models.ImageField(blank=True,upload_to ='images/profile_pics/')
    bio = models.TextField(max_length=150,blank=True)
    link = models.TextField(max_length=300,blank=True)
    joined = models.DateField(auto_now_add=True)
    follow = models.ManyToManyField(
    # self , create realtionship to the instances of the same model , that's pretty neat
    'self',
    related_name='followed_by',
    symmetrical=False,
    blank=True)
    ''' 
    no_of_followers = profile.followed_by.count()
    '''

    def __str__(self):
        return self.user.username

class Post (models.Model):
    owner = models.ForeignKey(Profile,on_delete=models.CASCADE)
    story = models.TextField(max_length=300)
    # i could user carousel to show pic in the profile.html
    pictures = models.ImageField(blank=True,upload_to='images/photos')
    likes = models.ManyToManyField(User,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created']


    def no_of_comments(self):
        pass
    
    def __str__(self):
        return (
            f'{self.owner}'
            f'{self.story}'
            f'{self.created}'
        )

# commenting working without django forms , worth to learn, read the home.html
# i saw a bootsrap form which might be suitable to show comments 
class Comment (models.Model):
    # many to one , many comments to a post
    post= models.ForeignKey(Post,on_delete=models.CASCADE)
    writer = models.ForeignKey(Profile,on_delete=models.CASCADE)
    comment = models.TextField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'comment by :{self.writer.user.username} on post :{self.post}'







