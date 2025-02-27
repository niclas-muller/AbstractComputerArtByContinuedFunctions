/* Create a canvas holding an animation of the shanks process */

const outerCont = document.getElementById("shanksAnimation");
outerCont.style.border = 'solid black';

let aniBtn = document.createElement('button');
aniBtn.type = "button";
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
        box.style.display = 'inline-block';
        box.style.margin = '1em';
        box.style.padding = '0.1em';
        cont.appendChild(box);
        row.push(box);
    }
    rows.push(row);
}

let interval = 500;

function _fill(row,col) {
    rows[row][col].style.border = 'solid black';
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
    rows[row][col].style.border = 'solid red';
}

let count = 1;
function animate() {
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
