
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
 * Función para crear un post
 */
export function obtenerLibros() {
    return new Promise((resolve, reject) => {
        fetch('http://127.0.0.1:8000/api/postusuarios/', {
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

//Obtener libros por genero en openlibrary api
export function obtenerLibrosPorGenero(genero, nLibros=3) {
    return new Promise((resolve, reject) => {
        fetch(`http://openlibrary.org/subjects/${genero}.json?limit=${nLibros}`, {
            method: 'GET',
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

//Obtener libros por titulo en openlibrary api
export function obtenerLibrosPorTitulo(titulo, nLibros=3) {
    return new Promise((resolve, reject) => {
        fetch(`http://openlibrary.org/search.json?title=${titulo}&limit=${nLibros}`, {
            method: 'GET',
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
 * Función para obtener el libro por su id
 */
export function obtenerLibroPorId(id) {
    return new Promise((resolve, reject) => {
      fetch(`https://openlibrary.org/works/${id}.json`, {
        method: 'GET',
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
 * Función para obtener el autor de un libro
 */
export function obtenerAutorPorId(id) {
    return new Promise((resolve, reject) => {
        fetch(`https://openlibrary.org${id}.json`, {
            method: 'GET',
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


