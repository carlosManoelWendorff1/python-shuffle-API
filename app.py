from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, DateTime, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from datetime import datetime

app = Flask(__name__)

# Database connection setup
db_username = "admin"
db_password = "12345678"
db_host = "shuffle.cno5zkhzwncl.us-east-2.rds.amazonaws.com"
db_name = "shuffle_database"
connection_string = f"mysql://{db_username}:{db_password}@{db_host}/{db_name}"
engine = create_engine(connection_string)
Base = declarative_base()
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Define the User model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(80), nullable=False)
    role = Column(String(20), nullable=False)
    created = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String(80))
    last_modified = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_modified_by = Column(String(80))

    def __init__(self, username, email, password, role, created_by):
        self.username = username
        self.email = email
        self.password = password
        self.role = role
        self.created_by = created_by
        self.last_modified_by = created_by

# Define the Post model
class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    last_modified_by = Column(String(80))
    last_modified = Column(DateTime)
    created_by = Column(String(80))
    created = Column(DateTime)
    content = Column(String(500))
    title = Column(String(100))

    def __init__(self, last_modified_by, created_by, content, title):
        self.last_modified_by = last_modified_by
        self.created_by = created_by
        self.content = content
        self.title = title

def user_to_dict(user):
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'password': user.password,
        'role': user.role,
        'created': user.created,
        'created_by': user.created_by,
        'last_modified': user.last_modified,
        'last_modified_by': user.last_modified_by
    }

def post_to_dict(post):
    return {
        'id': post.id,
        'last_modified_by': post.last_modified_by,
        'last_modified': post.last_modified,
        'created_by': post.created_by,
        'created': post.created,
        'content': post.content,
        'title': post.title
    }

# Create the database tables
Base.metadata.create_all(engine)
# CRUD routes for users
@app.route('/users', methods=['GET'])
def get_users():
    users = session.query(User).all()
    user_dicts = [user_to_dict(user) for user in users]
    return jsonify(user_dicts)

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if "username" in data and "email" in data and "password" in data and "role" in data:
        username = data["username"]
        email = data["email"]
        password = data["password"]
        role = data["role"]
        created_by = "admin"  # You can set the created_by user as needed
        user = User(username=username, email=email, password=password, role=role, created_by=created_by)
        session.add(user)
        session.commit()
        return jsonify(user_to_dict(user)), 201
    else:
        return "Missing data", 400

# CRUD routes for posts
@app.route('/posts', methods=['GET'])
def get_posts():
    posts = session.query(Post).all()
    post_dicts = [post_to_dict(post) for post in posts]
    return jsonify(post_dicts)

@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    if "content" in data and "title" in data:
        content = data["content"]
        title = data["title"]
        created_by = "admin"  # You can set the created_by user as needed
        post = Post(last_modified_by=created_by, created_by=created_by, content=content, title=title)
        session.add(post)
        try:
            session.commit()
            return jsonify(post_to_dict(post)), 201
        except IntegrityError as error:
            session.rollback()
            return "Invalid data", 400
    else:
        return "Missing data", 400
# Continue with update and delete routes for posts, if needed

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
