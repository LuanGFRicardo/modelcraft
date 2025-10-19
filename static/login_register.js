// Seleciona os elementos
const loginForm = document.getElementById('login-form');
const registerForm = document.getElementById('register-form');
const goToRegister = document.getElementById('go-to-register');
const goToLogin = document.getElementById('go-to-login');

// Alterna para o formulário de registro
goToRegister.addEventListener('click', (e) => {
    e.preventDefault();

    // Animação de saída para o login
    loginForm.classList.add('fade-out');
    setTimeout(() => {
        loginForm.style.display = 'none';
        loginForm.classList.remove('fade-out');

        // Mostra o formulário de registro com animação de entrada
        registerForm.style.display = 'block';
        registerForm.classList.add('fade-in');
    }, 500); // Tempo da animação
});

// Alterna para o formulário de login
goToLogin.addEventListener('click', (e) => {
    e.preventDefault();

    // Animação de saída para o registro
    registerForm.classList.add('fade-out');
    setTimeout(() => {
        registerForm.style.display = 'none';
        registerForm.classList.remove('fade-out');

        // Mostra o formulário de login com animação de entrada
        loginForm.style.display = 'block';
        loginForm.classList.add('fade-in');
    }, 500); // Tempo da animação
});
