const outerCont = document.getElementById("shanksAnimation");
outerCont.style.border = 'solid black';
const rows = [];
let numCols = 13 
for (let i=0; i<=numCols; i++) {
    const row = [];
    let cont = document.createElement('div');
    cont.style.textAlign = "left";
    outerCont.appendChild(cont);
    for (let j=1; j<numCols-2*i+1; j++) {
        let box = document.createElement('div');
        box.style.display = 'inline-block';
        box.style.border = 'solid black';
        box.style.margin = '1em';
        box.style.padding = '0.1em';
        cont.appendChild(box);
        row.push(box);
    }
    rows.push(row);
}

rows[0][0].innerHTML = 'z<sub>0</sub>';
rows[0][1].innerHTML = 'f(z<sub>0</sub>)';
rows[0][2].innerHTML = 'f(f(z<sub>0</sub>))';
rows[0][3].innerHTML = 'z<sub>3</sub>';
rows[0][4].innerHTML = 'z<sub>4</sub>';
