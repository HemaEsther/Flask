from flask import Flask, jsonify, request

# create flask app
app = Flask(__name__)

# create a route
@app.route('/')
def home():
    return "Flask Server is Running!"

@app.route('/api/hello',methods=['GET'])
def say_hello():
    return jsonify({"message": "Hello from Flask API!"})

@app.route('/api/greet',methods=['POST'])
def greet_user():
    data=request.get_json()
    name=data.get("name","Guest")
    return jsonify({"greeting": f"Hello, {name}!"})

#Run server
if __name__ == '__main__':
    app.run(debug=True)