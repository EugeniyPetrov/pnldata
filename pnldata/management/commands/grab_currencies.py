from lxml import html
from urllib import urlencode, quote
import requests
import requests_cache
from django.core.management.base import BaseCommand, CommandError
from pnldata.models import Currency, Expense, ExchangeRate, Transaction
from django.db.models import Min, Max, Q
import datetime
from decimal import Decimal
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Grab currencies from xe.com'

    def _grab_currencies(self, date):
        url = "http://www.xe.com/currencytables/?%s" % (urlencode({
            "from": "EUR",
            "date": date.strftime("%Y-%m-%d"),
        }))

        if date == datetime.date.today():
            logger.debug("Request %s" % url)
            page = requests.get(url)
        else:
            with requests_cache.enabled(settings.XE_CACHE):
                logger.debug("Request %s from cache" % url)
                page = requests.get(url)

        tree = html.fromstring(page.content)

        currencies = {}
        rows = tree.cssselect("table#historicalRateTbl tbody tr")
        for row in rows:
            cols = row.cssselect('td')
            curr = cols[0].text_content()
            currencies[curr] = Decimal(cols[2].text_content())

        return currencies

    def _refresh_expences(self, date, currency):
        for expense in Expense.objects.filter(transaction__date=date, purse__currency=currency):
            logger.debug("Save expense %s" % expense)
            expense.save()

    def add_arguments(self, parser):
        parser.add_argument(
            '--update-all',
            action='store_true',
            help='Update all expences',
        )

    def handle(self, *args, **options):
        if options["update_all"]:
            dates = Expense.objects.all().values_list('transaction__date', flat=True).distinct()
        else:
            dates = Expense.objects.filter(Q(purse_amount_eur__isnull=True) | Q(purse_amount_usd__isnull=True)).values_list('transaction__date', flat=True).distinct()

        usd = Currency.objects.get(iso_code="USD")
        eur = Currency.objects.get(iso_code="EUR")

        for date in dates:
            grabbed_currencies = self._grab_currencies(date)
            currency_iso_codes = Expense.objects.filter(transaction__date=date).values_list('purse__currency__iso_code', flat=True).distinct()
            for iso_code in currency_iso_codes:
                if iso_code in grabbed_currencies:
                    units_per_eur = grabbed_currencies[iso_code]
                    currency = Currency.objects.get(iso_code=iso_code)
                    ExchangeRate.objects.update_or_create(
                        date=date,
                        currency=currency,
                        defaults={'units_per_eur': units_per_eur},
                    )
                for to_currency in (usd, eur,):
                    if iso_code != to_currency.iso_code and to_currency.iso_code in grabbed_currencies:
                        ExchangeRate.objects.update_or_create(
                            date=date,
                            currency=to_currency,
                            defaults={'units_per_eur': grabbed_currencies[to_currency.iso_code]},
                        )
                self._refresh_expences(date, currency)
