
from flask import Flask, render_template
from routes.venues import venues_bp
from routes.gatherings import gatherings_bp
from routes.entry_classes import entry_bp
from routes.patrons import patrons_bp
from routes.staff import staff_bp

app = Flask(__name__)

app.register_blueprint(venues_bp)
app.register_blueprint(gatherings_bp)
app.register_blueprint(entry_bp)
app.register_blueprint(patrons_bp)
app.register_blueprint(staff_bp)

@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)