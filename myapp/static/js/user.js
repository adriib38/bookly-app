//Importar funciones de peticionesAPI.js
import { obtenerPostsUsuario, obtenerLibrosEscritor, obtenerListasUsuario} from './peticionesAPI.js';
import { obtenerLibroPorId } from './peticionesLibros.js';
import { formatearPost } from './formatoPost.js';

const divPostsUsuario = document.getElementById('posts-usuario');
const username = document.getElementById('username').innerHTML;
const divLibrosUsuario = document.getElementById('box-libros-autor');
const ulListaLeidos = document.getElementById('ul-lista-leidos');
const ulListaLeyendo = document.getElementById('ul-lista-leyendo');
const ulListaPorLeer = document.getElementById('ul-lista-por-leer');

/**
 * Obtener todos los posts de todos los usuarios
 */
obtenerPostsUsuario(username).then(posts => {
    //Imprimir posts del usuario
    imprimirPosts(posts);
}).catch(error => {
    console.log(error);
});

/**
 * Obtener libros del usuario
 */
async function obtenerYImprimirLibros(username) {
    try {
        const libros = await obtenerLibrosEscritor(username);
        const librosConInfo = await Promise.all(libros.map(async (libro) => {
            const libroInfo = await obtenerInfoLibro(libro.book);
            return libroInfo;
        }));
        imprimirLibrosEscritor(librosConInfo);
    } catch (error) {
        console.log(error);
    }
}

obtenerYImprimirLibros(username);

/**
 * Funcion para obtener el nombre de un libro
 */
//usar obtenerLibroPorId(id) de peticionesLibros.js
function obtenerInfoLibro(id) {
    return new Promise((resolve, reject) => {
        obtenerLibroPorId(id).then(libro => {
            resolve(libro);
        }).catch(error => {
            console.log(error);
            reject(error);
        });
    });
}

/**
 * Obtener listas del usuario
 */
obtenerListasUsuario(username).then(listas => {
    //Por cada lista
    listas.forEach(lista => {
        //Reducir libros de la lista a 4
        lista.books = lista.books.slice(0, 4);
       console.log(lista);
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
    console.log(error);
});

/**
 * Funcion para obtener el nombre de un libro
 */
async function obtenerNombreLibro(id) {
    try {
        const libro = await obtenerLibroPorId(id);
        return libro.title;
    } catch (error) {
        console.log(error);
        return id;
    }
}

// Imprimir los posts del usuario
function imprimirPosts(posts) {
    divPostsUsuario.innerHTML = '';
    posts.forEach(post => {
        post = formatearPost(post);

        let nombre = document.createElement('h3');
        nombre.classList.add('post-user');
        nombre.innerHTML = '@' + post.user;
        if (post.verified == true) {
            nombre.innerHTML +=
                `<img src="/static/svg/verify.svg" alt="Verificado" class="post-user-verified">`;
        }

        let fechaCreacion = new Date(post.created_at).toLocaleString();

        let linkDelete = '';
        if(post.is_mine == true){
            linkDelete = `<a href="/post/${post.id}/delete"><i class="fas fa-trash"></i></a>`;
        }
        divPostsUsuario.innerHTML += `
            <article class="post">
                <a href="/user/${post.user}">${nombre.outerHTML}</a>
                
                <a href="/post/${post.id}">
                    <p class="post-contenido">${post.content}</p>
                </a>

                <span class="fecha">${fechaCreacion}</span>
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

function imprimirLibrosEscritor(libros) {

    if(libros.length != 0){
        // Crear un elemento contenedor para la lista de libros
        let ul = document.createElement('ul');
        ul.classList.add('lista-libros-usuario');
        //Crear titulo de la lista
        let h3 = document.createElement('h3');
        h3.innerHTML = 'Libros del autor';

        // Crear un elemento contenedor para cada libro
        libros.forEach(libro => {
            console.log(libro);
            let key = libro.key.split('/')[2];
            ul.innerHTML += `
                <li class="libro-usuario">
                    <a href="/libro/${key}">${libro.title}</a>
                </li>
            `;
        });

        divLibrosUsuario.appendChild(h3);
        divLibrosUsuario.appendChild(ul);
    } else {
        divLibrosUsuario.innerHTML = '';
    }
}
