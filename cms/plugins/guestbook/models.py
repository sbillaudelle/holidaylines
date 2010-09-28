from django.db import models

class GuestbookEntry(models.Model):

    title = models.CharField(max_length=200)
    content = models.TextField()

    def __unicode__(self):
        return u"{0}".format(self.title)

