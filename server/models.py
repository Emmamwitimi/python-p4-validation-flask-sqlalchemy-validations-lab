from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates('name')
    def validate_name(self,key,name):
        existing_author = Author.query.filter_by(name=name).first()
        if not name:
            raise ValueError("Every author must have a name")

        if existing_author:
            raise ValueError("Author name must be unique")
        return name


    @validates('phone_number')
    def validate_phone_number(self,key,phone_number):
        if len(phone_number) != 10 :
            raise ValueError("Phone number must be exactly 10 digits long")

        if not phone_number.isdigit():
            raise ValueError("phone number must be in digits")
        return phone_number
    

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('content')
    def validate_len(self,key,content):
        if len(content) < 250:
            raise ValueError('Post content should be at least 250 characters long')
        return content

    @validates('summary')
    def validate_summary(self,key,summary):
        if len(summary) > 250:
            raise ValueError('Post summary should have a maximum of 250 characters.')
        return 
        
    @validates('category')
    def validate_category(self,key,category):
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError('category must either be fiction or non-fiction')
        return category

    @validates('title')
    def validate_title(self,key,title):
        title_phrases = ["Won't Believe",'Secret','Top','Guess']

        if  not any(phrase in title for phrase in title_phrases):
            raise ValueError("Title must contain one of the following: 'Won't Believe', 'Secret', 'Top', 'Guess'")
        return title

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
