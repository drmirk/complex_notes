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
