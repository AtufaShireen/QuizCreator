$(document).ready(function () {


    $('#add-form-row').click(function (ev) {
        console.log("pressed");
        ev.preventDefault();
        var count = $('#id_quizz_question-TOTAL_FORMS').val();
        console.log('forma', count);
        var tmplMarkup = $('#item-template').html();
        var compiledTmpl = tmplMarkup.replace(/__prefix__/g, count);
        $('div#items-form-container').append(compiledTmpl);

        $('#id_quizz_question-TOTAL_FORMS').val(parseInt(count) + 1);

    });


    $("input[type='checkbox']").click(function () {

        var n = $("input[class='remove-form']:checked").length;
        console.log('n here', n)

        $("input[class='remove-form']:checked").each(function () {

            // $(this).parents('.form-row').remove();
            console.log('removed');
        })
    })


});