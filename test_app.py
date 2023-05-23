import os
import pytest
from unittest.mock import Mock, patch
from app import app, db, Submission, call_openai_api


os.environ['DATABASE_URL'] = 'sqlite:///test.db'
os.environ['OPENAI_API_KEY'] = 'testkey'

@pytest.fixture(autouse=True)
def app_context():
    app.config['TESTING'] = True
    with app.app_context():
        print("/n 1")
        db.create_all()
        yield 
        print("2")
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client():
    yield app.test_client()

def test_improve_text(client):
    print("testing improve test")
    with patch('app.call_openai_api') as mock:
        mock.return_value = 'better text'
        response = client.post('/improve_text', data=dict(original_text='shitty text'), follow_redirects=True)
    assert b'better text' in response.data
    submission = Submission.query.first()
    assert submission is not None
    # assert submission.original_text == 'shitty text'
    # assert submission.improved_text == 'better text'

def test_call_openai_api():
    with patch('openai.Completion.create') as mock:
        mock.return_value = Mock(choices=[Mock(text=' better text ')])
        result = call_openai_api('shitty text')
        mock.assert_called_once_with(
            engine="text-davinci-003", 
            prompt="Proofread and rephrase the following text in a professional tone: shitty text", 
            max_tokens=150, n=1, stop=None, temperature=0
        )
        assert result == 'better text'

# if calling API for request, there's a mocking library for that 










