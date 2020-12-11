from django.db import models


class Article(models.Model):
    #author = models.ForeignKey(Journalist, on_delete=models.CASCADE, related_name="articles")
    author = models.CharField(max_length=120)
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=200)
    body = models.TextField()
    location = models.CharField(max_length=120)
    publication_date = models.DateTimeField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{ self.author } { self.title }"