
// Constructor of an XMLHttpRequest object
function getXMLHttpRequest() {
    var xhr = null;
     
    if (window.XMLHttpRequest || window.ActiveXObject) {
        if (window.ActiveXObject) {
            try {
                xhr = new ActiveXObject("Msxml2.XMLHTTP");
            } catch(e) {
                xhr = new ActiveXObject("Microsoft.XMLHTTP");
            }
        } else {
            xhr = new XMLHttpRequest(); 
        }
    } else {
        // XMLHttpRequest not supported by the browser
        return null;
    }
     
    return xhr;
}


function isAvailable(callback, field) {
    // Creation of an object
    var xhr = getXMLHttpRequest(); 

    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && (xhr.status == 200 || xhr.status == 0)) {
            callback(xhr.responseText);
        } else if (xhr.readyState < 4) {
            document.getElementById("loader").style.display = "inline";
        }
    };

    var user = document.getElementById(field).value;

    // Initialisation
    xhr.open("GET", "checkUser/" + user, true);
    // Sending request
    xhr.send(null);
}

function informUser(data) {
    document.getElementById("loader").style.display = "none";
    userObject = document.getElementById("username");
    if (data != "True") {
        userObject.className += " has-error";
    } else {
        userObject.className = userObject.className.replace(/ has-error/g, "");
    }
}
