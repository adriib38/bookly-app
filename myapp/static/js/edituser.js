const btnEliminarCuenta = document.getElementById('eliminar-cuenta');
const username = document.getElementById('username').innerHTML;

const btnSolicitudEscritor = document.getElementById('solicitud-escritor');

btnEliminarCuenta.addEventListener('click', function (e) {
    const swalWithBootstrapButtons = Swal.mixin({
        customClass: {
          confirmButton: 'btn btn-success',
          cancelButton: 'btn btn-danger'
        },
        buttonsStyling: false
      })
      
      swalWithBootstrapButtons.fire({
        title: '¿Estás seguro?',
        showClass: {
          popup: 'fadeInUp'
        },
        hideClass: {
            popup: 'display-none'
        },
        text: "Eliminaremos todos tus datos de forma permanente.",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'No, cancelar',
        reverseButtons: true
      }).then((result) => {
        if (result.isConfirmed) {
            //Cuando se confirma la eliminación
          swalWithBootstrapButtons.fire(
            'Deleted!',
            'Your file has been deleted.',
            'success'
          )
            //Elperar 2 segundos y redireccionar
            setTimeout(function () {
                //Redireccionar a la página de eliminación
                location.href = '/delete/' + username + '/user';
            }, 2000);

        } else if (
          result.dismiss === Swal.DismissReason.cancel
        ) {
            //Cuando se cancela la eliminación
        }
      })
});

btnSolicitudEscritor.addEventListener('click', function (e) {
  Swal.fire({
    title: '¿Estás seguro?',
    text: "Por favor, envía una solicitud solo si crees que cumples con los requisitos.",
    showClass: {
      popup: 'fadeInUp'
    },
    hideClass: {
      popup: 'display-none'
    },
    showCancelButton: true,
    confirmButtonText: 'Enviar',
  }).then((result) => {
    /* Read more about isConfirmed, isDenied below */
    if (result.isConfirmed) {
      Swal.fire('¡Solicitud enviada!', '', 'success')
      //Elperar 2 segundos y redireccionar
      setTimeout(function () {
        location.href = '/writer/' + username + '/solicitud';
      }, 2000);

    } else if (result.isDenied) {
      
    }
  })
});


// Definir Dark/Light mode
const btnDarkMode = document.getElementById('toggle-dark-mode');
btnDarkMode.addEventListener('click', toggleDarkMode);

// Función para establecer una cookie
function setCookie(name, value, days) {
  var expires = "";
  var sameSite = "SameSite=None; Secure"; // Añade SameSite y Secure para las cookies en entornos seguros (HTTPS)

  if (days) {
    var date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    expires = "; expires=" + date.toUTCString();
  }

  document.cookie = name + "=" + (value || "") + expires + "; path=/;" + sameSite;
}

// Función para obtener el valor de una cookie
function getCookie(name) {
  var nameEQ = name + "=";
  var ca = document.cookie.split(';');
  for (var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1, c.length);
    }
    if (c.indexOf(nameEQ) == 0) {
      return c.substring(nameEQ.length, c.length);
    }
  }
  return null;
}

// Función para cambiar el modo oscuro
function toggleDarkMode() {
  var body = document.body;
  var isDarkModeEnabled = body.classList.toggle("dark-mode");

  btnDarkMode.innerHTML = isDarkModeEnabled ? 'Modo claro' : 'Modo oscuro';
  setCookie("darkMode", isDarkModeEnabled ? "enabled" : "disabled", 30);
}

// Obtener el estado almacenado en la cookie
(function checkDarkMode() {
  var darkModeCookie = getCookie("darkMode");
  if (darkModeCookie === "enabled") {
    document.body.classList.add("dark-mode");
    btnDarkMode.innerHTML = 'Modo claro';
  }
})();
