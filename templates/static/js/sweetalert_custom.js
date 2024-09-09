document.addEventListener('DOMContentLoaded', function() {
    const alertSuccess = document.querySelector('#alert-success');
    const alertError = document.querySelector('#alert-error');

    if (alertSuccess) {
        Swal.fire({
            icon: 'success',
            title: 'Sucesso',
            text: alertSuccess.getAttribute('data-message'),
            timer: 3000,
            showConfirmButton: false
        });
    }

    if (alertError) {
        Swal.fire({
            icon: 'error',
            title: 'Erro',
            text: alertError.getAttribute('data-message'),
            timer: 3000,
            showConfirmButton: false
        });
    }
});
