from django.db import models


# Create your models here.
class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering=('-created_at',)
    def __str__(self) -> str:
        return f'{self.created_at}'