
/**
 * Funcion para obtener el token del usuario desde las cookies
 * 
 * @returns token del usuario
 */
export function obtenerToken() {
    //Obtener token del usuario
    var cookies = document.cookie.split(';');
    var tokenUser = null;
    for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        if (cookie.indexOf('tokenUser=') === 0) {
            tokenUser = cookie.substring('tokenUser='.length, cookie.length);
            break;
        }
    }
    tokenUser = 'Token ' + tokenUser;
    return tokenUser;
}

//Almacenar token del usuario para usarlo en las peticiones
let tokenUser = obtenerToken();

/**
 * Obtener todos los posts de todos los usuarios
 */
export function obtenerMuro() {
    return new Promise((resolve, reject) => {
        fetch('http://127.0.0.1:8000/api/muro/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': tokenUser
            }
        })
            .then(response => response.json())
            .then(data => {
                resolve(data);
            })
            .catch(error => {
                console.log(error);
                reject(error);
            });
    });
}

/**
 * Función para crear un post
 */
export async function crearPost(contenido, idGrupo = null) {
    try {
        const response = await fetch('http://127.0.0.1:8000/api/posts/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': tokenUser
            },
            body: JSON.stringify({
                content: contenido,
                group: idGrupo
            })
        });

        const post = await response.json();
        post.content = contenido; // Agregar la propiedad 'content' al objeto 'post'
        controlNotificaciones(post); // Comprobar si se menciona a un usuario para enviarle una notificación

        return response;
    } catch (error) {
        console.log(error);
    }
}

/**
 * Función para obtener los posts de un usuario
 */
export async function obtenerPostsUsuario(username) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/api/postusuario/${username}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': tokenUser
            }
        });
        const data = await response.json();
        return data;
    } catch (error) {
        console.log(error);
    }
}

/**
 * Función para obtener los posts con un hashtag
 */
export async function obtenerPostsHashtag(hashtag) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/api/posts/hashtag/${hashtag}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': tokenUser
            }
        });
        const data = await response.json();
        return data;
    } catch (error) {
        console.log(error);
    }
}

/**
 * Función para obtener los posts con un contenido
 */
export async function obtenerPostsBusqueda(q) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/api/posts/busqueda/${q}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': tokenUser
            }
        });
        const data = await response.json();
        return data;
    } catch (error) {
        console.log(error);
    }
}

/**
 * Funcion para obtener los usuarios segun un username
 */
export async function obtenerUsuariosBusqueda(q) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/api/users/busqueda/${q}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': tokenUser
            }
        });
        const data = await response.json();
        return data;
    } catch (error) {
        console.log(error);
    }
}

/**
 * Funcion para obtener los posts de un grupo
 */
export async function obtenerPostsGrupo(idGrupo) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/api/posts/grupo/${idGrupo}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': tokenUser
            }
        });
        const data = await response.json();
        return data;
    } catch (error) {
        console.log(error);
    }
}

/**
 * Función para crear un post en un grupo
 */
export function crearPostGrupo(contenido, idGrupo) {
    const response = fetch('http://127.0.0.1:8000/api/posts/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': tokenUser
        },
        body: JSON.stringify({
            content: contenido,
            group: idGrupo
        })
    });
    return response;
}

/**
 * Funcion para obtener los grupos de un usuario
 */
export async function obtenerGruposUsuario(username) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/api/grupos/${username}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': tokenUser
            }
        });
        const data = await response.json();
        return data;
    } catch (error) {
        console.log(error);
    }
}

/**
 * Funcion para obtener las listas de libros de un usuario por username
 */
export async function obtenerListasUsuario(username) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/api/listbook/${username}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': tokenUser
            }
        });
        const data = await response.json();
        return data;
    } catch (error) {
        console.log(error);
    }
}

/**
 * Funcion para obtener las listas de libros de un usuario por username
 */
export async function obtenerResenyasLibro(idLibro) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/api/resenya/${idLibro}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': tokenUser
            }
        });
        const data = await response.json();
        return data;
    } catch (error) {
        console.log(error);
    }
}

/**
 * Funcion para obtener los libros de un usuario escritor
 */
export async function obtenerLibrosEscritor(username) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/api/libros/user/${username}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': tokenUser
            },
        });
        const data = await response.json();
        return data;
    } catch (error) {
        console.log(error);
    }
}

/**
 * Función para crear una reseña de un libro
 * La reseña de le asignara al usuario que realiza la petición logueado
 */
export function crearResenya(idLibro, contenido, estrellas) {
    const response = fetch(`http://127.0.0.1:8000/api/resenya/${idLibro}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': tokenUser
        },
        body: JSON.stringify({
            book: idLibro,
            content: contenido,
            stars: estrellas
        })
    });
    return response;
}

/**
* Funcion para obtener las secciones de libros predefinidas en la base de datos
*/
export async function obtenerSeccionesLibros() {
    try {
        const response = await fetch(`http://127.0.0.1:8000/api/libros/secciones`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': tokenUser
            },
        });
        const data = await response.json();
        return data;
    } catch (error) {
        console.log(error);
    }
}

/**
 * Funcion para obtener entradas de un blog
 */
export async function obtenerEntradasBlog() {
    try {
        const response = await fetch(`http://127.0.0.1:8000/api/blog/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });
        const data = await response.json();
        return data;
    } catch (error) {
        console.log(error);
    }
}

/**
 * Funcion para crear notificaciones
 */
export function crearNotificacion(to_user, from_user, notification_type, post = null, comment = null) {
    return fetch('http://127.0.0.1:8000/api/notificaciones/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': tokenUser
        },
        body: JSON.stringify({
            to_user: to_user,
            from_user: from_user,
            post: post,
            notification_type: notification_type,
            comment: comment,
        })
    });
}

//Por cada mencion en un post se crea una notificacion
async function controlNotificaciones(post) {
    let usuariosMencionados = [];
    post.content.split(" ").forEach(element => {
        if (element.startsWith("@")) {
            usuariosMencionados.push(element.substring(1));
        }
    });

    usuariosMencionados.forEach(element => {
        //crearNotificacion(element, post.id_user, 1, post.id, null);
    });
}