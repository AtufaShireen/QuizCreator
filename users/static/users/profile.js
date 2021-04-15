
function myFunction() {
    var x = document.getElementById("myDIV");
    var y = document.getElementById("content");
    if (x.style.display === "none") {
        y.style.width = "460px";
        x.style.display = "block";
        y.style.margin = "40px 20px 0 20px";
    }
    else {
        x.style.display = "none";
    }
}

document.getElementById('getval').addEventListener('change', readURL, true);
function readURL() {
    var file = document.getElementById("getval").files[0];
    var reader = new FileReader();
    reader.onloadend = function () {
        document.getElementById('profile-upload').style.backgroundImage = "url(" + reader.result + ")";
    }
    if (file) {
        reader.readAsDataURL(file);
    } else {
    }
}