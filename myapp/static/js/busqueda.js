//Importar funciones de peticionesAPI.js
import { obtenerPostsBusqueda, obtenerUsuariosBusqueda } from './peticionesAPI.js';

//Importar funciones de peticionesLibros.js
import { obtenerLibrosPorTitulo } from './peticionesLibros.js';

//Importar funciones de formatoPost.js
import { formatearPost } from './formatoPost.js';

const divPostsMuro = document.getElementById('box-muro-busqueda');
const divUsuariosMuro = document.getElementById('box-usuarios-busqueda');
const divLibrosMuro = document.getElementById('box-libros-busqueda');

const q = document.getElementById('query').innerHTML;
const inputBusqueda = document.getElementById('input-busqueda');
inputBusqueda.value = q;


//Tabs
document.getElementById("libros-btn").addEventListener("click", function () { openTab(event, 'box-libros-busqueda'); });
document.getElementById("usuarios-btn").addEventListener("click", function () { openTab(event, 'box-usuarios-busqueda'); });
document.getElementById("posts-btn").addEventListener("click", function () { openTab(event, 'box-muro-busqueda'); });

function openTab(evt, seccionNombre) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(seccionNombre).style.display = "flex";
    evt.currentTarget.className += " active";
}

/**
 * Obtener los usuarios por busqueda
 */
obtenerUsuariosBusqueda(q).then(usuarios => {
    //Imprimir usuarios en el muro
    //console.log(usuarios);
    imprimirUsuarios(usuarios);
}).catch(error => {
    //console.log(error);
});

/**
 * Obtener los posts por busqueda
 */
obtenerPostsBusqueda(q).then(posts => {
    //Imprimir posts en el muro
    imprimirPosts(posts);
}).catch(error => {
    //console.log(error);
});

/**
 * Obtener los libros por busqueda
 */
obtenerLibrosPorTitulo(q, 5).then(libros => {
    //Imprimir libros en el muro
    libros = libros.docs;
    //console.log(libros);
    imprimirLibros(libros);
}).catch(error => {
    //console.log(error);
});

// Imprimir los usuarios
function imprimirUsuarios(usuarios){
    if (usuarios.length == 0){
        divUsuariosMuro.innerHTML = `
            <article class="usuario">
                <h3>No se han encontrado usuarios.</h3>
            </article>
        `;
        return;
    }

    //Dejar 5 usuarios
    usuarios = usuarios.slice(0, 5);

    divUsuariosMuro.innerHTML = '';
    usuarios.forEach(usuario => {

        let nombre = document.createElement('h3');
        nombre.classList.add('post-user');
        nombre.innerHTML = '@' + usuario.username;
        if (usuario.profile.verified == true){
            nombre.innerHTML += 
            `<img src="/static/svg/verify.svg" alt="Verificado" class="post-user-verified">`;
        }

        divUsuariosMuro.innerHTML += `
            <article class="usuario">
                <a href="/user/${usuario.username}">${nombre.outerHTML}</a>
            </article>
        `;
    });
}

// Imprimir los posts del usuario
function imprimirPosts(posts){
    divLibrosMuro.innerHTML = '';
    if (posts.length == 0){
        divPostsMuro.innerHTML = `
            <article class="usuario">
                <h3>No se han encontrado posts.</h3>
            </article>
        `;
        return;
    }

    posts.forEach(post => {
        post = formatearPost(post);

        let nombre = document.createElement('h3');
        nombre.classList.add('post-user');
        nombre.innerHTML = '@' + post.user;
        if (post.verified == true){
            nombre.innerHTML += 
            `<img src="/static/svg/verify.svg" alt="Verificado" class="post-user-verified">`;
        }

        let fechaCreacion = new Date(post.created_at).toLocaleString();
        divPostsMuro.innerHTML += `
            <article class="post">
                <a href="/user/${post.user}">${nombre.outerHTML}</a>
                
                <a href="/post/${post.id}">
                    <p class="post-contenido">${ post.content }</p>
                </a>

                <span class="fecha">${ fechaCreacion }</span>
                <span class="linea-separador"></span>
                <div class="post-acciones">
                    <a href="/post/${post.id}">
                        <i class="fas fa-share"></i>
                        ${post.num_comments}
                    </a>
                    <a href="/post/${post.id}/delete"
                        <i class="fas fa-trash"></i>
                    </a>
                </div>
            </article>
        `;
    });
}

function imprimirLibros(libros){
    if (libros.length == 0){
        divLibrosMuro.innerHTML = `
            <article class="usuario">
                <h3>No se han encontrado libros.</h3>
            </article>
        `;
        return;
    }

    divLibrosMuro.innerHTML = '';
    libros.forEach(libro => {
        let article = document.createElement('article');
        let nombre = document.createElement('h3');
        nombre = libro.title;
        
        let id = libro.key.split('/')[2];
        //Añadir nombre a article
        article.innerHTML = `
            <a href="/libro/${id}">${nombre}</a>
        `;
        divLibrosMuro.appendChild(article);
    });
}