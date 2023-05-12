from flask import Flask, render_template, request
import openai
import os 
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://oliviaflask:619150olivia@localhost/test_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

load_dotenv()

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_text = db.Column(db.Text, nullable=False)
    improved_text = db.Column(db.Text, nullable=False)

    def __init__(self, original_text, improved_text):
        self.original_text = original_text
        self.improved_text = improved_text

@app.route('/')
def index():
    return render_template('index.html')

openai.api_key = os.environ.get("OPENAI_API_KEY") 

@app.route('/improve_text', methods=['POST'])
def improve_text():
    original_text = request.form['original_text']

    # Use the OpenAI API to improve the text
    improved_text = call_openai_api(original_text)

    # Save the input and improved text to the database
    submission = Submission(original_text=original_text, improved_text=improved_text)
    db.session.add(submission)
    db.session.commit()

    return render_template('index.html', improved_text=improved_text)


def call_openai_api(original_text):
    prompt = f"Proofread and rephrase the following text in a professional tone: {original_text}"
    response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=150, n=1, stop=None, temperature=0)

    improved_text = response.choices[0].text.strip()
    return improved_text


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

