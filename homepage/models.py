from django.db import models
from litmus.models import Profile

# Model to save notes
class Notes(models.Model):
    user_profile = models.ForeignKey(Profile, on_delete = models.CASCADE)
    diary_notes = models.TextField(blank = False)
    create_time = models.DateTimeField(auto_now_add=True)
    no_of_likes = models.IntegerField(default = 0)
    is_public = models.BooleanField(default = False)


