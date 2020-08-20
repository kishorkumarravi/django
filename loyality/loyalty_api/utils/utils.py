# Utils for URL
import logging

from ..serializers import TranSerializer

card_reward = {'Silver':1, 'Gold':2, 'Platinum':4, 'Black':8}

def create_new_rec(record):
    try:
        logging.info(f'record.. {record}')
        tran_serializer = TranSerializer(data=record)
        if tran_serializer.is_valid():
            tran_serializer.save()
            logging.info('Saved..')
            return True
        return False
            
    except Exception as err:
        logging.info(f'err.. {err}')
        return False

def get_reward(req_data):
    try:
        amount = req_data['amount']
        temp_reward = str(int(amount)/150)[:1]
        cardType = req_data['cardType']
        rewardType = card_reward[cardType]
        org_reward = int(temp_reward)*int(rewardType)
        logging.info(f'reward :: {org_reward}')
        return org_reward, 'SUCCESS'
    except Exception as err:
        logging.error(f'Exception get_reward: {err}')
        return 0, 'FAILED'
