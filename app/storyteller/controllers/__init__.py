from flask import Blueprint

from app.storyteller.core import StoryGenerator

story_model = StoryGenerator()

storyteller = Blueprint('storyteller', __name__, url_prefix='/storyteller')
