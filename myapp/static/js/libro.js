//Importar funciones de peticionesLibros.js
import { obtenerLibroPorId, obtenerAutorPorId } from './peticionesLibros.js';

//Importar funciones de peticionesAPI.js
import { obtenerResenyasLibro, crearResenya } from './peticionesAPI.js';

const divLibro = document.getElementById("box-libro-info");
const libroPortada = document.getElementById("libro-portada");

const divResenyas = document.getElementById("box-resenyas");
const btnEnviarResenya = document.getElementById("resenya-enviar");
const boxFeedback = document.getElementById("box-feedback");

//Obtener el id del libro de la url
const idLibro = window.location.pathname.split('/')[2];

//Obtener resenyas del libro
obtenerResenyasLibro(idLibro).then(resenyas => {
    imprimirResenyas(resenyas);
}).catch(error => {
    console.log(error);
});

//Comprobar si el libro ya está en el localstorage
if (localStorage.getItem('libro:' + idLibro)) {
    //Obtener el libro del localstorage
    const libro = JSON.parse(localStorage.getItem('libro:' + idLibro));
    //Imprimir el libro
    imprimirLibro(libro);
} else {
    //Obtener el libro de la API
    obtenerLibroPorId(idLibro).then(libro => {
        //Añadir el autor al libro
        obtenerAutorPorId(libro.authors[0].author.key).then(autor => {
            //Añadir el autor al libro
            libro.author = autor;
            //Almacenar el libro en el localstorage
            localStorage.setItem('libro:' + idLibro, JSON.stringify(libro));
            //Imprimir el libro
            imprimirLibro(libro);
        }).catch(error => {
            console.log(error);
        });
    }).catch(error => {
        console.log(error);
    });
}

//Imprimir el libro
function imprimirLibro(libro) {
    let descripcion = libro.description ? libro.description : 'Sin descripción';
    divLibro.innerHTML = `
        <h1 id="libro-titulo">${libro.title}</h1>
        <p id="libro-autor"><a href="${libro.author.wikipedia}">${libro.author.name}</a>
        <p id="libro-descripcion">${descripcion}</p>
        <a href="https://www.amazon.es/s?k=${libro.title}" target="_blank"> Ver en amazon</a>
    `;

    libroPortada.src = `https://covers.openlibrary.org/b/id/${libro.covers[0]}-L.jpg`;
    libroPortada.classList.remove('placeholder');
}

function imprimirResenyas(resenyas) {
    divResenyas.innerHTML = '';
    let resenyasTitulo = document.createElement('h3');
    resenyasTitulo.innerHTML = resenyas[0].stars_average + '<img src="/static/svg/star.svg" alt="Valoración">' + ' de ' + resenyas.length + ' valoraciones';
    divResenyas.appendChild(resenyasTitulo);
    resenyas.forEach(resenya => {

        console.log(resenya);
        let article = document.createElement('article');

        let fechaCreacion = new Date(resenya.created_at).toLocaleString();

        let lecturaVerificada = resenya.readed ? 'Lectura verificada - ' : '';

        let nombre = document.createElement('h3');
        nombre.classList.add('post-user');
        nombre.innerHTML = '@' + resenya.username;
        if (resenya.verified == true) {
            nombre.innerHTML += '<img src="/static/svg/verify.svg" alt="Verificado" class="post-user-verified">';
        }

        let estrellas = document.createElement('span');
        let estrellasHTML = '';
        for (let i = 0; i < resenya.stars; i++) {
            estrellasHTML += '<img src="/static/svg/star.svg" alt="Valoración">';
        }
        estrellas.innerHTML = estrellasHTML;

        article.innerHTML += `
            <article class="resenya post">
                <a class="post-user" href="/user/${resenya.username}">${nombre.outerHTML}</a>
     
                <span class="post-stars">${estrellas.outerHTML}</span>
                <p class="post-contenido">${resenya.content}</p>    
                <span class="fecha">${lecturaVerificada} ${fechaCreacion}</span>
                <span class="linea-separador"></span>
                <div class="post-acciones">
                    <a href="/resenya/${resenya.id}/delete"
                        <i class="fas fa-trash"></i>
                    </a>
                </div>
            </article>
        `;
        divResenyas.appendChild(article);
    });
}


btnEnviarResenya.addEventListener('click', () => {
    //Obtener estrellas seleccionadas
    const radioButtons = document.querySelectorAll('input[name="rate"]');
    let estrellasSeleccionadas;
    for (const radioButton of radioButtons) {
        if (radioButton.checked) {
            estrellasSeleccionadas = radioButton.value;
            break;
        }
    }
    //Obtener contenido de la reseña
    let resenyaContenido = document.getElementById('resenya-contenido').value;
    //Enviar resenya
    crearResenya(idLibro, resenyaContenido, estrellasSeleccionadas).then(resenyas => {
        boxFeedback.innerHTML = `
        <div class="alert alert-successful">
            Reseña publicada correctamente!
        </div>`;
        //Obtener resenyas del libro
        obtenerResenyasLibro(idLibro).then(resenyas => {
            imprimirResenyas(resenyas);
        }).catch(error => {
            console.log(error);
        });
    }).catch(error => {
        boxFeedback.innerHTML = `
        <div class="alert alert-error">
            Error al publicar la reseña. Intentalo más tarde.
        </div>`;
    });
});