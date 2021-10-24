

$('#fb_1').click(function() {
    $('#filedrop_1').change(function() {
        let filename = $('#filedrop_1').val();
        console.log(1);
        $('#dli_1').css({'display':'flex'});
        $('#dli_1 span').html(filename);
    });
});​

$('#fb_2').click(function() {
    $('#filedrop_2').change(function() {
        let filename = $('#filedrop_2').val();
        console.log(2);
        $('#dli_2').css({'display':'flex'});
        $('#dli_2 span').html(filename);
    });
});​


// ВАЛИДАЦИЯ

let input = $('input[type="text"]');

input.change(function() {

    if (input.val() == '' || /\D+/.test(input.val()) || /^0/.test(input.val())){
        alert('Некорректный ввод данных')
    }
});