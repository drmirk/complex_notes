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

/* AJAX to load note without completely refreshing page */
$(document).ready(function(){
    // $('.all_notes_class').on('click', '.single_notes', function (event) {
    $('.single_notes').on('click', function (event) {
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
});

/* AJAX to load all notes of a section & latest modified note of that section without completely refreshing page */
 $(document).ready(function(){
    $('.sections').on('click', function (event) {
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
                    $('.all_notes_class').append("<div class='hover_choice single_notes' id=" + this['id'] + "><a href=/note/" + this['id'] + "><p class='note_title_gap'><strong>" + this['title'] + "</strong></p><p class='note_preview_gap horizontal_line'>" + this['preview'] + "</p></a></div>");
                });
            }

        });
	});
});
