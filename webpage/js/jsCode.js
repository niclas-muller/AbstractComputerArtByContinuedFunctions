/* load common elements (stylesheet,etc.) into head */

function fillHtmlHead() {
    let styleSheetInclude = document.createElement('link');
    styleSheetInclude.rel = 'stylesheet';
    styleSheetInclude.href =  '../css/styles.css';
    document.head.appendChild(styleSheetInclude);

    let favIconInclude = document.createElement('link');
    favIconInclude.rel = 'icon';
    favIconInclude.type = 'image/x-icon';
    favIconInclude.href = '../../images/favicon.png';
    document.head.appendChild(favIconInclude);

    let iconInclude = document.createElement('link');
    iconInclude.rel="stylesheet";
    iconInclude.href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.3.0/font/bootstrap-icons.css";
    document.head.appendChild(iconInclude);

    let charsetInclude = document.createElement('meta');
    charsetInclude.charset = "UTF-8";
    document.head.appendChild(charsetInclude);

    let viewportSettings = document.createElement('meta');
    viewportSettings.name="viewport";
    viewportSettings.content="width=device-width, initial-scale=1.0";
    document.head.appendChild(viewportSettings);
}

fillHtmlHead();

/* functionality behind changing the preview image on the landing page */
function loadRandomPreview() {
    let rnd = Math.floor(10*Math.random()) + 1;
    let path = "../../images/bestOf/frame_" + rnd + ".png";
    document.getElementById("imagePreview").src = path;
}

/* create the header element */
function createHeader() {
    const headerObj = document.createElement("header");
    headerObj.id = "cmnHeader";
    document.body.insertBefore(headerObj, document.body.firstChild)
    document.getElementById("cmnHeader").innerHTML = "<h1> Abstract Computer Art by Continued Functions </h1>";
    document.getElementById("cmnHeader").innerHTML += "<div id = 'headerNavDiv'></div>";
    document.getElementById("headerNavDiv").innerHTML += "<a id='homeBtn' class='headerBtn' href='main.html'> <i class='bi bi-house'></i> Home </a>";
    document.getElementById("headerNavDiv").innerHTML += "<a id='galleryBtn' class='headerBtn' href='gallery.html'> <i class='bi bi-collection'></i> Gallery </a>";
    document.getElementById("headerNavDiv").innerHTML += "<a id='theoryBtn' class='headerBtn' href='theory.html'> <i class='bi bi-eyeglasses'></i> Theory </a>";
    document.getElementById("headerNavDiv").innerHTML += "<a id='createBtn' class='headerBtn' href='create.html'> <i class='bi bi-brush'></i> Create </a>";
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

/* fill the sample images section on the gallery page */
function fillSampleImages() {
    const sampleImgsSec = document.getElementById("sampleImgs");
    for (let i = 1; i <= 50; i++) {
        let framePath = "../../images/bestOf/frame_" + i + ".png"
        let tmpImg = document.createElement("img");
        tmpImg.src = framePath;
        sampleImgsSec.appendChild(tmpImg);
    }
}

fillSampleImages();

/* fill the zooms section on the gallery page */
function fillZooms() {
    const zoomsSec = document.getElementById("zooms");
    for (let i = 1; i <= 6; i++) {
        let framePath = "../../images/zooms/zoom_" + i + ".gif"
        let tmpImg = document.createElement("img");
        tmpImg.src = framePath;
        zoomsSec.appendChild(tmpImg);
    }
}

fillZooms();

/* functions to make content of nav panel in gallery (in)-visible at mouseover */

function makeNavVisible() {
    document.getElementById("navContent").style.display = "block";
}

function makeNavInvisible() {
    document.getElementById("navContent").style.display = "none";
}
