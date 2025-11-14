(function(){
     'use strict'

     //Para validar los formualarios
     var forms = document.querySelectorAll('.needs-validation')

     //Bucle
    Array.prototype.slice.call(forms)
    .forEach(function (form) {
      form.addEventListener('submit', function (event) {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }

        form.classList.add('was-validated')
      }, false)
    })

})()