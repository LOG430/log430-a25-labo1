from ..daos.user_dao_mongo import UserDAOMongo
from ..daos.user_dao import UserDAO
from ..models.user import User
import pytest

@pytest.fixture(scope="module")
def setup_test_data():
    """Set up test data before running tests and clean up after"""
    dao = UserDAOMongo()
    
    # Clean up any existing data
    dao.delete_all()
    
    # Insert initial test data
    dao.insert(User(None, 'Ada Lovelace', 'alovelace@example.com'))
    dao.insert(User(None, 'Adele Goldberg', 'agoldberg@example.com'))
    dao.insert(User(None, 'Alan Turing', 'aturing@example.com'))
    
    yield dao
    
    # Clean up after tests
    dao.delete_all()
    dao.close()

def test_user_select(setup_test_data):
    dao = setup_test_data
    user_list = dao.select_all()
    assert len(user_list) >= 3

def test_user_insert(setup_test_data):
    dao = setup_test_data
    user = User(None, 'Margaret Hamilton', 'hamilton@example.com')
    dao.insert(user)
    user_list = dao.select_all()
    emails = [u.email for u in user_list]
    assert user.email in emails

def test_user_update(setup_test_data):
    dao = setup_test_data
    user = User(None, 'Charles Babbage', 'babage@example.com')
    assigned_id = dao.insert(user)

    corrected_email = 'babbage@example.com'
    user.id = assigned_id
    user.email = corrected_email

    dao.update(user)

    user_list = dao.select_all()
    emails = [u.email for u in user_list]
    assert corrected_email in emails

def test_user_delete(setup_test_data):
    dao = setup_test_data
    user = User(None, 'Douglas Engelbart', 'engelbart@example.com')
    assigned_id = dao.insert(user)
    dao.delete(assigned_id)

    user_list = dao.select_all()
    emails = [u.email for u in user_list]
    assert user.email not in emails