# coding: utf-8
from datetime import datetime
from django.db.models import Avg
from django.test import TestCase

from myhome.models import Seneor


class UV_valueViewTestCase(TestCase):

    def setUp(self):
        now = datetime.now()
        Seneor.objects.create(Tvalue=23.00, Hvalue=42.00, Uvalue=12, time=now)
        Seneor.objects.create(Tvalue=23.00, Hvalue=42.00, Uvalue=24, time=now)

    def test_json_data(self):
        alldata = Seneor.objects.filter(time__day=datetime.today().day)
        result = alldata.extra({'hour': 'HOUR(time)'}).values('hour') \
            .annotate(Avg('Uvalue'))
        top_item = result[0]
        assert 'hour' in top_item
        assert 'Uvalue__avg' in top_item
        assert top_item['Uvalue__avg'] == (12 + 24) / 2
