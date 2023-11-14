//Importar funciones de peticionesAPI.js
import { obtenerMuro, crearPost, obtenerGruposUsuario, obtenerListasUsuario } from './peticionesAPI.js';
import { obtenerLibroPorId } from './peticionesLibros.js';
import { formatearPost } from './formatoPost.js';
import { validarPost } from './validaciones.js';

//Importar funciones de picker de emojis
import { picker } from './picker.js';

const btnEnviarPost = document.getElementById('enviar-post');
const feedback = document.getElementById('box-feedback');
const ulAsideGrupos = document.getElementById('ul-grupos');
const divAsideLists = document.getElementById('div-listas');

let username = document.getElementById('username').innerHTML;

const ulListaLeidos = document.getElementById('ul-lista-leidos');
const ulListaLeyendo = document.getElementById('ul-lista-leyendo');
const ulListaPorLeer = document.getElementById('ul-lista-por-leer');

/**
 * Obtener grupos del usuario
 */
obtenerGruposUsuario(username).then(grupos => {
    ulAsideGrupos.innerHTML = '';
    grupos.forEach(grupo => {
        let li = document.createElement('li');
        li.innerHTML = `<a href="/grupo/${grupo.id}">> ${grupo.name}</a>`;
        ulAsideGrupos.appendChild(li);
    });
}).catch(error => {
    (error);
});

/**
 * Obtener listas del usuario
 */
obtenerListasUsuario(username).then(listas => {
    
    //Por cada lista
    listas.forEach(lista => {
        //Reducir libros de la lista a 4
        lista.books = lista.books.slice(0, 4);
       (lista);

        //Añadir titulos a las listas
        if(lista.type_list == 'leidos'){
            ulListaLeidos.innerHTML = '';
            //Por cada libro de la lista, crear un elemento li
            lista.books.forEach(async book => {
                let li = document.createElement('li');
                let tituloLibro = await obtenerNombreLibro(book.book);
                li.innerHTML = `<a href="/libro/${book.book}">> ${tituloLibro}</a>`;
                ulListaLeidos.appendChild(li);
            });
        }

        if(lista.type_list == 'leyendo'){
            ulListaLeyendo.innerHTML = '';
            //Por cada libro de la lista, crear un elemento li
            lista.books.forEach(async book => {
                let li = document.createElement('li');
                let tituloLibro = await obtenerNombreLibro(book.book);
                li.innerHTML = `<a href="/libro/${book.book}">> ${tituloLibro}</a>`;
                ulListaLeyendo.appendChild(li);
            });
        }

        if(lista.type_list == 'por_leer'){
            ulListaPorLeer.innerHTML = '';
            //Por cada libro de la lista, crear un elemento li
            lista.books.forEach(async book => {
                let li = document.createElement('li');
                let tituloLibro = await obtenerNombreLibro(book.book);
                li.innerHTML = `<a href="/libro/${book.book}">> ${tituloLibro}</a>`;
                ulListaPorLeer.appendChild(li);
            });
        }
    });
}).catch(error => {
    (error);
});

/**
 * Funcion para obtener el nombre de un libro
 */
async function obtenerNombreLibro(id) {
    try {
        const libro = await obtenerLibroPorId(id);
        return libro.title;
    } catch (error) {
        (error);
        return id;
    }
}

/**
 * Obtener todos los posts de todos los usuarios
 */
obtenerMuro().then(posts => {
    //Imprimir posts en el muro
    (posts);
    imprimirPosts(posts);
}).catch(error => {
    (error);
});

/**
 * Evento para crear un post
 */
btnEnviarPost.addEventListener('click', (e) => {
    e.preventDefault();
    let contenidoPost = document.getElementById('contenido-post');
    let contenido = contenidoPost.value;

    //Validar contenido del post
    let validacion = validarPost(contenido);
    if(validacion.valido == false){
        feedback.innerHTML = `
            <div class="alert alert-error">
                ${validacion.mensaje}
            </div>
        `;
        return;
    }

    //Crear post
    crearPost(contenido).then(posts => {
        feedback.innerHTML = `
        <div class="alert alert-successful">
            Post publicado correctamente!
        </div>`;
        //Obtener todos los posts e imprimirlos
        obtenerMuro().then(posts => {
            //Imprimir posts en el muro
            (posts);
            imprimirPosts(posts);
        }).catch(error => {
            (error);
        });
    }).catch(error => {
        feedback.innerHTML = `
        <div class="alert alert-error">
            Error al publicar el post. Intentalo más tarde.
        </div>`;
    });
});

/**
 * Función para imprimir los posts en el muro
 */
function imprimirPosts(posts) {
    const seccionMuro = document.getElementById('muro');
    seccionMuro.innerHTML = '';
    posts.forEach(post => {
        post = formatearPost(post);

        let nombre = document.createElement('h3');
        nombre.classList.add('post-user');
        nombre.innerHTML = '@' + post.user;
        if (post.verified == true) {
            nombre.innerHTML += '<img src="/static/svg/verify.svg" alt="Verificado" class="post-user-verified">';
        }

        let fechaCreacion = new Date(post.created_at).toLocaleString();

        let linkDelete = '';
        if(post.is_mine == true){
            linkDelete = `<a href="/post/${post.id}/delete"><i class="fas fa-trash"></i></a>`;
        }

        seccionMuro.innerHTML += `
            <article class="post">
                <a href="/user/${post.user}">${nombre.outerHTML}</a>
             
                <p class="post-contenido">${post.content}</p>
               
                <span class="fecha">${fechaCreacion} ${post.group}</span>
                <span class="linea-separador"></span>
                <div class="post-acciones">
                    <a href="/post/${post.id}">
                        <i class="fas fa-share"></i>
                        ${post.num_comments}
                    </a>
                    ${linkDelete}
                </div>
            </article>
        `;
    });
}

