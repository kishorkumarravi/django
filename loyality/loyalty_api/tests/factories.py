from factory import DjangoModelFactory, Faker

from ..models import TranDetail


class TranDetailFactory(DjangoModelFactory):
    cardType = Faker('cardType')
    category = Faker('category')
    tran_date = Faker('tran_date')
    desc = Faker('desc')
    reward = Faker('reward')
    status = Faker('status')
    
    class Meta:
        model = TranDetailFactory