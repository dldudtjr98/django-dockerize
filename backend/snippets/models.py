from django.db import models
from django.contrib.auth.models import AbstractUser
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(
        default='',
        max_length=100, 
        blank=True, 
    )
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(
        default='python',
        max_length=100,
    )
    style = models.CharField(
        default='friendly',
        max_length=100,
    )
    owner = models.ForeignKey(
        'cert.CustomUser', 
        related_name='snippets', 
        on_delete=models.CASCADE
    )
    highlighted = models.TextField()

    class Meta:
        ordering = ['created',]

    def save(self, *args, **kwargs):
        """
        `pygments` 라이브러리를 사용하여 하이라이트된 코드를 만든다.
        """
        lexer = get_lexer_by_name(self.language)
        linenos = self.linenos and 'table' or False
        options = self.title and {'title': self.title} or {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos, full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super(Snippet, self).save(*args, **kwargs)

    def __str__(self):
        return f"{ self.title }"

