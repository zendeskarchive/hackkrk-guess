import wtforms
from wtforms import validators

class UserForm(wtforms.Form):
    username = wtforms.TextField(validators=[validators.required()])
    password = wtforms.TextField(validators=[validators.required()])


class RiddleForm(wtforms.Form):
    question = wtforms.TextField(validators=[validators.required()])
    answer = wtforms.TextField(validators=[validators.required()])
    photo = wtforms.TextField(validators=[validators.required(),
                                          validators.length(max=1024 * 1024 * 5)])

class AttemptForm(wtforms.Form):
    answer = wtforms.TextField(validators=[validators.required()])

class PageForm(wtforms.Form):
    page = wtforms.IntegerField(default=1, validators=[
        validators.number_range(min=1)])
    per_page = wtforms.IntegerField(default=10, validators=[
        validators.number_range(min=1)])
