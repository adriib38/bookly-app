// Importar funciones de peticiones a la API
import { obtenerPostsHashtag } from './peticionesAPI.js';
import { formatearPost } from './formatoPost.js';

let hashtag = window.location.href.split('/').pop();


/**
 * Obtener todos los posts de todos los usuarios
 */
obtenerPostsHashtag(hashtag).then(posts => {
    //Imprimir posts en el muro
    imprimirPosts(posts);
}).catch(error => {
    console.log(error);
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
        seccionMuro.innerHTML += `
            <article class="post">
                <a href="/user/${post.user}">${nombre.outerHTML}</a>
                <a href="/post/${post.id}">
                    <p class="post-contenido">${post.content}</p>
                </a>
                <span class="fecha">${fechaCreacion} ${post.group}</span>
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
