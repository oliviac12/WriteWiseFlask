import os
import pytest
from unittest.mock import Mock, patch
from app import app, db, Submission, call_openai_api


os.environ['DATABASE_URL'] = 'sqlite:///test.db'
os.environ['OPENAI_API_KEY'] = 'testkey'

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.app_context():
        return app.test_client()

# run before each test. It creates all the tables in the test database
def setup_function():
    with app.app_context():
        db.create_all()

# run after each test. that runs after each test function is done. It drops all tables and removes the session.
def teardown_function():
    db.session.remove()
    db.drop_all()

def test_improve_text(client):
    with patch('app.call_openai_api') as mock:
        mock.return_value = 'better text'
        response = client.post('/improve_text', data=dict(original_text='shitty text'), follow_redirects=True)
    assert b'better text' in response.data
    submission = Submission.query.first()
    assert submission is not None
    assert submission.original_text == 'shitty text'
    assert submission.improved_text == 'better text'

def test_call_openai_api():
    with app.app_context():
        with patch('openai.Completion.create') as mock:
            mock.return_value = Mock(choices=[Mock(text=' better text ')])
            result = call_openai_api('shitty text')
            mock.assert_called_once_with(
        engine="text-davinci-003", 
        prompt="Proofread and rephrase the following text in a professional tone: shitty text", 
        max_tokens=150, n=1, stop=None, temperature=0
    )
        assert result == 'better text'










