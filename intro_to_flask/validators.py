from wtforms.validators import ValidationError

class Unique(object):
  def __init__(self, model, field, message=None):
    print "in Unique __init__"
    self.model = model
    self.field = field
    if not message:
      message = 'This element already exists.'
    self.message = message

  def __call__(self, form, field):
    print "in Unique __call__"
    check = self.model.query.filter(self.field == field.data).first()
    print field.data
    print self.field
    print check.project_name
    if check:
      raise ValidationError(self.message)
