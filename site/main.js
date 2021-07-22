



const socket = new WebSocket('ws://localhost:5000');

//starts connectopm to websocket
socket.addEventListener('open', function(event){
    console.log('server connected');
});

//receives data from server
//parses json and sends to setData Method
socket.addEventListener('message', function(event) {
    console.log(JSON.parse(event.data));
    setData(JSON.parse(event.data));
});


//updates page with new data
//updates all data at once
const setData = (data) => {

    //get all html elements
    const displayFloatSensor  = document.getElementById('displayFloatSensor');
    const sumpFloatSensor = document.getElementById('sumpFloatSensor');
    const atoFloatSensor = document.getElementById('atoFloatSensor');
    const pumpSystemStatus =document.getElementById('pumpSystemStatus');
    //const pumpSystemStatusSwitch = document.getElementById('pumpSystemStatusSwitch');
    const mainPumpStatus = document.getElementById('mainPumpStatus');
   // const mainPumpStatusSwitch = document.getElementById('mainPumpStatusSwitch');
    const mainPumpLock = document.getElementById('mainPumpLock');
   // const mainPumpLockSwitch = document.getElementById('mainPumpLockSwitch');
    const atoSystemStatus = document.getElementById('atoSystemStatus');
  //  const atoSystemStatusSwitch = document.getElementById('atoSystemStatusSwitch');
    const atoPumpStatus = document.getElementById('atoPumpStatus');
   // const atoPumpStatusSwitch = document.getElementById('atoPumpStatusSwitch');
    const atoPumpLock = document.getElementById('atoPumpLock');
  //  const atoPumpLockSwitch = document.getElementById('atoPumpLockSwitch');

    //make sure there is data
    if(data != null){
        //updating sensors
        displayFloatSensor.textContent = (data.sensors.displayFloatSensorLevel==1);
        sumpFloatSensor.textContent = (data.sensors.sumpFloatSensorLevel==1);
        atoFloatSensor.textContent = (data.sensors.atoReservoirSensorLevel==1);

        //update pump system data
        pumpSystemStatus.textContent = (data.pumpController.status==1);
       // pumpSystemStatusSwitch.checked  =  (data.pumpController.status==1);
        mainPumpStatus.textContent  =  (data.pumpController.pump.status==1);
       // mainPumpStatusSwitch.checked  =  (data.pumpController.pump.status==1);
        mainPumpLock.textContent  =  (data.pumpController.pump.locked==1);
       // mainPumpLockSwitch.checked  =  (data.pumpController.pump.locked==1);

        //update ato data
        atoSystemStatus.textContent = (data.atoController.status==1);
        //atoSystemStatusSwitch.checked  =  (data.atoController.status==1);
        atoPumpStatus.textContent = (data.atoController.pump.status==1);
        //atoPumpStatusSwitch.checked  =  (data.atoController.pump.status==1);
        atoPumpLock.textContent = (data.atoController.pump.locked==1);
       // atoPumpLockSwitch.checked  =  (data.atoController.pump.locked==1);
    }
    toggleButtons(true)
}

//used by the toggle button for main pump system
function toggleMainPump(){
    socket.send('toggleMainPump')
    disablePumpButtons();
}

//used by the toggle button for main pump
function toggleMainPumpLock(){
    socket.send('toggleMainPumpLock')
    disablePumpButtons();
}

//used by the toggle button for main pump Lock
function togglePumpSystem(){
    socket.send('togglePumpSystem')
    disablePumpButtons();
}
//used by the toggle button for ATO system
function toggleATOSystem(){
    socket.send('toggleATOSystem')
    disableAtoButtons();
}

//used by the toggle button for ATO pump 
function toggleATOPump(){
    socket.send('toggleATOPump')
    disableAtoButtons();
}

//used by the toggle button for ATO pump Lock
function toggleATOPumpLock(){
    socket.send('toggleATOPumpLock')
    disableAtoButtons();
}

//used to disable or enable all class toggle buttons
function toggleButtons(tog){
    buttons = document.getElementsByClassName('toggle');

    for(var x =0;x <buttons.length; x++){
        buttons[x].disabled = !tog;
    }
}

//used to disable buttons of class pumpButton
function disablePumpButtons(){
    buttons = document.getElementsByClassName('pumpButton');

    for(var x =0;x <buttons.length; x++){
        buttons[x].disabled = !tog;
    }
}

//used to disable buttons of class atoButton
function disableAtoButtons(){
    buttons = document.getElementsByClassName('atoButton');

    for(var x =0;x <buttons.length; x++){
        buttons[x].disabled = !tog;
    }
}


