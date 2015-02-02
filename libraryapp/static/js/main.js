function initJournal() {
    $('.like-box input[type="checkbox"]').click(function(event){
        var indicator = $('#ajax-progress-indicator');
        var box = $(this);

        $.ajax(box.data('url'), {
            'type': 'POST',
            'async': true,
            'dataType': 'json',
            'data': {
                'id': box.data('answer-id'),
                'estimate': box.is(':checked') ? '1': '',
                'question': box.data('question'),
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            'error': function(xhr, status, error){
                // alert(error);
                indicator.hide();
            },
            'success': function(data, status, xhr){
                alert('Спасибо за Вашу оценку');
                indicator.hide();
                document.location.reload (true);
            }
        });
    });
}

$(document).ready(function(){
    initJournal();
});
