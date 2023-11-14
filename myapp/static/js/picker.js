const btnEmojis = document.getElementById('btn-emojis');
const boxEmojis = document.getElementById('box-emojis');

//Picker de emojis
const pickerOptions = { 
    onEmojiSelect: function(emoji) {
        let contenidoPost = document.getElementById('contenido-post');
        contenidoPost.value += emoji.native;
    },
    title: 'Elige un emoji',
    locale: 'es',
    set: 'native',
}
export const picker = new EmojiMart.Picker(pickerOptions)

//Abrir contenedor de emojis al hacer click en el boton
btnEmojis.addEventListener('click', () => {
    //Mostrar contenedor de emojis al lado del boton
    boxEmojis.appendChild(picker);
});

//Cerrar contenedor de emojis al hacer click fuera
document.addEventListener('mousedown', (e) => {
    if(e.target != btnEmojis && e.target.localName != 'em-emoji-picker'){
        boxEmojis.innerHTML = '';
    }
});
