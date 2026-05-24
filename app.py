from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api')
def api():
    
    data = ["Apple", "Banana", "Mango", "Litchi"]

    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)