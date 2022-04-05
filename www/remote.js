function loadFileAsText(){
    var fileToLoad = document.getElementById("fileToLoad").files[0];
  
    var fileReader = new FileReader();
    fileReader.onload = function(fileLoadedEvent){
        var textFromFileLoaded = fileLoadedEvent.target.result;
        //console.log(textFromFileLoaded);
        let serverString = textFromFileLoaded.split("\n");
        console.log(serverString);
        makeList(serverString);
        document.getElementById("selections").style.visibility="visible";
        document.getElementById("selections").style.display="block";
    };
  
    fileReader.readAsText(fileToLoad, "UTF-8");
  }


function makeList(serverStringParam){

    if (document.body.contains(document.getElementById("selectServer"))) {
        console.log("selectList exists");
        document.getElementById("selectServer").remove();
    }

    var selectList = document.createElement("select");
    selectList.id = "selectServer";
    document.body.appendChild(selectList);

    //Create and append the options
    for (var i = 0; i < serverStringParam.length; i++) {
        var option = document.createElement("option");
        option.value = serverStringParam[i];
        option.text = serverStringParam[i];
        selectList.appendChild(option);
    }

}

function uptimeCheck() {

    outputUptime.innerText = "";

    let url = "http://"+document.getElementById("selectServer").value+"/uptime?uptime=secret";

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
    
    let url = "http://"+document.getElementById("selectServer").value+"/df?df=secret";

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

    let url = "http://"+document.getElementById("selectServer").value+"/ping?ping=secret";

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
            
    let url = "http://"+document.getElementById("selectServer").value+"/dnsLookup?dnsLookup=google.com";

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
            
    let url = "http://"+document.getElementById("selectServer").value+"/usage?usage=secret";

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
    document.getElementById("selections").style.visibility="hidden";
    document.getElementById("selections").style.display="none";

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