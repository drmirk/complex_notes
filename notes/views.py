'''Import app object'''
from __init__ import *
'''Import flask objects'''
from flask import render_template, request, url_for, redirect, flash, jsonify


def note_button(note_form, single_note, parent_notebook, parent_section, create_new_note=False):
    if note_form.note_new_btn.data:
        if parent_notebook is None:
            flash('Create a Notebook & Section first!')
            return None
        if parent_section is None:
            flash('Create a Section first!')
            return None
        return redirect(url_for('new_note_view',
                        parent_notebook=parent_notebook,
                        parent_section=parent_section))
    if note_form.note_save_btn.data:
        if create_new_note:
            single_note = Note()
        elif single_note is None:
            return None
        title = note_form.note_title.data.strip()
        body = note_form.note_body.data.strip()
        if not title and not body:
            flash("Both Title and Body can't be empty!")
            return None
        single_note.set_preview(note_form)
        single_note.set_body(note_form)
        single_note.set_creation_date(note_form)
        single_note.set_modification_date()
        if not title:
            preview = single_note.get_preview()
            single_note.set_title(preview[:100])
        else:
            single_note.set_title(note_form.note_title.data)
        if create_new_note:
            single_note.set_section_id(parent_section)
            single_note.set_notebook_id(parent_notebook)
            db.session.add(single_note)
            db.session.commit()
            new_note_id = single_note.get_id()
            flash('Note saved successfully!')
            return redirect(url_for('note_view', note_id=new_note_id))
        db.session.commit()
        flash('Note saved successfully!')
        return None
    if note_form.note_delete_btn.data:
        if create_new_note:
            flash('Note deleted successfully!')
            return None
        if single_note is not None:
            db.session.delete(single_note)
            db.session.commit()
            flash('Note deleted successfully!')
            return redirect(url_for('section_view', section_id=parent_section))


def section_button(section_form, parent_notebook, current_section, all_notes):
    if section_form.section_new_btn.data:
        if parent_notebook is None:
            flash('Create a Notebook first!')
            return None
        if section_form.section_new_title.data.strip():
            section = Section()
            section.set_title(section_form.section_new_title.data)
            section.set_notebook_id(parent_notebook)
            db.session.add(section)
            db.session.commit()
            new_section_id = section.get_id()
            flash('Section created successfully!')
            return redirect(url_for('section_view', section_id=new_section_id))
        else:
            flash("Section name can't be empty!")
    if section_form.section_save_btn.data:
        if section_form.section_current_title.data.strip():
            current_section.set_title(section_form.section_current_title.data)
            db.session.commit()
            flash('Section renamed successfully!')
            return None
    if section_form.section_delete_btn.data:
        if current_section is not None:
            for note in all_notes:
                db.session.delete(note)
            db.session.delete(current_section)
            db.session.commit()
            flash('Section deleted successfully!')
            return redirect(url_for('notebook_view', notebook_id=parent_notebook))


def notebook_button(notebook_form, current_notebook, all_sections):
    if notebook_form.notebook_new_btn.data:
        if notebook_form.notebook_new_title.data.strip():
            notebook = Notebook()
            notebook.set_title(notebook_form.notebook_new_title.data)
            db.session.add(notebook)
            db.session.commit()
            new_notebook_id = notebook.get_id()
            flash('Notebook created successfully!')
            return redirect(url_for('notebook_view', notebook_id=new_notebook_id))
        else:
            flash("Notebook name can't be empty!")
    if notebook_form.notebook_save_btn.data:
        if notebook_form.notebook_current_title.data.strip():
            current_notebook.set_title(notebook_form.notebook_current_title.data)
            db.session.commit()
            flash('Notebook renamed successfully!')
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
            flash('Notebook deleted successfully')
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
    all_notebooks = Notebook.query.all()
    return current_notebook, all_notebooks


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
    current_notebook, all_notebooks = get_all_notebooks(parent_notebook)
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
                all_notebooks=all_notebooks, all_sections=all_sections, all_notes=all_notes,
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
    current_notebook, all_notebooks = get_all_notebooks(parent_notebook)
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
                all_notebooks=all_notebooks, all_sections=all_sections, all_notes=all_notes,
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
    all_notebooks = Notebook.query.all()
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
                all_notebooks=all_notebooks, all_sections=all_sections, all_notes=all_notes,
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
    current_notebook, all_notebooks = get_all_notebooks(parent_notebook)
    '''note button'''
    note_form = NotesForm()
    single_note = None
    create_new_note = True
    note_button_press = note_button(note_form, single_note, parent_notebook, parent_section, create_new_note)
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
                all_notebooks=all_notebooks, all_sections=all_sections, all_notes=all_notes,
                current_notebook=current_notebook,
                current_section=current_section, notebook_form=notebook_form,
                section_form=section_form))


@app.route('/only_note/<int:note_id>')
def only_note(note_id):
    '''this function returns only a single note'''
    single_note = Note.query.get_or_404(note_id)
    title = single_note.get_title()
    note_body = single_note.get_body()
    note_creation_date = single_note.get_creation_date()
    note_modification_date = single_note.get_modification_date()
    return jsonify({'result': 'success', 'title': title, 'note_body': note_body, 'note_creation_date': note_creation_date, 'note_modification_date': note_modification_date})


@app.route('/only_section/<int:section_id>')
def only_section(section_id):
    '''this function returns all notes of a section and latest modified note'''
    all_notes_models = Note.query.filter_by(section_id=section_id).order_by(Note.creation_date.desc()).all()
    single_note = Note.query.filter_by(section_id=section_id).order_by(Note.modification_date.desc()).first()
    all_notes = []
    for note in all_notes_models:
        temp = {}
        temp['id'] = note.get_id()
        temp['title'] = note.get_title()
        temp['preview'] = note.get_preview()
        all_notes.append(temp)
    if single_note is None:
        title = ''
        note_body = ''
        note_creation_date = ''
        note_modification_date = ''
    else:
        title = single_note.get_title()
        note_body = single_note.get_body()
        note_creation_date = single_note.get_creation_date()
        note_modification_date = single_note.get_modification_date()
    return jsonify({'result': 'success', 'title': title, 'note_body': note_body, 'note_creation_date': note_creation_date, 'note_modification_date': note_modification_date, 'all_notes': all_notes})


@app.route('/only_notebook/<int:notebook_id>')
def only_notebook(notebook_id):
    '''this function returns all sections of a notebook, latest modified note of that notebook and all sections'''
    parent_notebook = notebook_id
    single_note = Note.query.filter_by(notebook_id=parent_notebook).order_by(Note.modification_date.desc()).first()
    if single_note is None:
        title = ''
        note_body = ''
        note_creation_date = ''
        note_modification_date = ''
        parent_section = None
    else:
        title = single_note.get_title()
        note_body = single_note.get_body()
        note_creation_date = single_note.get_creation_date()
        note_modification_date = single_note.get_modification_date()
        parent_section = single_note.get_section_id()
    all_notes_models = Note.query.filter_by(section_id=parent_section).order_by(Note.creation_date.desc()).all()
    all_sections_models = Section.query.filter_by(notebook_id=parent_notebook).order_by(Section.title).all()
    all_notes = []
    for note in all_notes_models:
        temp = {}
        temp['id'] = note.get_id()
        temp['title'] = note.get_title()
        temp['preview'] = note.get_preview()
        all_notes.append(temp)
    all_sections = []
    for section in all_sections_models:
        temp = {}
        temp['id'] = section.get_id()
        temp['title'] = section.get_title()
        all_sections.append(temp)
    return jsonify({'return': 'success', 'title': title, 'note_body': note_body, 'note_creation_date': note_creation_date, 'note_modification_date': note_modification_date, 'all_notes': all_notes, 'all_sections': all_sections})


@app.route('/new_notebook/<new_notebook_title>')
def new_notebook(new_notebook_title):
        if new_notebook_title.strip():
            notebook = Notebook()
            notebook.set_title(new_notebook_title)
            db.session.add(notebook)
            db.session.commit()
            new_notebook_id = notebook.get_id()
            all_notebooks_models = Notebook.query.all()
            all_notebooks = []
            for notebook in all_notebooks_models:
                temp = {}
                temp['id'] = notebook.get_id()
                temp['title'] = notebook.get_title()
                all_notebooks.append(temp)
            return jsonify({'return': 'success', 'new_notebook_id': new_notebook_id, 'all_notebooks': all_notebooks})
