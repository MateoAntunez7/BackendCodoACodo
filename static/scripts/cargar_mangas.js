function guardar() {
    let t = document.getElementById("titulo").value
    let v = parseFloat(document.getElementById("volumen").value)
    let i = document.getElementById("imagen").value

    let manga = {
        titulo: t,
        volumen: v,
        imagen: i
    }
    let url = "http://127.0.0.1:5000/mangas"
    var options = {
        body: JSON.stringify(manga),
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
    }
    fetch(url, options)
        .then(function () {
            console.log("creado")
            window.location.href = "http://127.0.0.1:5000/";  
        })
        .catch(err => {
            console.error(err);
        })
}
