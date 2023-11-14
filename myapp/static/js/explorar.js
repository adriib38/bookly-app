//Importar funciones de peticionesAPI.js
import { obtenerLibros, obtenerLibrosPorGenero, obtenerLibroPorId } from './peticionesLibros.js';
import { obtenerSeccionesLibros } from './peticionesAPI.js';

const divGeneros = document.getElementById('explorar-generos');
const divSecciones = document.getElementById('explorar-secciones');

let todos = {};

//Lista de categorias de openlibrary
let categorias = ["love", "horror", "fantasy", "kids", "adventure", "romance", "children"];

// Comprobar si ya existe una cookie con los datos
const librosCookie = getCookieOrUndefined('librosPorCategoria');
//Obtener libros de categorias e imprimir 
if(false) {
//if(librosCookie) {
    // Si la cookie ya existe, se utilizan los datos almacenados
    todos = JSON.parse(librosCookie);
    imprimirLibros(todos);
} else {
    // Si no existe la cookie, se realizan las peticiones al servidor
    categorias.forEach(categoria => {
        obtenerLibrosPorGenero(categoria, 6).then(libros => {
            todos[categoria] = libros.works;

            // Guardar los datos en una cookie con una duración de 1 día
            Cookies.set('librosPorCategoria', JSON.stringify(todos), { expires: 1 });

            imprimirLibros(todos);
        }).catch(error => {
            console.log(error);
        });
    });
}

function getCookieOrUndefined(clave) {
    //Obtener valor de la cookie
    var cookies = document.cookie.split(';');
    var valor = undefined;
    for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        if (cookie.indexOf(clave + '=') === 0) {
            valor = cookie.substring(clave.length + 1, cookie.length);
            break;
        }
    }
    return valor;
}

// Imprimir los posts del usuario
function imprimirLibros(todos) {
    divGeneros.innerHTML = '';
    //Por cada genero
    for (let genero in todos) {
        let divGenero = document.createElement('section');
        divGenero.classList.add('card-deck');
        divGenero.id = genero;

        //Titulo del genero
        let tituloGenero = document.createElement('h3');
        tituloGenero.classList.add('anchor100');
        tituloGenero.classList.add('titulo-del-genero');
        //Remplazar _ por espacio
        genero = genero.replace(/_/g, ' ');

        tituloGenero.innerHTML = genero;
        divGenero.appendChild(tituloGenero);

        //Por cada libro
        for (let libro in todos[genero]) {
            let divLibro = document.createElement('article');
            divLibro.classList.add('card');
            divLibro.id = todos[genero][libro].key;

            let id = todos[genero][libro].key;
            id = id.replace('/works/', '');
            divLibro.innerHTML += `
                <img class="card-img" src="https://covers.openlibrary.org/b/id/${todos[genero][libro].cover_id}-M.jpg" class="card-img-top">
                <a href="/libro/${id}">
                    <h3 class="card-titulo">${todos[genero][libro].title}</h3>
                </a>
            `;

            divGenero.appendChild(divLibro);
        }
        //Agregar genero al div de generos
        divGeneros.appendChild(divGenero);
    }
}

//Obtener secciones predefinidas de libros de la base de datos
obtenerSeccionesLibros().then(secciones => {
    imprimirSecciones(secciones);
}).catch(error => {
    console.log(error);
});

//Imprimir secciones predefinidas de libros
async function imprimirSecciones(secciones) {
    divSecciones.innerHTML = '';
    for (const seccion of secciones) {
      const {title, color, libros} = seccion;
      const divSeccion = document.createElement('section');
      divSeccion.id = title;
      divSeccion.classList.add('seccion-libros-predefinida');
  
      //Titulo de la seccion
      const tituloSeccion = document.createElement('h2');
      tituloSeccion.id = title;
      tituloSeccion.classList.add('titulo-seccion', `underline-${color}`);
      tituloSeccion.innerHTML = title;
      divSeccion.appendChild(tituloSeccion);
  
      //Deck de libros
      const seccionDeck = document.createElement('section');
      seccionDeck.classList.add('card-deck');
      
      //Por cada libro
      for (const {id} of libros) {
        const libroInfo = await obtenerNombreYPostadaLibro(id);
        const articleLibro = document.createElement('article');
        articleLibro.classList.add('card');
        articleLibro.innerHTML = `
          <img class="card-img" src="https://covers.openlibrary.org/b/id/${libroInfo.portadaId}-M.jpg" class="card-img-top">
          <a href="/libro/${id}">
            <h3 class="card-titulo">${libroInfo.titulo}</h3>
          </a>
        `;
        seccionDeck.appendChild(articleLibro);
      }
      divSeccion.appendChild(seccionDeck);
      divSecciones.appendChild(divSeccion);
    }
  }
  
/**
 * Funcion para obtener el nombre de un libro
 */
async function obtenerNombreYPostadaLibro(id) {
    try {
        const libro = await obtenerLibroPorId(id);
        return {
            titulo: libro.title,
            portadaId: libro.covers[0]
        }
    } catch (error) {
        console.log(error);
    }
}