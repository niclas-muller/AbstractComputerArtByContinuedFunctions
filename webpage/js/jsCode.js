function loadRandomPreview() {
    rnd = Math.floor(20*Math.random());
    path = '../../images/samples/sample_' + rnd + '.png';
    getElementById('imagePreview').src = path;
}
