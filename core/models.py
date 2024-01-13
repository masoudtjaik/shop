from django.db import models


# Create your models here.

class QuerySet(models.QuerySet):
    def delete(self):
        return super().update(is_deleted=True)

    def hard_delete(self):
        return super().delete()


class Manager(models.Manager):

    def get_queryset(self):
        return QuerySet(self.model).filter(is_deleted=False, is_active=True)

    def archive(self):
        return QuerySet(self.model)

    def deleted(self):
        return QuerySet(self.model).filter(is_deleted=True)


class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    objects = Manager()

    class Meta:
        abstract = True
        ordering = ('-created_at',)

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    def hard_delete(self):
        super().delete()

    def undelete(self):
        self.is_deleted = False
        self.save()

    def __str__(self) -> str:
        return f'{self.created_at}'


class StatusMixin:
    @property
    def status(self) -> bool:
        return self.is_active and not self.is_deleted  # noqa
