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
  body.classList.toggle("dark-mode");

  // Guardar el estado del modo oscuro en una cookie
  var isDarkModeEnabled = body.classList.contains("dark-mode");
  setCookie("darkMode", isDarkModeEnabled ? "enabled" : "disabled", 30);
}

// Obtener el estado almacenado en la cookie
function checkDarkMode() {
  var darkModeCookie = getCookie("darkMode");
  if (darkModeCookie === "enabled") {
    document.body.classList.add("dark-mode");
  }
}

// Comprobar el modo oscuro al cargar la página
checkDarkMode();
