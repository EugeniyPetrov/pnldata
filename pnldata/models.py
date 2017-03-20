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

class Expense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.ForeignKey(Currency)
    purse = models.ForeignKey(Purse)
    purse_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    transaction = models.ForeignKey(Transaction)
