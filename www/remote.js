function uptimeCheck() {

    outputUptime.innerText = "";

    let url = "http://127.0.0.1:5000/uptime?uptime=secret";

    let xhr = new XMLHttpRequest();
    xhr.open("GET", url);

    xhr.onreadystatechange = function () {
    if (xhr.readyState === 4) {
          console.log(xhr.status);
          console.log(xhr.responseText);
          outputUptime.innerText = "\n" + xhr.responseText + "\n";
     }};

    xhr.send();

}

function dfCheck() {

    outputDF.innerText = "";
    
    let url = "http://127.0.0.1:5000/df?df=secret";

    let xhr = new XMLHttpRequest();
    xhr.open("GET", url);

    xhr.onreadystatechange = function () {
    if (xhr.readyState === 4) {
          console.log(xhr.status);
          console.log(xhr.responseText);
          outputDF.innerText = "\n" + xhr.responseText + "\n";
     }};

    xhr.send();

}

function pingCheck() {

    outputPing.innerText = "";

    let url = "http://127.0.0.1:5000/ping?ping=secret";

    let xhr = new XMLHttpRequest();
    xhr.open("GET", url);

    xhr.onreadystatechange = function () {
    if (xhr.readyState === 4) {
          console.log(xhr.status);
          console.log(xhr.responseText);
          outputPing.innerText = "\n" + xhr.responseText + "\n";
     }};

    xhr.send();

}

function dnsCheck() {

    outputDNS.innerText = "";
            
    let url = "http://127.0.0.1:5000/dnsLookup?dnsLookup=google.com";

    let xhr = new XMLHttpRequest();
    xhr.open("GET", url);

    xhr.onreadystatechange = function () {
    if (xhr.readyState === 4) {
          console.log(xhr.status);
          console.log(xhr.responseText);
          outputDNS.innerText = "\n" + xhr.responseText + "\n";
     }};

    xhr.send();

}

function currentUsageCheck() {

    outputCurrentUsage.innerText = "";
            
    let url = "http://127.0.0.1:5000/usage?usage=secret";

    let xhr = new XMLHttpRequest();
    xhr.open("GET", url);

    xhr.onreadystatechange = function () {
    if (xhr.readyState === 4) {
          console.log(xhr.status);
          console.log(xhr.responseText);
          outputCurrentUsage.innerText = "\n" + xhr.responseText + "\n";
     }};

    xhr.send();

}

window.onload = function() {
    var outputUptime = document.createElement('outputUptime');
    document.getElementById("selectionChoice1").appendChild(outputUptime);
    outputUptime.type = "text"; 
    outputUptime.id = "outputUptime";

    var outputDF = document.createElement('outputDF');
    document.getElementById("selectionChoice2").appendChild(outputDF);
    outputDF.type = "text"; 
    outputDF.id = "outputDF";

    var outputPing = document.createElement('outputPing'); 
    document.getElementById("selectionChoice3").appendChild(outputPing);
    outputPing.type = "text"; 
    outputPing.id = "outputPing";

    var outputDNS = document.createElement('outputDNS');
    document.getElementById("selectionChoice4").appendChild(outputDNS);
    outputDNS.type = "text"; 
    outputDNS.id = "outputDNS";

    var outputCurrentUsage = document.createElement('outputCurrentUsage');
    document.getElementById("selectionChoice5").appendChild(outputCurrentUsage);
    outputCurrentUsage.type = "text"; 
    outputCurrentUsage.id = "outputCurrentUsage";
}