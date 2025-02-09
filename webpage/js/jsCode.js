/* functionality behind changing the preview image on the landing page */
function loadRandomPreview() {
    let rnd = Math.floor(20*Math.random());
    let functionType = document.getElementById("previewFunctionSelect").value;
    let path = "../../images/samples/" + functionType + "/sample_" + rnd + ".png";
    document.getElementById("imagePreview").src = path;
}

/* create the header element */
function createHeader() {
    const headerObj = document.createElement("header");
    headerObj.id = "cmnHeader";
    document.body.insertBefore(headerObj, document.body.firstChild)
    document.getElementById("cmnHeader").innerHTML = "<h1> Abstract Computer Art by Continued Functions </h1>";
    document.getElementById("cmnHeader").innerHTML += "<div id = 'headerNavDiv'></div>";
    document.getElementById("headerNavDiv").innerHTML += "<a class='headerBtn' href='main.html'> Home </a>";
    document.getElementById("headerNavDiv").innerHTML += "<a class='headerBtn' href='gallery.html'> Gallery </a>";
    document.getElementById("headerNavDiv").innerHTML += "<a class='headerBtn' href='theory.html'> Theory </a>";
    document.getElementById("headerNavDiv").innerHTML += "<a class='headerBtn' href='create.html'> Create </a>";
}

createHeader();

/* create the footer element */
function createFooter() {
    const footerObj = document.createElement("footer");
    footerObj.id = "cmnFooter";
    document.body.insertBefore(footerObj, document.body.lastChild);
    document.getElementById("cmnFooter").innerHTML = "<hr/>";
    document.getElementById("cmnFooter").innerHTML += "<p> I am a footer! I contain a subscribe link (newsletter), a darkmode switch, ... </p>";
}
createFooter();
