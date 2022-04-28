import os, random, urllib.request
from django.db import models
from django.conf import settings
from django.core.files import File




def upload_img_path(instance, filename):
    new_filename = random.randint(1,3910209312)
    name, ext = os.path.splitext(os.path.basename(filename))
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "QR/{final_filename}".format(final_filename=final_filename)

class QRCode(models.Model):
    user_id             = models.CharField(max_length=70, unique=True, default="")
    name                = models.CharField(max_length=300, default="")
    img                 = models.CharField(max_length=300, default="")


    def __str__(self):
        return self.user_id

    def get_image (self):
        if self.img:
            if settings.DEBUG:
                url = "http://localhost:8000" + self.img
            else:
                url = "https://python-api.bleanq.com" + self.img
           
            return url
        else:
            return ''

    def save_image(self, url):
        if url and not self.img:
            with open(url) as img:
                content = img.read()
            # result = urllib.request.urlretrieve(url)
            self.img.save(url, content)

        self.save()
        os.remove(url)