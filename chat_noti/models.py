from django.db import models
from django.contrib.auth.models import User

'''
i am gonna use this app to write message thing and notification ,coz they required async and django channels
'''

 # need to user django channel
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
