/* Create a canvas holding an animation of the shanks process */
alert(window.innerWidth);

const outerCont = document.getElementById("shanksAnimation");
outerCont.className = "border m-2 rounded-md shadow-md bg-amber-100 text-center";

let aniBtn = document.createElement('button');
aniBtn.type = "button";
aniBtn.className = "border rounded-lg m-2 p-1 bg-indigo-700 text-white cursor-pointer hover:shadow-xl transition-shadow duration-100";
aniBtn.innerHTML = "Click me to (re)-start animation";
aniBtn.addEventListener("click",animate);
outerCont.appendChild(aniBtn)

const rows = [];
let numCols = 9
for (let i=0; i<=numCols; i++) {
    const row = [];
    let cont = document.createElement('div');
    cont.style.textAlign = "left";
    outerCont.appendChild(cont);
    for (let j=1; j<numCols-2*i+1; j++) {
        let box = document.createElement('div');
        box.className = "inline-block m-1 p-1 w-10 h-auto text-center";
        cont.appendChild(box);
        row.push(box);
    }
    rows.push(row);
}

let interval = 500;

function _fill(row,col) {
    rows[row][col].className = "inline-block m-1 p-1 border rounded-sm w-10 h-auto text-center";
    let content = "";
    if (row == 0) {
        content += "z<sub>"+col+"</sub>";
    } else {
        content += "S<sup>"+row+"</sup><sub>"+col+"</sub>";
    }
    rows[row][col].innerHTML = content;
}

function fill(row,col) {
    setTimeout(_fill,interval*count,row,col);
    count++;
}

function highlight(row,col) {
    rows[row][col].className = "inline-block m-1 p-1 border-4 border-red-900 rounded-sm w-10 h-auto text-center";
}

function clearAll() {
    for (let i=0; i<=numCols; i++) {
        for (let j=1; j<numCols-2*i+1; j++) {
            rows[i][j-1].innerHTML = "";
            rows[i][j-1].className = "";
        }
    }
}

let count = 1;
function animate() {
    count = 1;
    clearAll();
    fill(0,0);
    fill(0,1);
    fill(0,2);
    fill(1,0);

    fill(0,3);
    fill(1,1);
    fill(0,4);
    fill(1,2);
    fill(2,0);

    fill(0,5);
    fill(1,3);
    fill(2,1);
    fill(0,6);
    fill(1,4);
    fill(2,2);
    fill(3,0);

    fill(0,7);
    fill(1,5);
    fill(2,3);
    fill(3,1);
    fill(0,8);
    fill(1,6);
    fill(2,4);
    fill(3,2);
    fill(4,0);

    setTimeout(function() {
        highlight(0,8);
        highlight(1,6);
        highlight(2,4);
        highlight(3,2);
        highlight(4,0);
    },interval*count);
}
