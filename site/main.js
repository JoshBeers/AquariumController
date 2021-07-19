const socket = new WebSocket('ws://localhost:5000');

const sendMessage = () =>{
    console.log('sendMessage ' + document.getElementById('input').value)
    socket.send(document.getElementById('input').value);
}


socket.addEventListener('open', function(event){
    console.log('server connected');
});

socket.addEventListener('message', function(event) {
    console.log(event.data);
    document.getElementById('outUserLock').textContent = event.data;
});



