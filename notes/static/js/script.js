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

    /* AJAX to load note without completely refreshing page */
    $('.all_notes_class').on('click', '.notes', function (event) {
        event.preventDefault();
        var note_id = $(this).attr('id');
        url = "/only_note/" + note_id
        req = $.ajax({
            url: url,
            method: 'GET'
        });
        req.done(function () {
            /* $('#main_form').fadeOut(100); */
            var title = req.responseJSON['title'];
            var note_body = req.responseJSON['note_body'];
            var note_creation_date = req.responseJSON['note_creation_date'];
            var note_modification_date = req.responseJSON['note_modification_date'];
            $('#note_title').val(title);
            $('#note_creation_date').val(note_creation_date[0]);
            $('#note_modification_date').val(note_modification_date[0]);
            CKEDITOR.instances.note_body.setData(note_body);
            /* $('#main_form').fadeIn(500); */
        });
    });

    /* AJAX to load all notes of a section & latest modified note of that section without completely refreshing page */
    $('.all_sections_class').on('click', '.sections', function (event) {
        event.preventDefault();
        var section_id = $(this).attr('id');
        url = "/only_section/" + section_id;
        // gets all notes of a section and latest modified note
        req = $.ajax({
            url: url,
            method: 'GET'
        });
        req.done(function () {
            // load latest modified note or in case of empty show nothing
            var title = req.responseJSON['title'];
            var note_body = req.responseJSON['note_body'];
            var note_creation_date = req.responseJSON['note_creation_date'];
            var note_modification_date = req.responseJSON['note_modification_date'];
            $('#note_title').val(title);
            $('#note_creation_date').val(note_creation_date[0]);
            $('#note_modification_date').val(note_modification_date[0]);
            CKEDITOR.instances.note_body.setData(note_body);
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
        var url = "/only_notebook/" + notebook_id;
        // get all sections of a notebook and latest modified note
        req = $.ajax({
            url: url,
            method: 'GET'
        });
        req.done(function () {
        // load latest modified note or in case of empty show nothing
        var title = req.responseJSON['title'];
        var note_body = req.responseJSON['note_body'];
        var note_creation_date = req.responseJSON['note_creation_date'];
        var note_modification_date = req.responseJSON['note_modification_date'];
        $('#note_title').val(title);
        $('#note_creation_date').val(note_creation_date[0]);
        $('#note_modification_date').val(note_modification_date[0]);
        CKEDITOR.instances.note_body.setData(note_body);
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

    /* create a new notebook and redirect to that newly created notebook */
    $('#new_notebook_modal').on('click', '#new_notebook_title_btn', function () {
        var new_notebook_title = $('#new_notebook_title')['0'].value;
        var url = "/new_notebook/" + new_notebook_title;
        req = $.ajax({
            url: url,
            method: 'GET'
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
            $('.all_notebooks_class > .notebooks#' + new_notebook_id).click();
        });
        /* closes the modal, and empties the input field */
        $('#new_notebook_modal').modal('toggle');
        $('#new_notebook_title')['0'].value = '';
    });

    /* create a new section and redirect to that newly created section */
    $('#new_section_modal').on('click', '#new_section_title_btn', function () {
        var new_section_title = $('#new_section_title')['0'].value;
        req = $.ajax({
            url: '/new_section',
            method: 'POST',
            data: {'current_notebook': current_notebook, 'new_section_title': new_section_title}
        });
        console.log(req);
        /* closes the modal, and empties the input field */
        $('#new_section_modal').modal('toggle');
        $('#new_section_modal')['0'].value = '';
    });




});
