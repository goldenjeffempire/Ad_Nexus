from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    interests = models.TextField()  # Store user interests as a JSON string
    preferences = models.TextField()  # Store preferences for ad categories

    def __str__(self):
        return self.user.username

class Ad(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)
    target_audience = models.TextField()  # JSON string defining audience attributes
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Recommendation(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    score = models.FloatField()  # Relevance score

    def __str__(self):
        return f"{self.user.user.username} -> {self.ad.title} (Score: {self.score})"

class AdSimulation(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    impressions = models.IntegerField(default=0)
    clicks = models.IntegerField(default=0)
    conversions = models.IntegerField(default=0)
    ctr = models.FloatField(default=0.0)  # Click-Through Rate
    conversion_rate = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Simulation for {self.ad.title} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
