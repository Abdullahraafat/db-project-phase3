from flask import Flask, redirect, url_for
from routes.entry_classes import entry_bp
<<<<<<< HEAD
from routes.patrons import patrons_bp
=======
from routes.gatherings import gatherings_bp
from routes.venues import venues_bp
from routes.staff import staff_bp
>>>>>>> 3a7256cf99eebf80bc0bb6f7f7ccb8b5b9e56b24

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(entry_bp)
<<<<<<< HEAD
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
=======
app.register_blueprint(gatherings_bp)
app.register_blueprint(venues_bp)
app.register_blueprint(staff_bp)

# New Redirect Route
@app.route('/', strict_slashes=True)
def index():
    return redirect(url_for('gatherings.add_gathering_route'))
>>>>>>> 3a7256cf99eebf80bc0bb6f7f7ccb8b5b9e56b24

if __name__ == '__main__':
    app.run(debug=True)
