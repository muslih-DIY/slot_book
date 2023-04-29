import pytest
import json
import os

TEST_DATA_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)),'data')


def get_test_data(filename)->dict:
    filepath = os.path.join(TEST_DATA_FOLDER,filename)
    
    with open(filepath,encoding='utf-8') as jsonfile:
        data = json.load(jsonfile)
    return data

@pytest.fixture    
def get_container()->dict:
    data:dict = get_test_data('containers.json')
    return data

@pytest.fixture    
def get_campaign()->dict:
    data:dict = get_test_data('obdcampaign.json')
    return data