
/**
 * Función que añade enlaces a los hashtags de un post
 */
export function formatearPost(post) {
    //Añadir enlaces a los hashtags y enlaces a las etiquetas de usuario
    let texto = post.content;
    let palabras = texto.split(' ');
    let textoNuevo = '';
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
    post.content = textoNuevo;

    // Añadir enlace al grupo si el post pertenece a un grupo
    let idGrupo = post.group;
    let nameGrupo = post.group_name;
    let spanHtml = '';

    if (post.group != null) {
        spanHtml = `<span class="post-grupo">en <a href="/grupo/${idGrupo}">${nameGrupo}</a></span>`;
        post.group = spanHtml;
    }else {
        post.group = '';
    }

    //Añadir enlace al post
    let linkPost = `<a href="/post/${post.id}">`;
   

    return post;
}

