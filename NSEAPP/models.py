from django.contrib.auth.models import User
from django.db import models
# from decimal import Decimal
from nsetools import Nse
nse = Nse()

class Stock(models.Model):
    # id = models.AutoField(primary_key=True)
    symbol = models.CharField(max_length=10)
    # name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.symbol}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    predicted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


    def __str__(self):
        return f"{self.user.username}'s Watchlist - {self.stock.symbol} {self.predicted_price}"
  
