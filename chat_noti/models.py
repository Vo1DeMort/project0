from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Room(models.Model):
    participants = models.ManyToManyField(User)
    created = models.DateField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated']

    def __str__(self):
        participant_usernames = ','.join([user.username for user in self.participants.all()])
        return f'Participants: {participant_usernames}'



def validate_msg_length(value):
    if len(value) > 300:
        raise ValidationError("Message length should not exceed 300 characters.")



class Message(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name='message_sender')
    # after the migration ,null and blank 'd be set back to flase
    room = models.ForeignKey(Room,on_delete=models.CASCADE,related_name='message_room',null=True,blank=True)
    # a list of validator functions can be passed into the validator model filed
    message = models.TextField(max_length=300,default=None,validators=[validate_msg_length])
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'send by {self.sender.username}'

