let contenido = document.getElementsByClassName('post-contenido')[0];
let fecha = document.getElementsByClassName('post-fecha')[0];

//Añadir enlaces a los hashtags y enlaces a las etiquetas de usuario
let textoNuevo = '';
let palabras = contenido.textContent.split(' ');
palabras.forEach(palabra => {
    if (palabra.startsWith('#')){
        let palabraSinHashtag = palabra.substring(1);
        textoNuevo += `<a class="post-hashtag" href="/hashtag/${palabraSinHashtag}"><strong>${palabra}</strong></a> `;
    } else if (palabra.startsWith('@')) {
        let palabraSinArroba = palabra.substring(1);
        textoNuevo += `<a class="post-usuario" href="/user/${palabraSinArroba}"><strong>${palabra}</strong></a> `;
    } else {
        textoNuevo += `${palabra} `;
    }
});
contenido.innerHTML = textoNuevo;
