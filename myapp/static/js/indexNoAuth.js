import { obtenerEntradasBlog } from './peticionesAPI.js';

const seccionEntradas = document.getElementById('box-blog-posts');

obtenerEntradasBlog().then(data => {
    data.forEach(entrada => {
        //Reducir el contenido de la entrada a 200 caracteres
        entrada.content = entrada.content.substring(0, 200) + '...';

        let article = document.createElement('article');
        article.classList.add('blog-post');
        article.classList.add('max-width-600');
        article.innerHTML = `
            <div class="contenido-entrada">
                <h3>${entrada.title}</h3>
                <p>${entrada.content}</p>
                <a href="blog/${entrada.id}">Leer más</a>
            </div>
        `;
        seccionEntradas.appendChild(article);        
    });
});


console.log('######    #####    #####   ### ###  ####     ###  ###\n\
 ##  ##  ### ###  ### ###   ## ##    ##       ##  ##\n\
 ##  ##  ##   ##  ##   ##   ####     ##        ####\n\
 #####   ##   ##  ##   ##   ###      ##         ##\n\
 ##  ##  ##   ##  ##   ##   ####     ##         ##\n\
 ##  ##  ### ###  ### ###   ## ##    ##  ##     ##\n\
######    #####    #####   ### ###  #######    ####');

console.log('𝑷𝒐𝒓 𝒂𝒅𝒓𝒊𝒂𝒏 𝒃𝒆𝒏𝒊𝒕𝒆𝒛');
console.log('---------------------------------');
console.log('𝑫𝒆𝒗𝒆𝒍𝒐𝒑𝒆𝒅 𝒘𝒊𝒕𝒉 🤍 𝒊𝒏 𝑽𝒂𝒍𝒆̀𝒏𝒄𝒊𝒂');
console.log('---------------------------------');
console.log('Agradecimientos a Alex Torres.');
console.log('---------------------------------');
console.log('https://linktr.ee/adrianbnitez');
console.log('https://linktr.ee/adrianbnitez');
console.log('https://linktr.ee/adrianbnitez');
console.log('https://linktr.ee/adrianbnitez');
console.log('https://linktr.ee/adrianbnitez');
