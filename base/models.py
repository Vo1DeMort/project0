from django.db import models
from django.contrib.auth.models import User

class Profile (models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic = models.ImageField(blank=True,upload_to ='images/profile_pics/')
    bio = models.TextField(max_length=150,blank=True)
    link = models.TextField(max_length=300,blank=True)
    joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Post (models.Model):
    owner = models.ForeignKey(Profile,on_delete=models.CASCADE)
    story = models.TextField(max_length=300)
    pictures = models.ImageField(blank=True,upload_to='images/photos')
    likes = models.ManyToManyField(User,blank=True)
    follow = models.ManyToManyField(
    # self , create realtionship to the instances of the same model , that's pretty neat
    'self',
    related_name='followed_by',
    symmetrical=False,
    blank=True)
    ''' 
    no_of_followers = profile.followed_by.count()
    '''
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created']

    '''
    def no_of_likes(self):
        return self.likes.count()

    '''

    def no_of_comments(self):
        pass
    
    def __str__(self):
        return (
            f'{self.owner}'
            f'{self.story}'
            f'{self.created}'
        )

class Comment (models.Model):
    post= models.ForeignKey(Post,on_delete=models.CASCADE)
    writer = models.ForeignKey(Profile,on_delete=models.CASCADE)
    comment = models.TextField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'comment by :{self.writer.user.username} on post :{self.post}'

 # this model is just a basic thing , not quite good enough for real app
 # i should make a different app for the message and notifications features which require djagno channel and asgi
class Message (models.Model):
    # use some relative names coz two fileds are clashing
    sender = models.ForeignKey(User,related_name='message_sender',on_delete=models.CASCADE)
    receiver = models.ForeignKey(User,related_name='message_receiver',on_delete=models.CASCADE)
    message = models.TextField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated']

    def __str__(self):
        return f'Message from {self.sender.username} to {self.receiver.username} at {self.created}'

class GroupMessage(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User,related_name='chat_owner',on_delete=models.CASCADE)
    participants = models.ManyToManyField(User,related_name='chat_participants')
    message = models.TextField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated']

    def __str__(self):
        return (
            f'{self.name} '
            f'by {self.owner.username}'
        )






