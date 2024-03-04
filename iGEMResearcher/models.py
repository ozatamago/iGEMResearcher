from django.db import models

class Team(models.Model):
    id = models.AutoField(primary_key=True)
    team = models.CharField(max_length=100)
    wiki = models.URLField()
    region = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    track = models.CharField(max_length=100)
    kind = models.CharField(max_length=100)
    section = models.CharField(max_length=100)
    year = models.IntegerField()
    description = models.TextField(null=True, blank=True) 
    summary = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.team

    def get_vectordb_text(self):
        # ベクトル化するテキストを返します
        return self.description

    def get_vectordb_metadata(self):
        # チームの各種情報をメタデータとして返します
        return {
            "id": self.id,
            "team": self.team,
            "wiki": self.wiki,
            "track": self.track,
            "year": self.year,
            "description": self.description,
            "summary": self.summary,
        }

