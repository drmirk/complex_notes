/* CKEDITOR code with customization for base.html */
CKEDITOR.replace('note_body', {
    extraPlugins: 'autogrow',
    autoGrow_onStartup: true,
    removePlugins: 'resize',
    filebrowserBrowseUrl: "{{ url_for('upload_file') }}",
    filebrowserUploadUrl: "{{ url_for('upload_file') }}",
    filebrowserWindowWidth: 100,
    filebrowserWindowHeight: 200,
    tabSpaces: 4,
    toolbar: [
        { name: 'tools', items: ['Maximize'] },
        { name: 'clipboard', items: ['Undo', 'Redo'] },
        { name: 'clipboard', items: ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord'] },
        { name: 'editing', items: ['SelectAll', '-', 'Find', 'Replace', '-', 'Scayt', 'AutoCorrect'] },
        { name: 'links', items: ['Link', 'Unlink', 'Anchor'] },
        { name: 'bidi', items: ['BidiLtr', 'BidiRtl'] },
        { name: 'insert', items: ['CodeSnippet', 'Image', 'Table', 'Smiley', 'SpecialChar'] },
        { name: 'insert', items: ['HorizontalRule', 'PageBreak'] },
        { name: 'insert', items: ['Blockquote', 'CreateDiv'] },
        { name: 'colors', items: ['TextColor', 'BGColor'] },
        { name: 'basicstyles', items: ['Bold', 'Italic', 'Underline'] },
        { name: 'basicstyles', items: ['Strike', 'Subscript', 'Superscript'] },
        { name: 'basicstyles', items: ['CopyFormatting', 'RemoveFormat'] },
        { name: 'paragraph', items: ['NumberedList', 'BulletedList'] },
        { name: 'paragraph', items: ['Outdent', 'Indent'] },
        { name: 'paragraph', items: ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-'] },
        { name: 'styles', items: ['Styles', 'Format', 'Font', 'FontSize'] },
    ],
});




$(document).ready(function () {
    /* If javascript is working, then new, save, delete buttons will be hidden */
    $('.hide_this').hide();

    /* convert Date object to a timestamp & add the timezone offset */
    var time_zone_offset = new Date().getTimezoneOffset() * 60000;

    /* Then convert time_zone_offset back to a date object, then run the toISOString(), then remove all seconds and miliseconds */
    function get_current_time() {
        return ((new Date(Date.now() - time_zone_offset)).toISOString().split('.')[0].slice(0,-3));
    };

    /* from json loads a note */
    function load_note() {
        /* $('#main_form').fadeOut(100); */
        var note_id = req.responseJSON['note_id'];
        current_note = note_id;
        var title = req.responseJSON['title'];
        var note_body = req.responseJSON['note_body'];
        var note_creation_date = req.responseJSON['note_creation_date'];
        var note_modification_date = req.responseJSON['note_modification_date'];
        $('#note_title').val(title);
        $('#note_creation_date').val(note_creation_date[0]);
        $('#note_modification_date').val(note_modification_date[0]);
        CKEDITOR.instances.note_body.setData(note_body);
        /* $('#main_form').fadeIn(500); */
    }

    /* AJAX to load note without completely refreshing page */
    $('.all_notes_class').on('click', '.notes', function (event) {
        event.preventDefault();
        var note_id = $(this).attr('id');
        req = $.ajax({
            url: "/only_note",
            method: 'POST',
            data: {'note_id': note_id}
        });
        req.done(load_note);
    });

    /* AJAX to load all notes of a section & latest modified note of that section without completely refreshing page */
    $('.all_sections_class').on('click', '.sections', function (event) {
        event.preventDefault();
        var section_id = $(this).attr('id');
        current_section = section_id;
        // gets all notes of a section and latest modified note
        req = $.ajax({
            url: "/only_section",
            method: 'POST',
            data: {'section_id': section_id}
        });
        req.done(function () {
            // load latest modified note or in case of empty show nothing
            load_note();
            // console.log(req.responseJSON["all_notes"][0]["title"]);
            // clear all notes from previous section
            $('.all_notes_class').empty();
            var all_notes = req.responseJSON["all_notes"]
            // if section has any note, then load them
            if (all_notes.length > 0) {
                $(all_notes).each(function () {
                    $('.all_notes_class').append("<div class='hover_choice notes' id=" + this['id'] + "><a href=/note/" + this['id'] + "><p class='note_title_gap'><strong>" + this['title'] + "</strong></p><p class='note_preview_gap horizontal_line'>" + this['preview'] + "</p></a></div>");
                });
            }

        });
    });

    /* AJAX to load all section of a notebook with all notes & latest modified note of that notebook without completely refreshing page */
    $('.all_notebooks_class').on('click', '.notebooks', function (event) {
        event.preventDefault();
        var notebook_id = $(this).attr('id');
        current_notebook = notebook_id;
        // get all sections of a notebook and latest modified note
        req = $.ajax({
            url: "/only_notebook",
            method: 'POST',
            data: {'notebook_id': notebook_id}
        });
        req.done(function () {
        // load latest modified note or in case of empty show nothing
            load_note();
            current_section = req.responseJSON['current_section'];
        // clear all notes & section from previous notebook
        $('.all_notes_class').empty();
        $('.all_sections_class').empty();
        var all_notes = req.responseJSON['all_notes']
        var all_sections = req.responseJSON['all_sections']
        // if notebook has any note, then load them
        if (all_notes.length > 0) {
            $(all_notes).each(function () {
                $('.all_notes_class').append("<div class='hover_choice notes' id=" + this['id'] + "><a href=/note/" + this['id'] + "><p class='note_title_gap'><strong>" + this['title'] + "</strong></p><p class='note_preview_gap horizontal_line'>" + this['preview'] + "</p></a></div>");
            });
        };
        // if notebook has any section, then load them
        if (all_sections.length > 0) {
            $(all_sections).each(function () {
                $('.all_sections_class').append("<div class='hover_choice sections' id=" + this['id'] + "><a href=/section/" + this['id'] + "><p class='horizontal_line'>" + this['title'] + "</p></a></div>");
            });
        };
        });
    });

    /* create a new notebook */
    $('#new_notebook_btn').on('click', function () {
        $('#new_notebook_modal').modal('toggle');
    });

    /* create a new notebook and redirect to that newly created notebook */
    $('#new_notebook_modal').on('click', '#new_notebook_title_btn', function () {
        var new_notebook_title = $('#new_notebook_title')['0'].value;
        var url = "/new_notebook/" + new_notebook_title;
        req = $.ajax({
            url: "/new_notebook",
            method: 'POST',
            data: {'new_notebook_title': new_notebook_title}
        });
        // console.log(req);
        req.done(function () {
            var new_notebook_id = req.responseJSON['new_notebook_id'];
            $('.all_notebooks_class').empty();
            var all_notebooks = req.responseJSON['all_notebooks'];
            if (all_notebooks.length > 0) {
                $(all_notebooks).each(function () {
                    $('.all_notebooks_class').append("<div class='hover_choice notebooks' id=" + this['id'] + "><a href=/notebook/" + this['id'] + "><p class='horizontal_line'>" + this['title'] + "</p></a></div>");
                });
            };
            current_notebook = new_notebook_id;
            $('.all_notebooks_class > .notebooks#' + new_notebook_id).click();
        });
        /* closes the modal, and empties the input field */
        $('#new_notebook_modal').modal('toggle');
        $('#new_notebook_title')['0'].value = '';
    });

    /* if no notebook, section won't be created */
    $('#new_section_btn').on('click', function () {
        if (current_notebook != -100) {
            $('#new_section_modal').modal('toggle');
        }
        else {
            $('#create_notebook_first_modal').modal('toggle');
            setTimeout(function(){
                $('#create_notebook_first_modal').modal('toggle')
              }, 1000);
        }
    });

    /* create a new section and redirect to that newly created section */
    $('#new_section_modal').on('click', '#new_section_title_btn', function () {
        var new_section_title = $('#new_section_title')['0'].value;
        req = $.ajax({
            url: '/new_section',
            method: 'POST',
            data: {'current_notebook': current_notebook, 'new_section_title': new_section_title}
        });
        req.done(function () {
            var new_section_id = req.responseJSON['new_section_id'];
            $('.all_sections_class').empty();
            var all_sections = req.responseJSON['all_sections'];
            if (all_sections.length > 0) {
                $(all_sections).each(function () {
                    $('.all_sections_class').append("<div class='hover_choice sections' id=" + this['id'] + "><a href=/section" + this['id'] + "><p class='horizontal_line'>" + this['title'] + "</p></a></div>");
                });
            };
            $('.all_sections_class > .sections#' + new_section_id).click();
        });
        /* closes the modal, and empties the input field */
        $('#new_section_modal').modal('toggle');
        $('#new_section_title')['0'].value = '';
    });

    /* create a new note */
    $('#new_note_btn').on('click', function () {
        if (current_section != -100) {
            current_note = 0;
            current_time = get_current_time();
            $('#note_title').val('');
            $('#note_creation_date').val(current_time);
            $('#note_modification_date').val(current_time);
            CKEDITOR.instances.note_body.setData('');
        }
        else {
            $('#create_section_first_modal').modal('toggle');
            setTimeout(function(){
                $('#create_section_first_modal').modal('toggle')
              }, 1000);
        }
    });

    /* automatically saves a note */
    function save_note() {
        var note_id = current_note;
        var parent_notebook = current_notebook;
        var parent_section = current_section;
        var note_title = $('#note_title').val();
        var note_body = CKEDITOR.instances.note_body.getData();
        var note_creation_date = $('#note_creation_date').val();
        var note_modification_date = $('#note_modification_date').val();
        var data = {
            'note_id': note_id,
            'note_title': note_title,
            'note_body': note_body,
            'note_creation_date': note_creation_date,
            'note_modification_date': note_modification_date,
            'parent_notebook': parent_notebook,
            'parent_section': parent_section
        };
        req = $.ajax({
            url: '/save_note',
            method: 'POST',
            data: data

        });
        req.done(function () {
            current_note = req.responseJSON['note_id']
        });
    };

    /* automatically saves notes after 30 seconds interval */
    window.setInterval(save_note, 30000)

});
