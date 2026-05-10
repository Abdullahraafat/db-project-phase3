from flask import Flask, render_template
from routes.gatherings import gatherings_bp  # Adjust path as needed
from routes.venues import venues_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(gatherings_bp)
app.register_blueprint(venues_bp)

@app.route('/')
def index():
    return render_template('index.html')  # Make sure this exists

if __name__ == '__main__':
    app.run(debug=True)

