from tkinter import CASCADE
from django.db import models
import uuid

# Create your models here.
class Prompt(models.Model):
    ENGINE_TYPE = (
        ('text-davinci-002','New Instruct Davinci'),
        ('text-davinci-001','Old Instruct Davinci'),
        ('text-curie-001','Instruct Curie')
    )
    LANGUAGE_TYPE = (
        ('en','English'), ('es','Spanish'), ('de', 'German'), ('nl','Dutch'), ('fr','French')
    )
    article_name = models.CharField(max_length=2000, blank=True, null=True)
    url = models.TextField(null=True, blank=True)
    prompt = models.TextField()
    myFile = models.FileField(upload_to='Docs/', blank=True, null=True)
    engine = models.CharField(max_length=150, choices=ENGINE_TYPE)
    language = models.CharField(max_length=150, choices=LANGUAGE_TYPE)
    summary = models.TextField(null=True, blank=True)
    audio = models.FileField(upload_to='audios/',null=True, blank=True)
    myRange = models.CharField(max_length=4,default=400)
    VOTE_TOTAL = models.IntegerField(default=0, null=True, blank=True)
    VOTE_RATIO = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)

    def __str__(self):
        if self.article_name is None:
            return self.id
        else:
            return self.article_name

    # def __str__(self):
    #     print(self.article_name)
    #     return super().__str__()

class Review(models.Model):
    STAR_TYPE = (
        ('None',None),
        ('1','Poor'),
        ('2','Below Average'),
        ('3','Average'),
        ('4','Above Average'),
        ('5','Excellent')
    )
    review = models.ForeignKey(Prompt, on_delete=models.CASCADE)
    comments = models.TextField(null=True,blank=True)
    rate = models.CharField(max_length=100, null=True,blank=True,choices=STAR_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True) 

    def __str__(self):
        return str(self.review)

class PromptReview(models.Model):
    ENGINE_TYPE = (
        ('text-davinci-002','New Instruct Davinci'),
        ('text-davinci-001','Old Instruct Davinci'),
        ('text-curie-001','Instruct Curie')
    )
    LANGUAGE_TYPE = (
        ('en','English'), ('es','Spanish'), ('de', 'German'), ('nl','Dutch'), ('fr','French')
    )
    STAR_TYPE = (
        ('None',None),
        ('1','Poor'),
        ('2','Below Average'),
        ('3','Average'),
        ('4','Above Average'),
        ('5','Excellent')
    )
    article_name = models.CharField(max_length=2000, blank=True, null=True)
    url = models.TextField(null=True, blank=True)
    prompt = models.TextField()
    myFile = models.FileField(upload_to='Docs/', blank=True, null=True)
    engine = models.CharField(max_length=150, choices=ENGINE_TYPE)
    language = models.CharField(max_length=150, choices=LANGUAGE_TYPE)
    summary = models.TextField(null=True)
    audio = models.FileField(upload_to='audios/',null=True, blank=True)
    comments = models.TextField(null=True,blank=True)
    rate = models.CharField(max_length=100, null=True,blank=True,choices=STAR_TYPE)
    VOTE_TOTAL = models.IntegerField(default=0, null=True, blank=True)
    VOTE_RATIO = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)

    def __str__(self):
        if self.article_name is None:
            return self.id
        else:
            return self.article_name