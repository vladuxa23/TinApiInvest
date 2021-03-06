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
                document.getElementById("result-alert").classList
                    .add('alert-danger');
                alert.show();
                $('#result-text').text("Не удалось добавить кредит, " +
                    "попробуйте снова");
            }
            else {
                console.log("ok")
                document.getElementById("result-alert").classList
                    .add('alert-success');
                alert.show();
                $('#result-text').text("Кредит успешно добавлен");
            }
        });
        event.preventDefault();
        $('#openModal').modal('hide');
        $('body').removeClass('modal-open');
        $('.modal-backdrop').remove();

    });
});

$('#date_start').datepicker({
    format: "dd.mm.yyyy",
    weekStart: 0,
    clearBtn: true,
    language: "ru",
    autoclose: true,
    todayHighlight: true
});

$('#openModal').on('hidden.bs.modal', function () {
    $(this).find('form').trigger('reset');
})

$(document).on('keydown', 'input[pattern]', function(e){
  var input = $(this);
  var oldVal = input.val();
  var regex = new RegExp(input.attr('pattern'), 'g');

  setTimeout(function(){
    var newVal = input.val();
    if(!regex.test(newVal)){
      input.val(oldVal);
    }
  }, 1);
});