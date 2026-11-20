from django.db import models


class Note(models.Model):
    """Store a sticky note with its title, content, and creation time."""
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at', '-pk']

    def __str__(self):
        """Return the note title for readable display."""
        return self.title
