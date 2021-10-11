let interval = 1500;
window.onload = getInfo();

function getInfo(){
    console.log(12345)
    $.ajax({
        method: 'POST',
        url: window.location.origin+'/refresh-portfolio',
        contentType: 'application/json',
        dataType: 'json',
        success:(data)=>{
            console.log(12)
            $('h1')[0].innerText=data['result'];
        },
        complete: function (){
            setTimeout(getInfo, interval);
        }
    });
}