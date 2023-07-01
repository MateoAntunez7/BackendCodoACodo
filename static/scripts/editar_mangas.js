console.log(location.search)    
var args = location.search.substr(1).split('&');  
//separa el string por los “&” creando una lista
// [“id=3” , “nombre=’tv50’” , ”precio=1200”,”stock=20”]
console.log(args)
var parts = []
for (let i = 0; i < args.length; ++i) {
    parts[i] = args[i].split('=');
}
console.log(parts)

//// [[“id",3] , [“nombre",’tv50’]]
//decodeUriComponent elimina los caracteres especiales que recibe en la URL 
document.getElementById("id").value = decodeURIComponent(parts[0][1])
document.getElementById("titulo").value = decodeURIComponent(parts[1][1])
document.getElementById("volumen").value = decodeURIComponent(parts[2][1])
document.getElementById("imagen").value =decodeURIComponent( parts[3][1])

function modificar() {
    let id = document.getElementById("id").value
    let t = document.getElementById("titulo").value
    let v = parseFloat(document.getElementById("volumen").value)
    let i = document.getElementById("imagen").value
   
    let manga = {
        titulo: t,
        volumen: v,
        imagen: i
    }
    let url = "http://127.0.0.1:5000/mangas"+id
    var options = {
        body: JSON.stringify(producto),
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        redirect: 'follow'
    }
    fetch(url, options)
        .then(function () {
            console.log("modificado")
            window.location.href = "./index.html";  
        //NUEVO,  si les da error el fetch  comentar esta linea que puede dar error  
        })
        .catch(err => {
            //this.errored = true
            console.error(err);
        })      
}
