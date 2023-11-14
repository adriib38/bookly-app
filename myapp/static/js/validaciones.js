
export const validarPost = (contenido) => {
    if (contenido.length == 0) {
        return {
            mensaje: 'El contenido del post no puede estar vacío',
            valido: false
        }
    } 

    if(contenido.length > 340) {
        return {
            mensaje: 'El contenido del post no puede superar los 340 caracteres',
            valido: false
        }
    }
    
    return {
        mensaje: 'El contenido del post no puede estar vacío',
        valido: true
    }
}