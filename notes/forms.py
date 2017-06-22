'''Get the user inputs using flask-wtf instead of directly using html form objects.
HTML5 datetime field provides a calender to easily choose date'''
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.fields.html5 import DateTimeLocalField


class NotesForm(FlaskForm):
    '''using flask-wtf to create a
    form class for notes'''
    note_title = TextAreaField()
    note_body = TextAreaField()
    note_creation_date = DateTimeLocalField()
    note_modification_date = DateTimeLocalField()
    note_new_btn = SubmitField()
    note_save_btn = SubmitField()
    note_delete_btn = SubmitField()


class NotebookForm(FlaskForm):
    '''using flask-wtf to create a
    form class for notebooks'''
    notebook_current_title = StringField()
    notebook_new_title = StringField()
    notebook_new_btn = SubmitField()
    notebook_save_btn = SubmitField()
    notebook_delete_btn = SubmitField()


class SectionForm(FlaskForm):
    '''using flask-wtf to create a
    form class for sections'''
    section_current_title = StringField()
    section_new_title = StringField()
    section_new_btn = SubmitField()
    section_save_btn = SubmitField()
    section_delete_btn = SubmitField()
