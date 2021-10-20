$(document).ready(function(){
    $('form').on('submit', function(event){
        $.ajax({
            data:{
                name: $('#name').val(),
                date_start: $('#date_start').val(),
                total_month: $('#total_month').val(),
                percent: $('#percent').val(),
                amount: $('#amount').val(),
                amount_value: $('#amount_value').val(),
            },
            type: 'POST',
            url: '/add-credit'
        }).done(function (data){
            var alert = $('#result-alert');
            if (data.error) {
                console.log("error")
                document.getElementById("result-alert").classList.add('alert-danger');
                alert.show();
                $('#result-text').text("Не удалось добавить кредит, попробуйте снова");
            }
            else {
                console.log("ok")
                document.getElementById("result-alert").classList.add('alert-success');
                alert.show();
                $('#result-text').text("Кредит успешно добавлен");
            }
        });
        event.preventDefault();
        $('#openModal').modal('hide');

    });
});