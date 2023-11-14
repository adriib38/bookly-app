//Importar funciones de peticionesAPI.js
import { crearPost, obtenerGruposUsuario } from './peticionesAPI.js';
import { validarPost } from './validaciones.js';

//Importar funciones de picker de emojis
import { picker } from './picker.js';

let username = document.getElementById('username').innerHTML;
const btnEnviarPost = document.getElementById('enviar-post');
const feedback = document.getElementById('box-feedback');
const selectGrupo = document.getElementById('select-grupo-post');

//Obtener grupos del usuario
obtenerGruposUsuario(username).then(grupos => {
    //Añadir una opción vacía
    selectGrupo.innerHTML = `<option value="">Selecciona un grupo</option>`;
    //Añadir una opción por cada grupo
    grupos.forEach(grupo => {
       selectGrupo.innerHTML += `<option value="${grupo.id}">${grupo.name}</option>`;
    });

}).catch(error => {
    console.log(error);
});
/**
 * Evento para crear un post
 */
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
    let idGrupo = selectGrupo.value ?? null;
    crearPost(contenido, idGrupo).then(posts => {
        feedback.innerHTML = `
            <div class="alert alert-successful">
                ¡Post publicado correctamente!
            </div>`;
        //Redirigir al muro
    }).catch(error => {
        feedback.innerHTML = `
            <div class="alert alert-error">
                Error al publicar el post. Intentalo más tarde.
                <br>
                ${error}
            </div>`;
    });
});








