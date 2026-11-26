
document.getElementById("form_registro").addEventListener("submit", (e) => {
  
  
  let email = document.getElementById("email").value.trim().toLocaleLowerCase();
  let password = document.getElementById("password").value;
  let password2 = document.getElementById("password2").value;
  
  let errorPassword = document.getElementById("error-password");
  errorPassword.textContent = "";

  let errorEmail = document.getElementById("error-email");
  errorEmail.textContent = "";

  let formularioValido = true;

  const regexEmail = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  if (!regexEmail.test(email)) {
    errorEmail.textContent =
      "Debe introducir un email válido";
     formularioValido = false;
  }

  const regexPassword = /^(?=.*[a-zA-Z])(?=.*\d)(?=.*[= ])[a-zA-Z\d= ]{8,10}$/;
  // /^(?=.*[a-zA-Z])(?=.*\d)(?=.*[^a-zA-Z0-9]).{8,10}$/;
  if (!regexPassword.test(password) || !regexPassword.test(password2)) {
     errorPassword.textContent =
      "8-10 caracteres, un número y = o espacio.";
     formularioValido = false;
  }

  if (password != password2) {
    errorPassword.textContent = "Las contraseñas no coinciden.";
    formularioValido = false;
  }
  if (!formularioValido) {
    e.preventDefault();
  }
});
