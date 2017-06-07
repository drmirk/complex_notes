'''Import app object'''
from __init__ import *
'''Import flask objects'''
from flask import render_template, request, url_for, redirect


def note_button(note_form, single_note, parent_notebook, parent_section):
    if note_form.note_new_btn.data:
        return redirect(url_for('new_note_view',
                        parent_notebook=parent_notebook,
                        parent_section=parent_section))
    if note_form.note_save_btn.data:
        single_note.set_title(note_form.note_title.data)
        single_note.set_preview(note_form)
        single_note.set_body(note_form)
        single_note.set_creation_date(note_form)
        single_note.set_modification_date()
        db.session.commit()
        return None
    if note_form.note_delete_btn.data:
        if single_note is not None:
            db.session.delete(single_note)
            db.session.commit()
            return redirect(url_for('section_view', section_id=parent_section))


def section_button(section_form, parent_notebook, current_section, all_notes):
    if section_form.section_new_btn.data:
        if section_form.section_new_title.data.strip():
            section = Section()
            section.set_title(section_form.section_new_title.data)
            section.set_notebook_id(parent_notebook)
            db.session.add(section)
            db.session.commit()
            new_section_id = section.get_id()
            return redirect(url_for('section_view', section_id=new_section_id))
    if section_form.section_save_btn.data:
        if section_form.section_current_title.data.strip():
            current_section.set_title(section_form.section_current_title.data)
            db.session.commit()
            return None
    if section_form.section_delete_btn.data:
        if current_section is not None:
            for note in all_notes:
                db.session.delete(note)
            db.session.delete(current_section)
            db.session.commit()
            return redirect(url_for('notebook_view', notebook_id=parent_notebook))


def notebook_button(notebook_form, current_notebook, all_sections):
    if notebook_form.notebook_new_btn.data:
        if notebook_form.notebook_new_title.data.strip():
            notebook = Notebook()
            notebook.set_title(notebook_form.notebook_new_title.data)
            db.session.add(notebook)
            db.session.commit()
            new_notebook_id = notebook.get_id()
            return redirect(url_for('notebook_view', notebook_id=new_notebook_id))
    if notebook_form.notebook_save_btn.data:
        if notebook_form.notebook_current_title.data.strip():
            current_notebook.set_title(notebook_form.notebook_current_title.data)
            db.session.commit()
            return None
    if notebook_form.notebook_delete_btn.data:
        if current_notebook is not None:
            for section in all_sections:
                parent_section = section.get_id()
                all_notes = Note.query.filter_by(section_id=parent_section).order_by(Note.creation_date.desc()).all()
                for note in all_notes:
                    db.session.delete(note)
                db.session.delete(section)
            db.session.delete(current_notebook)
            db.session.commit()
            return redirect(url_for('notebook_view'))


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
    all_sections = Section.query.filter_by(notebook_id=parent_notebook).order_by(Section.title).all()
    return current_section, parent_notebook, all_sections


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


@app.route('/note/<int:note_id>', methods=['GET', 'POST'])
def note_view(note_id):
    '''this view is executed
    when a note is clicked'''
    single_note = Note.query.get_or_404(note_id)
    '''get all notes of a section from database in a descending order'''
    parent_section = single_note.get_section_id()
    all_notes = Note.query.filter_by(section_id=parent_section).order_by(Note.creation_date.desc()).all()
    '''get all sections from database'''
    current_section, parent_notebook, all_sections = get_all_sections(parent_section)
    '''get all notebooks from database'''
    current_notebook, notebooks = get_all_notebooks(parent_notebook)
    '''note button'''
    note_form = NotesForm()
    note_button_press = note_button(note_form, single_note, parent_notebook, parent_section)
    '''load note in from'''
    load_note_into_form(note_form, single_note)
    '''section button'''
    section_form = SectionForm()
    section_button_press = section_button(section_form, parent_notebook, current_section, all_notes)
    try:
        section_form.section_current_title.data = current_section.get_title()
    except:
        section_form.section_current_title.data = ''
    '''notebook button'''
    notebook_form = NotebookForm()
    notebook_button_press = notebook_button(notebook_form, current_notebook, all_sections)
    notebook_form.notebook_current_title.data = current_notebook.get_title()
    '''rendering note from database'''
    if note_button_press is not None:
        return note_button_press
    elif section_button_press is not None:
        return section_button_press
    elif notebook_button_press is not None:
        return notebook_button_press
    else:
        return (render_template('base.html', note_form=note_form,
                notebooks=notebooks, all_sections=all_sections, all_notes=all_notes,
                single_note=single_note, current_notebook=current_notebook,
                current_section=current_section, notebook_form=notebook_form,
                section_form=section_form))


@app.route('/section/<int:section_id>', methods=['GET', 'POST'])
def section_view(section_id):
    '''this view is executed
    when a section is clicked'''
    '''get all sections from database'''
    current_section, parent_notebook, all_sections = get_all_sections(section_id)
    '''get all notebooks from database'''
    current_notebook, notebooks = get_all_notebooks(parent_notebook)
    '''get all notes and a single note of a section
    from database in a descending order'''
    all_notes, single_note = get_all_and_single_notes(section_id)
    '''note button'''
    note_form = NotesForm()
    note_button_press = note_button(note_form, single_note, parent_notebook, section_id)
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
    section_button_press = section_button(section_form, parent_notebook, current_section, all_notes)
    try:
        section_form.section_current_title.data = current_section.get_title()
    except:
        section_form.section_current_title.data = ''
    '''notebook button'''
    notebook_form = NotebookForm()
    notebook_button_press = notebook_button(notebook_form, current_notebook, all_sections)
    notebook_form.notebook_current_title.data = current_notebook.get_title()
    '''rendering note from database'''
    if note_button_press is not None:
        return note_button_press
    elif section_button_press is not None:
        return section_button_press
    elif notebook_button_press is not None:
        return notebook_button_press
    else:
        return (render_template('base.html', note_form=note_form,
                notebooks=notebooks, all_sections=all_sections, all_notes=all_notes,
                single_note=single_note, current_notebook=current_notebook,
                current_section=current_section, notebook_form=notebook_form,
                section_form=section_form))


@app.route('/', methods=['GET', 'POST'])
@app.route('/notebook/<int:notebook_id>', methods=['GET', 'POST'])
def notebook_view(notebook_id=None):
    '''this view is executed
    when a notebook is clicked'''
    if notebook_id is None:
        single_note = Note.query.order_by(Note.modification_date.desc()).first()
        if single_note is None:
            current_notebook = Notebook.query.order_by(Notebook.title).first()
            if current_notebook is None:
                parent_notebook = None
                current_section = None
                parent_section = None
            else:
                parent_notebook = current_notebook.get_id()
                current_section = Section.query.filter_by(notebook_id=parent_notebook).order_by(Section.title).first()
            if current_section is None:
                parent_section = None
            else:
                parent_section = current_section.get_id()
        else:
            parent_notebook = single_note.get_notebook_id()
            current_notebook = Notebook.query.get_or_404(parent_notebook)
            parent_section = single_note.get_section_id()
            current_section = Section.query.get_or_404(parent_section)
    else:
        parent_notebook = notebook_id
        current_notebook = Notebook.query.get_or_404(parent_notebook)
        single_note = Note.query.filter_by(notebook_id=parent_notebook).order_by(Note.modification_date.desc()).first()
        if single_note is None:
            parent_section = None
        else:
            parent_section = single_note.get_section_id()
        if parent_section is None:
            current_section = Section.query.filter_by(notebook_id=parent_notebook).order_by(Section.title).first()
        else:
            current_section = Section.query.get_or_404(parent_section)
    all_notes = Note.query.filter_by(section_id=parent_section).order_by(Note.creation_date.desc()).all()
    all_sections = Section.query.filter_by(notebook_id=parent_notebook).order_by(Section.title).all()
    notebooks = Notebook.query.all()
    '''note button'''
    note_form = NotesForm()
    note_button_press = note_button(note_form, single_note, parent_notebook, parent_section)
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
    section_button_press = section_button(section_form, notebook_id, current_section, all_notes)
    try:
        section_form.section_current_title.data = current_section.get_title()
    except:
        section_form.section_current_title.data = ''
    '''notebook button'''
    notebook_form = NotebookForm()
    notebook_button_press = notebook_button(notebook_form, current_notebook, all_sections)
    try:
        notebook_form.notebook_current_title.data = current_notebook.get_title()
    except:
        notebook_form.notebook_current_title.data = ''
    '''rendering note from database'''
    if note_button_press is not None:
        return note_button_press
    elif section_button_press is not None:
        return section_button_press
    elif notebook_button_press is not None:
        return notebook_button_press
    else:
        return (render_template('base.html', note_form=note_form,
                notebooks=notebooks, all_sections=all_sections, all_notes=all_notes,
                single_note=single_note, current_notebook=current_notebook,
                current_section=current_section, notebook_form=notebook_form,
                section_form=section_form))


@app.route('/new_note/<int:parent_notebook>/<int:parent_section>', methods=['GET', 'POST'])
def new_note_view(parent_notebook, parent_section):
    '''view when creating a new note'''
    '''get all notes of a section from database in a descending order'''
    all_notes = Note.query.filter_by(section_id=parent_section).order_by(Note.creation_date.desc()).all()
    '''get all all_sections from database'''
    current_section, parent_notebook, all_sections = get_all_sections(parent_section)
    '''get all notebooks from database'''
    current_notebook, notebooks = get_all_notebooks(parent_notebook)
    '''note button'''
    note_form = NotesForm()
    if note_form.note_new_btn.data:
        return redirect(url_for('new_note_view',
                        parent_notebook=parent_notebook,
                        parent_section=parent_section))
    if note_form.note_save_btn.data:
        single_note = Note()
        single_note.set_title(note_form.note_title.data)
        single_note.set_preview(note_form)
        single_note.set_body(note_form)
        single_note.set_creation_date(note_form)
        single_note.set_modification_date()
        single_note.set_section_id(parent_section)
        single_note.set_notebook_id(parent_notebook)
        db.session.add(single_note)
        db.session.commit()
        new_note_id = single_note.get_id()
        return redirect(url_for('note_view', note_id=new_note_id))
    if note_form.note_delete_btn.data:
        pass
    note_form.note_creation_date.raw_data = current_time()
    note_form.note_modification_date.raw_data = current_time()
    '''section button'''
    section_form = SectionForm()
    section_button_press = section_button(section_form, parent_notebook, current_section, all_notes)
    try:
        section_form.section_current_title.data = current_section.get_title()
    except:
        section_form.section_current_title.data = ''
    '''notebook button'''
    notebook_form = NotebookForm()
    notebook_button_press = notebook_button(notebook_form, current_notebook, all_sections)
    notebook_form.notebook_current_title.data = current_notebook.get_title()
    '''rendering note from database'''
    if section_button_press is not None:
        return section_button_press
    elif notebook_button_press is not None:
        return notebook_button_press
    else:
        return (render_template('base.html', note_form=note_form,
                notebooks=notebooks, all_sections=all_sections, all_notes=all_notes,
                current_notebook=current_notebook,
                current_section=current_section, notebook_form=notebook_form,
                section_form=section_form))

