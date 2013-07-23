function displayElement(div) {
    var doc = document.getElementById(div)
    doc.className = doc.className + " rotatingForm";
    doc.style.display = "inline-block";
    return
}

function hideElement(div) {
    document.getElementById(div).style.display = "None";
    return
}
