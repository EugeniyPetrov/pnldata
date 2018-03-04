from django.db import models
from django.core.validators import MinLengthValidator

class Currency(models.Model):
    iso_code = models.CharField(max_length=3, unique=True, validators=[MinLengthValidator(3)])

    def __unicode__(self):
        return self.iso_code

    class Meta():
        verbose_name_plural = 'currencies'

class Purse(models.Model):
    name = models.CharField(max_length=255)
    currency = models.ForeignKey(Currency)

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.currency)

class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __unicode__(self):
        return '%s' % (self.name)

class Transaction(models.Model):
    date = models.DateField()
    description = models.CharField(max_length=255, blank=True)
    tag1 = models.ForeignKey(Tag, related_name='tags1', blank=True, null=True)
    tag2 = models.ForeignKey(Tag, related_name='tags2', blank=True, null=True)
    tag3 = models.ForeignKey(Tag, related_name='tags3', blank=True, null=True)

    def __unicode__(self):
        return '#%d %s (%s)' % (self.id, self.description, self.date,)

class Expense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.ForeignKey(Currency)
    purse = models.ForeignKey(Purse)
    purse_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    purse_amount_usd = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    purse_amount_eur = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    transaction = models.ForeignKey(Transaction)

    def __unicode__(self):
        return '%.2f %s (%s %s)' % (self.amount, self.currency, self.purse_amount, self.purse.currency,)

    def _convert_purse_amount(self, to_currency):
        from_rate = None
        for rate in ExchangeRate.objects.filter(date=self.transaction.date, currency=self.purse.currency)[:1]:
            from_rate = rate
        
        to_rate = None
        for rate in ExchangeRate.objects.filter(date=self.transaction.date, currency=to_currency)[:1]:
            to_rate = rate

        if not from_rate or not to_rate or not self.purse_amount:
            return None
        else:
            return self.purse_amount / from_rate.units_per_eur * to_rate.units_per_eur

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        self.purse_amount_usd = self._convert_purse_amount(Currency.objects.get(iso_code="USD"))
        self.purse_amount_eur = self._convert_purse_amount(Currency.objects.get(iso_code="EUR"))
        super(Expense, self).save(*args, **kwargs)

class ExchangeRate(models.Model):
    date = models.DateField()
    currency = models.ForeignKey(Currency)
    units_per_eur = models.DecimalField(max_digits=20, decimal_places=10)

    class Meta:
        unique_together = (('date', 'currency'),)
        indexes = [
           models.Index(fields=['date', 'currency']),
        ]
