from django.db import models
# from PIL import Image
# Create your models here.

class NewsBox(models.Model):
    src_name    = models.CharField(max_length=255)
    src_link    = models.URLField()
    title       = models.CharField(max_length=255)
    img         = models.ImageField(blank=True)
    news_link   = models.URLField()
    created     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    # def save(self, *args, **kwargs):
    #     super(NewsBox, self).save(*args, **kwargs)
    #     if self.img:
    #         img = Image.open(self.img.path)
    #         if img.width > 300 or img.height > 300:
    #             output_size = (300,300)
    #             img.thumbnail(output_size)
    #             img.save(self.img.path)

    class Meta:
        ordering = ('-created',)
