const firebaseConfig = {
    apiKey: "AIzaSyADwA6l2cK_BBn_dJgwJGmZ1YD8cCBEfX4",
    authDomain: "pechack-4826f.firebaseapp.com",
    databaseURL: "https://pechack-4826f-default-rtdb.firebaseio.com",
    projectId: "pechack-4826f",
    storageBucket: "pechack-4826f.appspot.com",
    messagingSenderId: "986323968038",
    appId: "1:986323968038:web:ed2dc74ef16a3bab3d46e7",
    measurementId: "G-E3HRQXQMRZ"
};

//initialize database
firebase.initializeApp(firebaseConfig);
//reference for database
var pechackDB = firebase.database().ref('pechack')

document.getElementById("peckhack").addEventListener("submit", submitForm);

function submitForm(e){
    e.preventDefault();
    var firstname= getElementVal("fname");
    var lastname= getElementVal("lname");
    var subject= getElementVal("subject");

    console.log(fname, lname, msgContent);
}

const getElementVal=(id)=>{
    return document.getElementById(id).value;
}