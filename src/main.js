/* set global style elements*/

document.body.className = "font-mono bg-zinc-200 max-w-6xl mx-auto";

/* load common elements (stylesheet,etc.) into head */

fillHtmlHead();

function fillHtmlHead() {
    let styleSheetInclude = document.createElement('link');
    styleSheetInclude.rel = 'stylesheet';
    styleSheetInclude.href =  'output.css';
    document.head.appendChild(styleSheetInclude);

    let favIconInclude = document.createElement('link');
    favIconInclude.rel = 'icon';
    favIconInclude.type = 'image/x-icon';
    favIconInclude.href = '../images/favicon.png';
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

/* functionality behind changing the preview image on the landing page */
function loadRandomPreview() {
    let rnd = Math.floor(10*Math.random()) + 1;
    let path = "../images/bestOf/frame_" + rnd + ".png";
    document.getElementById("imagePreview").src = path;
}

/* create the header element */

createHeader();

function createHeader() {
    const headerObj = document.createElement("div");
    headerObj.className = "sticky top-0 w-full mb-3 text-center bg-amber-200 shadow";
    headerObj.id = "cmnHeader";

    const headline = document.createElement("h1");
    headline.innerHTML = "Abstract Computer Art by Continued Functions";
    headline.className = "text-2xl font-bold mb-2 pt-2";
    headerObj.appendChild(headline)

    const btnContainer = document.createElement("div");
    btnContainer.className = "flex justify-center";

    function addButton(btnId, btnHref, btnContent) {
        tmpDiv = document.createElement("div");
        tmpDiv.className = "m-3 p-2 border-2 rounded-md hover:bg-indigo-600 hover:text-white transition-colors duration-600";
        tmpBtn = document.createElement("a");
        tmpBtn.id = btnId;
        tmpBtn.href = btnHref;
        tmpBtn.innerHTML = btnContent;
        tmpDiv.appendChild(tmpBtn);
        btnContainer.appendChild(tmpDiv);
    }
    addButton('mainBtn', 'main.html', "<i class='bi bi-house'></i> Home ");
    addButton('galleryBtn', 'gallery.html', "<i class='bi bi-collection'></i> Gallery ");
    addButton('theoryBtn', 'theory.html', "<i class='bi bi-eyeglasses'></i> Theory ");
    addButton('createBtn', 'create.html', "<i class='bi bi-brush'></i> Create ");

    headerObj.appendChild(btnContainer)

    document.body.insertBefore(headerObj, document.body.firstChild)
}

/* create the footer element */

createFooter();

function createFooter() {
    const footerObj = document.createElement("div");
    footerObj.className = "sticky bot-0 w-full mt-3 text-center bg-amber-200 shadow";
    footerObj.id = "cmnFooter";
    let subscribeLink = document.createElement("a");
    let darkmodeSwitch = document.createElement("a");
    let footerTitle = document.createElement("p");
    subscribeLink.innerHTML = "I am a subscription link!";
    darkmodeSwitch.innerHTML = "I am a darkmode switch!";
    footerTitle.innerHTML = "I am a footer title!";
    footerObj.appendChild(footerTitle);
    footerObj.appendChild(subscribeLink);
    footerObj.appendChild(darkmodeSwitch);
    document.body.insertBefore(footerObj, document.body.lastChild);
}

/* fill the sample images section on the gallery page */

function fillSampleImages() {
    const sampleImgsSec = document.getElementById("sampleImgs");
    for (let i = 1; i <= 50; i++) {
        let framePath = "../images/bestOf/frame_" + i + ".png"
        let tmpImg = document.createElement("img");
        tmpImg.src = framePath;
        tmpImg.className = "mx-auto m-2";
        sampleImgsSec.appendChild(tmpImg);
    }
}

/* fill the zooms section on the gallery page */

function fillZooms() {
    const zoomsSec = document.getElementById("zooms");
    for (let i = 1; i <= 6; i++) {
        let framePath = "../images/zooms/zoom_" + i + ".gif"
        let tmpImg = document.createElement("img");
        tmpImg.src = framePath;
        tmpImg.className = "mx-auto m-2";
        zoomsSec.appendChild(tmpImg);
    }
}

/* fill the walks section on the gallery page */

function fillWalks() {
    const walksSec = document.getElementById("walks");
    for (let i = 1; i <= 4; i++) {
        let framePath = "../images/orbits/orbit_" + i + ".gif"
        let tmpImg = document.createElement("img");
        tmpImg.src = framePath;
        tmpImg.className = "mx-auto m-2";
        walksSec.appendChild(tmpImg);
    }
}

if (document.URL.split('/').slice(-1)[0] == "gallery.html") {
    fillSampleImages();
    fillZooms();
    fillWalks();
}

/* style button corresponding to active page */

let btnName = document.URL.split('/').slice(-1)[0].split('.')[0] + 'Btn';
document.getElementById(btnName).className = "font-bold";
document.getElementById(btnName).parentNode.className = "m-3 p-2 border-4 rounded-md hover:bg-indigo-600 hover:text-white transition-colors duration-600";
