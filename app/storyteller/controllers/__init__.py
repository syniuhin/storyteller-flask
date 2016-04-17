from flask import Blueprint

from app.storyteller.core import MockGenerator

story_model = MockGenerator()  # StoryGenerator()

storyteller = Blueprint('storyteller', __name__, url_prefix='/storyteller')
