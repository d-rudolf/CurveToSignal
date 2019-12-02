
"use strict";
var canvas = document.getElementById("myCanvas");
var ctx = canvas.getContext("2d");
var points = [];
var dicPointsChecked = {"x": [], "y": []};
var chart;
var chartData;
var calcData;

document.getElementById("BtnClearCanvas").addEventListener("click", clearCanvas); 
document.getElementById("BtnExportData").addEventListener("click", exportData); 


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
    points.push([x,canvas.height-y]);
}

function writeCoordinates(x,y){
    document.getElementById("xCoord").innerText = "X: " + x;
    document.getElementById("yCoord").innerText = "Y: " + y; 

}

// checks if x is monotonic inceasing
function checkPoints(){
    var xMax = 0;
    points.forEach(function(item, index, array) {
        var x = item[0];
        if (x > xMax){
            xMax = x
            dicPointsChecked["x"].push(item[0])
            dicPointsChecked["y"].push(item[1])
        } 
    });
}

function getPoints(){
    var parameters = {
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
    calcData = data
    prepareData(data);
    initChart();
    plotChart();
}

function prepareData(data){

    chartData = [{ values: prepareXY(data.adX, data.adY),
                   key:    'input',
                   color:  '#ff7f0e'
                 },
                 { values: prepareXY(data.adX, data.adYCalc_real),
                   key:    'calculated',
                   color:  '#7777ff'
                 }]; 
}

function prepareXY(adX, adY){
    var adXY = [];
    for (var i = 0; i < adX.length; i++) {
        adXY.push({x: adX[i], y: adY[i]});
    }
    return adXY;
}

function plotChart(){
    nv.addGraph(function() {
        d3.select('#svgSignal')   
          .datum(chartData)        
          .call(chart);         
        //Update the chart when window resizes.
        nv.utils.windowResize(function() { chart.update() });
        return chart;
    });
}

function initChart(){
    chart = nv.models.lineChart()
                .margin({left: 100})  //Adjust chart margins to give the x-axis some breathing room.
                .useInteractiveGuideline(true)  //We want nice looking tooltips and a guideline!
                //.transitionDuration(350)  //how fast do you want the lines to transition?
                .showLegend(true)       //Show the legend, allowing users to turn on/off line series.
                .showYAxis(true)        //Show the y-axis
                .showXAxis(true);        //Show the x-axis
    chart.xAxis     
         .axisLabel('x')
         .tickFormat(d3.format(',r'));
    chart.yAxis     
         .axisLabel('y')
         .tickFormat(d3.format('.02f'));
}

function clearCanvas(){
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

function exportData(){
    var dataStr = JSON.stringify(calcData.adYCalc_real)
    var dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
    var exportFileDefaultName = 'CurveToSignal.json';
    var linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
}