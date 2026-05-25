/* ============================================================
   LOGIN.JS — Logique de connexion UVCI
   Appelle POST /api/accounts/login/ et redirige selon le rôle
   ============================================================ */

const API_BASE = 'http://localhost:8000/api';

// --- Éléments DOM ---
const emailInput = document.getElementById('email');
const pwdInput = document.getElementById('password');
const btnLogin = document.getElementById('btnLogin');
const btnLoader = document.getElementById('btnLoader');
const btnText = document.querySelector('.btn-submit__text');
const btnArrow = document.querySelector('.btn-submit__arrow');
const alertBox = document.getElementById('alertError');
const alertMsg = document.getElementById('alertMessage');
const togglePwd = document.getElementById('togglePwd');
const iconEye = document.getElementById('iconEye');
const iconEyeOff = document.getElementById('iconEyeOff');
const demoBtns = document.querySelectorAll('.demo-btn');

// --- Afficher / cacher le mot de passe ---
togglePwd.addEventListener('click', () => {
    const isHidden = pwdInput.type === 'password';
    pwdInput.type = isHidden ? 'text' : 'password';
    iconEye.style.display = isHidden ? 'none' : 'block';
    iconEyeOff.style.display = isHidden ? 'block' : 'none';
});

// --- Boutons démo : pré-remplir le formulaire ---
demoBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        emailInput.value = btn.dataset.email;
        pwdInput.value = btn.dataset.pwd;
        hideAlert();
    });
});

// --- Masquer l'alerte quand l'utilisateur retape ---
emailInput.addEventListener('input', hideAlert);
pwdInput.addEventListener('input', hideAlert);

// --- Soumission avec Enter ---
document.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') handleLogin();
});

// --- Clic sur le bouton ---
btnLogin.addEventListener('click', handleLogin);

// ============================================================
// Fonction principale de connexion
// ============================================================
async function handleLogin() {
    const email = emailInput.value.trim();
    const password = pwdInput.value;

    if (!email || !password) {
        showAlert('Veuillez renseigner votre email et votre mot de passe.');
        return;
    }
    if (!isValidEmail(email)) {
        showAlert('Adresse email invalide.');
        return;
    }

    setLoading(true);

    try {
        // Étape 1 : récupérer le token CSRF depuis Django
        await fetch(`${API_BASE}/accounts/csrf/`, {
            credentials: 'include'
        });

        // Lire le cookie csrftoken
        const csrfToken = getCookie('csrftoken');

        // Étape 2 : envoyer le login avec le token
        const response = await fetch(`${API_BASE}/accounts/login/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            credentials: 'include',
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok) {
            sessionStorage.setItem('user', JSON.stringify(data.user));
            redirectByRole(data.user.role);
        } else {
            showAlert(extractError(data));
        }

    } catch (err) {
        showAlert('Serveur injoignable. Vérifiez que Django tourne sur le port 8000.');
        console.error('[UVCI Login]', err);
    } finally {
        setLoading(false);
    }
}

// Lire un cookie par son nom
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return '';
}

// ============================================================
// Redirection selon le rôle de l'utilisateur
// ============================================================
function redirectByRole(role) {
    const routes = {
        admin: '../page/dashboard_admin.html',
        secretaire: '../page/dashboard_secretaire.html',
        enseignant: '../page/dashboard_enseignant.html',
    };
    const destination = routes[role] || '../page/dashboard_admin.html';
    window.location.href = destination;
}

// ============================================================
// Utilitaires
// ============================================================
function showAlert(message) {
    alertMsg.textContent = message;
    alertBox.style.display = 'flex';
}

function hideAlert() {
    alertBox.style.display = 'none';
}

function setLoading(loading) {
    btnLogin.disabled = loading;
    btnText.style.display = loading ? 'none' : 'inline';
    btnLoader.style.display = loading ? 'flex' : 'none';
    btnArrow.style.display = loading ? 'none' : 'block';
}

function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function extractError(data) {
    // DRF peut renvoyer les erreurs sous plusieurs formes
    if (typeof data === 'string') return data;
    if (data.detail) return data.detail;
    if (data.non_field_errors) return data.non_field_errors[0];
    if (data.email) return data.email[0];
    if (data.password) return data.password[0];
    return 'Une erreur est survenue. Réessayez.';
}