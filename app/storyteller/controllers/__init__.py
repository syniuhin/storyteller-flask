from app.storyteller.core import MockGenerator

from flask import Blueprint

story_model = MockGenerator()  # StoryModel()

storyteller = Blueprint('storyteller', __name__, url_prefix='/storyteller')
