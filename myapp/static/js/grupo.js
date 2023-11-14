//Importar funciones de peticionesAPI.js
import { obtenerPostsGrupo, crearPostGrupo } from './peticionesAPI.js';
import { formatearPost } from './formatoPost.js';
import { validarPost } from './validaciones.js';

//Importar funciones de picker de emojis
import { picker } from './picker.js';

//Obtener id del grupo actual, segun ultimo elemento de la url
const url = window.location.href;
const idGrupo = url.substring(url.lastIndexOf('/') + 1);

const btnEnviarPost = document.getElementById('enviar-post');
const btnDejarGrupo = document.getElementById('grupo-dejar');
const feedback = document.getElementById('box-feedback');

//Evento para dejar grupo
btnDejarGrupo.addEventListener('click', (e) => {
    e.preventDefault();

    const swalWithBootstrapButtons = Swal.mixin({
        customClass: {
            confirmButton: 'btn btn-success',
            cancelButton: 'btn btn-danger'
        },
        buttonsStyling: false
    })

    swalWithBootstrapButtons.fire({
        title: '¿Seguro que quieres salir?',
        showClass: {
            popup: 'fadeInUp'
        },
        hideClass: {
            popup: 'display-none'
        },
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí, salir',
        cancelButtonText: 'No, cancelar!',
        reverseButtons: true
    }).then((result) => {
        if (result.isConfirmed) {
            //Redireccionar a la página de eliminación
            location.href = '/grupo/' + idGrupo + '/join';
        } else if (
            /* Read more about handling dismissals below */
            result.dismiss === Swal.DismissReason.cancel
        ) {
            //Cuando se cancela la accion
        }
    })
});

//Evento para enviar post
btnEnviarPost.addEventListener('click', (e) => {
    e.preventDefault();
    const contenidoPost = document.getElementById('contenido-post');
    const contenido = contenidoPost.value;

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
    crearPostGrupo(contenido, idGrupo).then(posts => {
        feedback.innerHTML = `
        <div class="alert alert-successful">
            Post publicado correctamente!
        </div>`;
        //Refrescar posts
        obtenerPostsGrupo(idGrupo).then(posts => {
            //Imprimir posts en el muro
            imprimirPosts(posts);
        }).catch(error => {
            
        });
    }).catch(error => {
        feedback.innerHTML = `
        <div class="alert alert-error">
            Error al publicar el post. Intentalo más tarde.
        </div>`;
    });
});

/**
 * Obtener todos los posts de todos los usuarios
 */
obtenerPostsGrupo(idGrupo).then(posts => {
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

        let linkDelete = '';
        if(post.is_mine == true){
            linkDelete = `<a href="/post/${post.id}/delete"><i class="fas fa-trash"></i></a>`;
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
                    ${linkDelete}
                </div>
            </article>
        `;
    });
}
