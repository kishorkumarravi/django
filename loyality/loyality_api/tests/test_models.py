from django.test import TestCase

from ..models import TranDetail
from .factories import TranDetailFactory


class TranTestCase(TestCase):
    def test_str(self):
        """Test for string representation."""
        tran = TranDetailFactory()
        self.assertEqual(str(tran), tran.cardType)