import uuid
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Book(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.CharField(("title"), max_length=200)
    author = models.CharField(("author"), max_length=200)
    price = models.DecimalField(("price"), max_digits=6, decimal_places=2)
    cover = models.ImageField(("cover"), upload_to='covers/',blank=True, null=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['id'], name='id_index')
        ]
        permissions = [
            ('special_status','can read all books'),
        ]
        verbose_name = ("book")
        verbose_name_plural = ("books")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book_details", kwargs={"pk": self.pk})


class Review(models.Model):

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='reviews'    
    )
    review = models.CharField(("review"), max_length=255)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = ("Review")
        verbose_name_plural = ("Reviews")

    def __str__(self):
        return self.review

    def get_absolute_url(self):
        return reverse("Review_detail", kwargs={"pk": self.pk})
