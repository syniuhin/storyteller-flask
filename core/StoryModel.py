from neural import generate


class StoryModel(object):
  """
  Class for general model to generate stories about an image.
  """

  def __init__(self):
    self.z = None
    pass

  def load_model(self):
    self.z = generate.load_all()

  def is_loaded(self):
    return self.z is not None

  def generate_story(self, image_loc):
    if not self.is_loaded():
      raise ValueError('Model is not loaded!')
    return generate.story(self.z, image_loc)
