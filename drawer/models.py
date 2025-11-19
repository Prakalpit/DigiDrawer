import os
from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Tags'


    def __str__(self):
        return self.name


class File(models.Model):
    file = models.FileField(upload_to='files/')
    tags = models.ManyToManyField(Tag, blank=True)
    name = models.CharField(max_length=255)
    is_archived = models.BooleanField(default=False)
    file_size = models.PositiveIntegerField(null=True, blank=True)
    content_type = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.file and not self.pk:
            if not self.name:
                self.name = os.path.basename(self.file.name)
            self.file_size = self.file.size

            try:
                # Access the content_type from the uploaded file object
                self.content_type = self.file.file.content_type
            except AttributeError:
                self.content_type = ''

        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name



class RecycleBin(models.Model):
    pass