from flask import Flask, redirect, url_for
from routes.gatherings import gatherings_bp
from routes.venues import venues_bp


app = Flask(__name__)

# Register blueprints
app.register_blueprint(gatherings_bp)
app.register_blueprint(venues_bp)

@app.route('/', strict_slashes=True)
def index():
    return redirect(url_for('gatherings.add_gathering_route'))

if __name__ == '__main__':
    app.run(debug=True)

