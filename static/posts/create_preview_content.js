$(document).ready(function () {

    var contentInput = $("#id_content");
    var md = window.markdownit();

    function setContent(value){
        var markedContent = md.render(value);
        console.log(value);
        console.log(markedContent);
        $("#preview-content").html(markedContent);
    }

    setContent(contentInput.val());

    contentInput.keyup(function () {
        var newContent = $(this).val();
        setContent(newContent);
        $("img").each(function () {
            $(this).addClass('img-responsive');
        })
    });

    var titleInput = $("#id_title");

    function setTitle(value){
        $("#preview-title").text(value);
    }

    setTitle(titleInput.val());

    titleInput.keyup(function () {
        var newTitle = $(this).val();
        setTitle(newTitle);
    })

});