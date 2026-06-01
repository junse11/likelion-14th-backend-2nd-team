from django.db import models

class Movie(models.Model):
    GENRE_CHOICES = [
        ('action', '액션'),
        ('drama', '드라마'),
        ('comedy', '코미디'),
        ('thriller', '스릴러'),
        ('romance', '로맨스'),
        ('sf', 'SF'),
        ('horror', '공포'),
        ('animation', '애니메이션'),
    ]

    title = models.CharField(max_length=200)
    director = models.CharField(max_length=100)
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES)
    release_year = models.IntegerField()
    description = models.TextField(blank=True)
    poster_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-release_year', 'title']

    def __str__(self):
        return f"{self.title} ({self.release_year})"
