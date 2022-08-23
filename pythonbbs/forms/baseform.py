from wtforms import Form

class BaseForm(Form):
  @property
  def messages(self):
    message_list = []
    if self.errors:
      for errors in self.errors.values():
        message_list.extend(errors)
    return message_list