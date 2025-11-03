from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

# --- Database Configuration ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- Initialize Database ---
db = SQLAlchemy(app)

#create a model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def to_dict(self):
        return {"id":self.id,"name":self.name,"email":self.email}
    
# --- Create DB Tables ---
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return "Flask Server Running!"

@app.route('/api/users',methods=['POST'])
def create_user():
    data=request.get_json()
    new_user=User(name=data['name'],email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message":"User added"}),201

@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

# Get user by ID (GET)
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict())

# Delete user (DELETE)
@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully!"})  

if __name__ == '__main__':
    app.run(debug=True)