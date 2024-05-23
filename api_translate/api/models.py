from django.db import models



class UserTelegram(models.Model):
    id = models.BigIntegerField(primary_key=True)


class Favorite(models.Model):

    class Status(models.TextChoices):
        NOT_LEARN = 'not_learn', 'NOT LEARN' 
        LEARN = 'learn', 'LEARN' 


    user = models.ForeignKey(UserTelegram, on_delete=models.CASCADE, related_name='favorite_words')
    text_from = models.TextField(max_length=1000)
    text_to = models.TextField(max_length=1000)
    status = models.CharField(max_length=9, choices=Status.choices, default=Status.NOT_LEARN)


