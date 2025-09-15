from django.db import models

class Songs(models.Model):
    song_id = models.AutoField(primary_key=True)
    mood = models.CharField(max_length=50)
    file_path = models.TextField()
    
    def __str__(self):
        return f"{self.mood} - {self.file_path}"

class Quotes(models.Model):
    quote_id = models.AutoField(primary_key=True)
    mood = models.CharField(max_length=50)
    quote = models.TextField()
    
    def __str__(self):
        return f"{self.mood} - {self.quote[:30]}"

class Journal(models.Model):
    journal_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    mood = models.CharField(max_length=50)
    song = models.ForeignKey(Songs, on_delete=models.CASCADE)
    quote = models.ForeignKey(Quotes, on_delete=models.CASCADE)
    request_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.username} - {self.mood} - {self.request_time}"
