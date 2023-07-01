const { createApp } = Vue

  createApp({
    data() {
      return {
        url:"http://127.0.0.1:5000/mangas",
        mangas:[],
        error:false,
        cargando:true
      }
    },
    
    created() {
        this.fetchData(this.url)
    },
    methods: {
        fetchData(url) {
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    this.mangas = data;
                    this.cargando=false
                })
                .catch(err => {
                    console.error(err);
                    this.error=true              
                })
        },

        eliminar(manga) {
            const url = 'http://localhost:5000/mangas/' + manga;
            var options = {
                method: 'DELETE',
            }
            fetch(url, options)
                .then(res => res.text()) // or res.json()
                .then(res => {
                    location.reload();
                })
        }


    },
    



  }).mount('#app')