# models.py
from django.db import models

class TranDetail(models.Model):
    # id = models.CharField(max_length=60)
    cardType = models.CharField(max_length=60)
    category = models.CharField(max_length=60)
    tran_date = models.CharField(max_length=60)
    desc = models.CharField(max_length=60)
    reward = models.CharField(max_length=60)
    status = models.CharField(max_length=60)
    
    def __str__(self):
        return self.cardType
        # return f'{self.cardType}, {self.category}, {self.tran_date}, {self.desc}, \
        #     {self.reward}, {self.status}'