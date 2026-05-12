from flask import Flask, redirect, url_for
from routes.entry_classes import entry_bp
from routes.gatherings import gatherings_bp
from routes.venues import venues_bp
from routes.staff import staff_bp

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(entry_bp)
app.register_blueprint(gatherings_bp)
app.register_blueprint(venues_bp)
app.register_blueprint(staff_bp)

# New Redirect Route
@app.route('/', strict_slashes=True)
def index():
    return redirect(url_for('gatherings.add_gathering_route'))

if __name__ == '__main__':
    app.run(debug=True)
