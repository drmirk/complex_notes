'''Import app object'''
from __init__ import *
'''Import flask objects'''
from flask import render_template, request, url_for, redirect


def load_note_into_form(note_form, single_note):
    '''load note note_title, body, creation and modification date from database
    into the form object, so when rendering, this datas will be
    automatically loaded this could be also done from template
    but all logics only in the backend is more efficient'''
    note_form.note_title.data = single_note.get_title()
    note_form.note_body.data = single_note.get_body()
    note_form.note_creation_date.raw_data = single_note.get_creation_date()
    note_form.note_modification_date.raw_data = single_note.get_modification_date()


def get_all_sections(section_id):
    '''get all sections from database'''
    current_section = Section.query.get_or_404(section_id)
    parent_notebook = current_section.get_notebook_id()
    sections = Section.query.filter_by(notebook_id=parent_notebook).order_by(Section.title).all()
    return current_section, parent_notebook, sections


def get_all_notebooks(notebook_id):
    '''get all notebooks from database'''
    current_notebook = Notebook.query.get_or_404(notebook_id)
    notebooks = Notebook.query.all()
    return current_notebook, notebooks


def get_all_and_single_notes(section_id):
    '''get all notes of a section from database in a descending order'''
    all_notes = Note.query.filter_by(section_id=section_id).order_by(Note.creation_date.desc()).all()
    single_note = Note.query.filter_by(section_id=section_id).order_by(Note.modification_date.desc()).first()
    return all_notes, single_note


@app.route('/', methods=['GET', 'POST'])
@app.route('/<int:note_id>', methods=['GET', 'POST'])
def default_view(note_id=None):
    '''default view when app starts;
    also loading a note executes this view'''
    '''define a note form object'''
    note_form = NotesForm()
    '''if note_id is not given
    loads last modified note'''
    if note_id is None:
        single_note = Note.query.order_by(Note.modification_date.desc()).first()
    else:
        single_note = Note.query.get_or_404(note_id)
    '''load note in from'''
    load_note_into_form(note_form, single_note)
    '''get all notes of a section from database in a descending order'''
    parent_section = single_note.get_section_id()
    all_notes = Note.query.filter_by(section_id=parent_section).order_by(Note.creation_date.desc()).all()
    '''get all sections from database'''
    current_section, parent_notebook, sections = get_all_sections(parent_section)
    '''get all notebooks from database'''
    current_notebook, notebooks = get_all_notebooks(parent_notebook)
    '''section button'''
    section_form = SectionForm()
    if section_form.section_new_btn.data:
        section = Section()
        section.set_title(section_form.section_new_title.data)
        section.set_notebook_id(parent_notebook)
        db.session.add(section)
        db.session.commit()
        new_section_id = section.get_id()
        return redirect(url_for('section_view', section_id=new_section_id))
    try:
        section_form.section_current_title.data = current_section.get_title()
    except:
        section_form.section_current_title.data = ''
    '''notebook button'''
    notebook_form = NotebookForm()
    if notebook_form.notebook_new_btn.data:
        notebook = Notebook()
        notebook.set_title(notebook_form.notebook_new_title.data)
        db.session.add(notebook)
        db.session.commit()
        new_notebook_id = notebook.get_id()
        return redirect(url_for('notebook_view', notebook_id=new_notebook_id))
    if notebook_form.notebook_save_btn.data:
        current_notebook.set_title(notebook_form.notebook_current_title.data)
        db.session.commit()
    notebook_form.notebook_current_title.data = current_notebook.get_title()
    '''rendering note from database'''
    return (render_template('view_note.html', note_form=note_form,
            notebooks=notebooks, sections=sections, all_notes=all_notes,
            single_note=single_note, current_notebook=current_notebook,
            current_section=current_section, notebook_form=notebook_form,
            section_form=section_form))


@app.route('/section/<int:section_id>', methods=['GET', 'POST'])
def section_view(section_id):
    '''this view is executed
    when a section is clicked'''
    '''get all sections from database'''
    current_section, parent_notebook, sections = get_all_sections(section_id)
    '''get all notebooks from database'''
    current_notebook, notebooks = get_all_notebooks(parent_notebook)
    '''define a new form object'''
    note_form = NotesForm()
    '''get all notes and a single note of a section
    from database in a descending order'''
    all_notes, single_note = get_all_and_single_notes(section_id)
    if single_note is not None:
        load_note_into_form(note_form, single_note)
    else:
        '''when writing a new note, always set the creation date
        and modification date to current time
        btw creation date can be changed, but
        modification date can't be changed'''
        note_form.note_creation_date.raw_data = current_time()
        note_form.note_modification_date.raw_data = current_time()
    '''section button'''
    section_form = SectionForm()
    if section_form.section_new_btn.data:
        section = Section()
        section.set_title(section_form.section_new_title.data)
        section.set_notebook_id(parent_notebook)
        db.session.add(section)
        db.session.commit()
        new_section_id = section.get_id()
        return redirect(url_for('section_view', section_id=new_section_id))
    try:
        section_form.section_current_title.data = current_section.get_title()
    except:
        section_form.section_current_title.data = ''
    '''notebook button'''
    notebook_form = NotebookForm()
    if notebook_form.notebook_new_btn.data:
        notebook = Notebook()
        notebook.set_title(notebook_form.notebook_new_title.data)
        db.session.add(notebook)
        db.session.commit()
        new_notebook_id = notebook.get_id()
        return redirect(url_for('notebook_view', notebook_id=new_notebook_id))
    if notebook_form.notebook_save_btn.data:
        current_notebook.set_title(notebook_form.notebook_current_title.data)
        db.session.commit()
    notebook_form.notebook_current_title.data = current_notebook.get_title()
    '''rendering note from database'''
    return (render_template('view_note.html', note_form=note_form,
            notebooks=notebooks, sections=sections, all_notes=all_notes,
            single_note=single_note, current_notebook=current_notebook,
            current_section=current_section, notebook_form=notebook_form,
            section_form=section_form))


@app.route('/notebook/<int:notebook_id>', methods=['GET', 'POST'])
def notebook_view(notebook_id):
    '''this view is executed
    when a notebook is clicked'''
    '''get all notebooks from database'''
    current_notebook, notebooks = get_all_notebooks(notebook_id)
    '''get all sections of a notebook'''
    sections = Section.query.filter_by(notebook_id=notebook_id).order_by(Section.title).all()
    '''define a new form object'''
    note_form = NotesForm()
    if len(sections) == 0:
        all_notes = []
        single_note = None
        current_section = []
    else:
        '''get all notes and a single note of a section
        from database in a descending order'''
        section_id = Section.query.filter_by(notebook_id=notebook_id).order_by(Section.title).first().get_id()
        current_section = Section.query.get_or_404(section_id)
        all_notes, single_note = get_all_and_single_notes(section_id)
    if single_note is not None:
        load_note_into_form(note_form, single_note)
    else:
        '''when writing a new note, always set the creation date
        and modification date to current time
        btw creation date can be changed, but
        modification date can't be changed'''
        note_form.note_creation_date.raw_data = current_time()
        note_form.note_modification_date.raw_data = current_time()
    '''section button'''
    section_form = SectionForm()
    if section_form.section_new_btn.data:
        section = Section()
        section.set_title(section_form.section_new_title.data)
        section.set_notebook_id(notebook_id)
        db.session.add(section)
        db.session.commit()
        new_section_id = section.get_id()
        return redirect(url_for('section_view', section_id=new_section_id))
    try:
        section_form.section_current_title.data = current_section.get_title()
    except:
        section_form.section_current_title.data = ''
    '''notebook button'''
    notebook_form = NotebookForm()
    if notebook_form.notebook_new_btn.data:
        notebook = Notebook()
        notebook.set_title(notebook_form.notebook_new_title.data)
        db.session.add(notebook)
        db.session.commit()
        new_notebook_id = notebook.get_id()
        return redirect(url_for('notebook_view', notebook_id=new_notebook_id))
    if notebook_form.notebook_save_btn.data:
        current_notebook.set_title(notebook_form.notebook_current_title.data)
        db.session.commit()
    notebook_form.notebook_current_title.data = current_notebook.get_title()
    '''rendering note from database'''
    return (render_template('view_note.html', note_form=note_form,
            notebooks=notebooks, sections=sections, all_notes=all_notes,
            single_note=single_note, current_notebook=current_notebook,
            current_section=current_section, notebook_form=notebook_form,
            section_form=section_form))
