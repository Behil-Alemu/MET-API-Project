
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField,SelectField
from wtforms.validators import DataRequired, Email, Length


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    avatar = SelectField('Avatar',
    default=("https://gravatar.com/avatar/c128c36db79de723f1a5ac114704e211?s=400&d=robohash&r=x", "Avatar 0"),
    choices=[
        ('https://gravatar.com/avatar/9b516ce04785a4051f38b639649a14da?s=400&d=robohash&r=x', 'Avatar 1'), 
        ('https://gravatar.com/avatar/4380c6453db46121719005dd5e6f83dc?s=400&d=robohash&r=x', 'Avatar 2'), 
    ('https://gravatar.com/avatar/92405a3fcb1d8becb0cb5ba541ffe54d?s=400&d=robohash&r=x', 'Avatar 3'), 
    ('https://gravatar.com/avatar/86b415df66d63ce9961c57929b1026f7?s=400&d=robohash&r=x','Avatar 4')
    ]
    )

class UserEditForm(FlaskForm):
    """Form for editing profile"""
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    avatar = SelectField('Avatar',
    default=("https://gravatar.com/avatar/c128c36db79de723f1a5ac114704e211?s=400&d=robohash&r=x", "Avatar 0"),
    choices=[
        ('https://gravatar.com/avatar/9b516ce04785a4051f38b639649a14da?s=400&d=robohash&r=x', 'Avatar 1'), 
        ('https://gravatar.com/avatar/4380c6453db46121719005dd5e6f83dc?s=400&d=robohash&r=x', 'Avatar 2'), 
    ('https://gravatar.com/avatar/92405a3fcb1d8becb0cb5ba541ffe54d?s=400&d=robohash&r=x', 'Avatar 3'), 
    ('https://gravatar.com/avatar/86b415df66d63ce9961c57929b1026f7?s=400&d=robohash&r=x','Avatar 4')
    ]
    )
    social_media = StringField('(Optional) Social Media @')
    bio=StringField('(Optional) Bio')



class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


class PostForm(FlaskForm):
    """Post form."""

    title = StringField('Title:', validators=[DataRequired()])
    description = StringField('Description:', validators=[DataRequired()])
    imageURL = StringField('Your Art URL:', validators=[DataRequired()])

class EditPostForm(FlaskForm):
    """Post form."""

    title = StringField('Title:', validators=[DataRequired()])
    description = StringField('Description:', validators=[DataRequired()])
    imageURL = StringField('Your Art URL:', validators=[DataRequired()])

choices={
    1: "American Decorative Arts", 
    3: "Ancient Near Eastern Art",
    4: "Arms and Armor",
    5: "Arts of Africa, Oceania, and the Americas",
    6: "Asian Art",
    7: "The Cloisters",
    8: "The Costume Institute",
    9: "Drawings and Prints",
    10: "Egyptian Art",
    11: "European Paintings",
    12: "European Sculpture and Decorative Arts",
    13: "Greek and Roman Art",
    14: "Islamic Art",
    15: "The Robert Lehman Collection",
    16: "The Libraries",
    17: "Medieval Art",
    18: "Musical Instruments",
    19: "Photographs",
    21: "Modern Art"
}


 