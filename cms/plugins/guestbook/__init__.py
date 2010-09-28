from django.db import models
from cms import plugins
from django.template import Template, Context
import urllib
import urllib2

class GuestbookEntry(models.Model):

    name = models.CharField(max_length=200)
    content = models.TextField()

    date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u"{0}".format(self.title)


def handler_post(request):
    f = urllib2.urlopen('http://www.google.com/recaptcha/api/verify', urllib.urlencode(dict(
            privatekey='6LfHk7sSAAAAADWUwu_KESc-rByhEKXrlINtI3_1'.encode('utf-8'),
            remoteip=request.META['REMOTE_ADDR'].encode('utf-8'),
            challenge=request.POST['recaptcha_challenge_field'].encode('utf-8'),
            response=request.POST['recaptcha_response_field'].encode('utf-8'))))
    data = f.read()
    f.close()

    if data.split('\n')[0].strip() == 'true':
        e = GuestbookEntry(name=request.POST['name'], content=request.POST['content'])
        e.save()


HANDLERS = {
    '/post': handler_post
    }

def process(data):

    try:
        plugins.install_model(GuestbookEntry)
    except:
        pass

    entries = GuestbookEntry.objects.all()
    template = Template(data)
    return template.render(Context({
            'entries': entries
            }))
