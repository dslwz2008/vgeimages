from django.db import models


class ResultImages(models.Model):
    paraName = models.CharField(max_length=200, unique=True)
    status = models.PositiveSmallIntegerField()
    imageDir = models.CharField(max_length=200, unique=True)
    imageNum = models.IntegerField()

    def __unicode__(self):
        return '%s %d %s %d' % (self.paraName, self.status, self.imageDir, self.imageNum)

