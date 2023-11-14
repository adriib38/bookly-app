//Importar funciones de peticionesAPI.js
import { obtenerListasUsuario } from './peticionesAPI.js';

const sectionListas = document.getElementById('section-listas-libros');
const username = document.getElementById('username').innerHTML;

obtenerListasUsuario(username).then(listas => {
    imprimirListas(listas);

}).catch(error => {
    console.log(error);
});

const nombresListas = {
    'leidos': 'Leídos',
    'por_leer': 'Por leer',
    'leyendo': 'Leyendo',
}

/**
 * Imprime las listas de libros
 */
function imprimirListas(listas) {
    sectionListas.innerHTML = '';
    //Por cada lista de libros
    for (let lista of listas) {
        let ulBooks = document.createElement('ul');
        //Si no hay libros en la lista
        if (lista.books.length == 0) {
            let liBook = document.createElement('li');
            liBook.innerHTML = 'No hay libros en la lista';
            ulBooks.appendChild(liBook);
        }

        //Por cada libro de la lista
        for (let book of lista.books) {
            let liBook = document.createElement('li');
            let aBook = document.createElement('a');
            aBook.href = `/libro/${book.book}`;
            aBook.textContent = book.book;
            liBook.appendChild(aBook);
            ulBooks.appendChild(liBook);
            
        }

        //Se imprime la información del libro
        let article = document.createElement('article');
        let h2 = document.createElement('h2');
        h2.textContent = nombresListas[lista.type_list];
        article.appendChild(h2);
        article.appendChild(ulBooks);

        sectionListas.appendChild(article);
    }
}

