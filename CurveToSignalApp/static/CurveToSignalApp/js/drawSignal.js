
var canvas = document.getElementById("myCanvas");
var ctx = canvas.getContext("2d");
var points = [];
var dicPointsChecked = {"x": [], "y": []};

document.getElementById("BtnClearCanvas").addEventListener("click", clearCanvas); 



init();

function init(){
    
    clearCanvas();
    canvas.addEventListener("mousedown", startEventMouseMove); 
    canvas.addEventListener("mouseup", stopEventMouseMove); 
    ajaxSetup();
}


function startEventMouseMove(){
    
    clearCanvas();
    ctx.beginPath()
    ctx.moveTo(event.clientX, event.clientY);
    canvas.addEventListener("mousemove", drawLine);

}

function stopEventMouseMove(){
    canvas.removeEventListener("mousemove", drawLine);
    checkPoints();
    getPoints();
}


function ajaxSetup(){

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function drawLine(){
    var x = event.clientX;     // horizontal coordinate
    var y = event.clientY;     // vertical coordinate
    writeCoordinates(x,y);
    ctx.lineTo(x,y);
    ctx.stroke();
    points.push([x,y]);
}

function writeCoordinates(x,y){
    document.getElementById("xCoord").innerText = "X: " + x;
    document.getElementById("yCoord").innerText = "Y: " + y; 

}

// checks if x is monotonic inceasing
function checkPoints(){
    var xMax = 0;
    points.forEach(function(item, index, array) {
        x = item[0];
        if (x > xMax){
            xMax = x
            dicPointsChecked["x"].push(item[0])
            dicPointsChecked["y"].push(item[1])
        } 
    });
}

function getPoints(){
    parameters = {
        type: 'POST',
        url: '/CurveToSignalApp/get_points',
        data: dicPointsChecked,
        dataType: 'json',
        processData: 'true',
        success: function(data, textStatus, jqXHR) 
                {getCalculatedData(data, textStatus, jqXHR);},
        error: function(xhr,status,error){
                }
    }
    $.ajax(parameters);
}

function getCalculatedData(data, textStatus, jqXHR){

}

function clearCanvas(){
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}