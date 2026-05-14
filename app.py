from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def home():
    return jsonify({
        "message": "Hello from Jenkins Pipeline!",
        "status": "running",
        "version": "1.0.0"
    })


@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200


@app.route('/info')
def info():
    return jsonify({
        "app": "jenkins-pipeline-demo",
        "description": "A simple Flask app deployed via Jenkins CI/CD pipeline",
        "author": "Aland Khalil"
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)