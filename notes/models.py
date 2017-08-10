'''Import SQLALchemy for database/model'''
from flask_sqlalchemy import SQLAlchemy

'''Regular expression to remove html tags from a text'''
import re

'''To store/retrieve datetime in/from database'''
from datetime import datetime


'''sqlalchemy database object'''
db = SQLAlchemy()


def remove_tags(text):
    '''remove all html tag from a text'''
    TAG_REMOVE = re.compile(r'<[^>]+>')
    return TAG_REMOVE.sub('', text)


def current_time():
    '''returns current time in a list, in a formatted way
    which can be used in the wtform'''
    time = []
    time.append(datetime.now().strftime('%Y-%m-%d %H:%M').replace(' ', 'T'))
    return time


class Notebook(db.Model):
    '''sqlalchemy model for notebooks'''
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String())
    sections = db.relationship('Section', backref='notebook', lazy='dynamic')
    notes = db.relationship('Note', backref='notebook', lazy='dynamic')

    def get_id(self):
        '''returns id of a notebook'''
        return self.id

    def get_title(self):
        '''returns title of a notebook'''
        return self.title

    def set_title(self, title):
        '''set title of a notebook'''
        self.title = title

    def __repr__(self):
        return "<Notebook {}>".format(self.title)


class Section(db.Model):
    '''sqlalchemy model for sections'''
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String())
    notes = db.relationship('Note', backref='section', lazy='dynamic')
    notebook_id = db.Column(db.Integer(), db.ForeignKey('notebook.id'))

    def get_id(self):
        '''returns id of a section'''
        return self.id

    def get_title(self):
        '''returns title of a section'''
        return self.title

    def set_title(self, title):
        '''set title of a section'''
        self.title = title

    def get_notebook_id(self):
        '''returns parent notebook's id of a section'''
        return self.notebook_id

    def set_notebook_id(self, notebook_id):
        '''set parent of a section'''
        self.notebook_id = notebook_id

    def __repr__(self):
        return "<Section {}>".format(self.title)


class Note(db.Model):
    '''sqlalchemy model to represent database table'''
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String())
    preview = db.Column(db.String())
    body = db.Column(db.String())
    creation_date = db.Column(db.DateTime())
    modification_date = db.Column(db.DateTime())
    section_id = db.Column(db.Integer(), db.ForeignKey('section.id'))
    notebook_id = db.Column(db.Integer(), db.ForeignKey('notebook.id'))

    def get_id(self):
        '''returns id of a note'''
        return self.id

    def get_title(self):
        '''returns title of a note'''
        return self.title

    def set_title(self, title):
        '''set title of a note'''
        self.title = title

    def get_preview(self):
        '''returns first 300 char of a note'''
        return self.preview

    '''takes form object
    then takes the note_body and removes all html tags
    stores first 300 character'''
    def set_preview(self, form, auto_save_js=False, note_body_js=None):
        '''set preview of a note'''
        if auto_save_js:
            preview = remove_tags(note_body_js)
        else:
            preview = remove_tags(form.note_body.data)
        self.preview = preview[:300]

    def get_body(self):
        '''returns main body of a note'''
        return self.body

    def set_body(self, form, auto_save_js=False, note_body_js=None):
        '''sets body of a note'''
        if auto_save_js:
            self.body = note_body_js
        else:
            self.body = form.note_body.data

    '''wtform datetime only accepts a list
    containing only 1 item in a specific format
    so we get the time from database, format it accordingly
    the use this function to display in the browser'''
    def get_creation_date(self):
        '''returns creation time in a formatted way,
        so html datetime can use that'''
        time = []
        time.append(self.creation_date.strftime('%Y-%m-%d %H:%M').replace(' ', 'T'))
        return time

    '''wtform datetime returns datetime like a normal datetime form field, in a list
    using raw_data we are getting the list
    and formatting that accordingly to store in database'''
    def set_creation_date(self, form, auto_save_js=False, note_creation_date_js=None):
        '''gets creation time in a html format,
        & formats and sets that in db'''
        if auto_save_js:
            time = note_creation_date_js.replace('T', ' ')
        else:
            time = form.note_creation_date.raw_data[0].replace('T', ' ')
        self.creation_date = datetime.strptime(time, '%Y-%m-%d %H:%M')

    '''wtform datetime only accepts a list
    containing only 1 item in a specific format
    so we get the time from database, format it accordingly
    the use this function to display in the browser'''
    def get_modification_date(self):
        '''returns modification time in a formatted way,
        so html datetime can use that'''
        time = []
        time.append(self.modification_date.strftime('%Y-%m-%d %H:%M').replace(' ', 'T'))
        return time

    '''current saving time will be set as modification date
    and users cant change it.'''
    def set_modification_date(self):
        '''sets current time as mdification time'''
        self.modification_date = datetime.now()

    def get_section_id(self):
        '''returns parent id of a note'''
        return self.section_id

    def set_section_id(self, section_id):
        '''sets parent id of a note'''
        self.section_id = section_id

    def get_notebook_id(self):
        '''returns notebook id of that note'''
        return self.notebook_id

    def set_notebook_id(self, notebook_id):
        '''sets notebook id of a note'''
        self.notebook_id = notebook_id

    def __repr__(self):
        return "<Note {}>".format(self.title)
