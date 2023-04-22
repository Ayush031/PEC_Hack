import firebaseConfig from "./firebaseConfig"

//initialize database
firebase.initializeApp(firebaseConfig);
//reference for database
var pechackDB = firebase.database().ref('pechack')

document.getElementById("pechack").addEventListener("submit", submitForm);

function submitForm(e) {
    e.preventDefault();
    var firstname = getElementVal("fname");
    var lastname = getElementVal("lname");
    var subject = getElementVal("subject");

    saveMsg(firstname, lastname, subject);

    //enable alert after submission
    document.querySelector('.alert').style.display = "block";

    //remove alert
    setTimeout(() => {
        document.querySelector('.alert').style.display = "none";
    }, 3000);

    //reset form
    document.getElementById("pechack").reset();
}

const saveMsg = (fname, lname, subject) => {
    var newPechack = pechackDB.push();

    newPechack.set({
        fname: fname,
        lname: lname,
        subject: subject,
    });

};

const getElementVal = (id) => {
    return document.getElementById(id).value;
}