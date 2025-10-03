document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');
    if (loginForm){
        loginForm.addEventListener('submit', function(event) {
            const usuario = document.getElementById('login-usuario').value;
            const password = document.getElementById('login-password').value;
            let valid = true;

            if (!usuario.value.trim()){
                usuario.setCustomValidty('Por favor ingrese su nombre de usuario');
                usuario.reportValidity();
                valid = false;

            } else{
                usuario.setCustomValidity('');
            }

             if (!password.value.trim()){
                password.setCustomValidty('Por favor ingrese su contraseña');
                password.reportValidity();
                valid = false;

            } else{
                password.setCustomValidity('');
            }

            if (!valid){
                event.preventDefault(); // Evita el envío del formulario si hay errores
            }

            
    });

 }
    
   
});