from flask import Flask
from routes.entry_classes import entry_bp
from routes.patrons import patrons_bp

app = Flask(__name__)

app.register_blueprint(entry_bp)
app.register_blueprint(patrons_bp)

@app.route('/')
def home():

    return """
    <h1>Gathering System</h1>

    <a href='/add_entry_class'>
        Add Entry Class
    </a>

    <br><br>

    <a href='/update_entry_class'>
        Update Entry Class
    </a>

    <br><br>
     <a href='/register_patron'>
        Register Patron
    </a>

    <br><br>

    <a href='/purchase_pass'>
        Purchase Pass
    </a>

    <br><br>

    <a href='/inquiry1'>
        Inquiry 1
    </a>

    <br><br>

    <a href='/inquiry5'>
        Inquiry 5
    </a>
    """

if __name__ == '__main__':
    app.run(debug=True)