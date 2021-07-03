from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.

class Page(models.Model):
    name = models.CharField(max_length=100, default='pagename')
    page_id = models.IntegerField(null=True, blank=True)
    likes = models.IntegerField(null=True, blank=True, default=0)
    category = models.CharField(max_length=200, null=True)
    scraped_at = models.DateTimeField(auto_now_add=True)
    is_notable = models.BooleanField(default=False)

    def __str__(self):
        return self.name



class Advertisement(models.Model):
    parent = models.ForeignKey(Page, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, null = True)
    started_running_on = models.CharField(max_length=100, null = True)
    main_text = models.CharField(max_length=200, null=True)
    sub_text = models.CharField(max_length=200, null=True)# ?
    ad_id = models.IntegerField(null=True, blank=True, default=0)
    image_url = models.CharField(max_length=500, null=True)
    lp_url = models.CharField(max_length=500, null=True)
    memo = models.TextField(max_length=500, null=True, blank=True)
    scraped_at = models.DateTimeField(auto_now_add=True)
    is_favorite  = models.BooleanField(default=False)

    # def __str__(self):
    #     return self.main_text[:30]
