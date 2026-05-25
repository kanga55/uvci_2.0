/* ============================================================
   DASHBOARD.JS — Logique partagée entre les 3 dashboards
   Navigation sidebar, topbar, déconnexion
   ============================================================ */

const API_BASE = 'http://localhost:8000/api';

// ---- Récupérer l'utilisateur connecté ----
const user = JSON.parse(sessionStorage.getItem('user') || '{}');

window.addEventListener('DOMContentLoaded', () => {
    initUser();
    initNav();
    initMobileSidebar();
    protectPage();
});

// ---- Afficher le nom de l'utilisateur ----
function initUser() {
    const name = `${user.first_name || ''} ${user.last_name || ''}`.trim() || 'Utilisateur';
    const initial = name.charAt(0).toUpperCase();

    const elName = document.getElementById('userName');
    const elAvatar = document.getElementById('userAvatar');
    const elGreet = document.getElementById('greetName');

    if (elName) elName.textContent = name;
    if (elAvatar) elAvatar.textContent = initial;
    if (elGreet) elGreet.textContent = user.first_name || 'Admin';
}

// ---- Navigation entre pages ----
function initNav() {
    const navItems = document.querySelectorAll('.nav-item[data-page]');
    const pages = document.querySelectorAll('.page');
    const pageTitle = document.getElementById('pageTitle');

    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const target = item.dataset.page;

            // Activer le lien
            navItems.forEach(n => n.classList.remove('nav-item--active'));
            item.classList.add('nav-item--active');

            // Afficher la page
            pages.forEach(p => p.classList.remove('page--active'));
            const targetPage = document.getElementById(`page-${target}`);
            if (targetPage) targetPage.classList.add('page--active');

            // Mettre à jour le titre
            if (pageTitle) pageTitle.textContent = item.textContent.trim();

            // Fermer sidebar sur mobile
            closeSidebar();

            // Charger les données de la page si besoin
            if (typeof window[`load_${target}`] === 'function') {
                window[`load_${target}`]();
            }
        });
    });
}

// ---- Sidebar mobile ----
function initMobileSidebar() {
    const menuBtn = document.getElementById('menuBtn');
    const sidebarClose = document.getElementById('sidebarClose');
    const overlay = document.getElementById('overlay');
    const sidebar = document.getElementById('sidebar');

    if (menuBtn) menuBtn.addEventListener('click', openSidebar);
    if (sidebarClose) sidebarClose.addEventListener('click', closeSidebar);
    if (overlay) overlay.addEventListener('click', closeSidebar);

    // Déconnexion
    const btnLogout = document.getElementById('btnLogout');
    if (btnLogout) btnLogout.addEventListener('click', logout);
}

function openSidebar() {
    document.getElementById('sidebar')?.classList.add('sidebar--open');
    document.getElementById('overlay')?.classList.add('overlay--visible');
}

function closeSidebar() {
    document.getElementById('sidebar')?.classList.remove('sidebar--open');
    document.getElementById('overlay')?.classList.remove('overlay--visible');
}

// ---- Déconnexion ----
async function logout() {
    try {
        await fetch(`${API_BASE}/accounts/logout/`, {
            method: 'POST',
            credentials: 'include'
        });
    } catch (_) { }
    sessionStorage.clear();
    window.location.href = '../page/login.html';
}

// ---- Protection de page (redirection si non connecté) ----
function protectPage() {
    if (!user || !user.role) {
        window.location.href = '../page/login.html';
    }
}

// ---- Utilitaires API ----
async function apiFetch(endpoint) {
    try {
        const res = await fetch(`${API_BASE}${endpoint}`, {
            credentials: 'include',
            headers: { 'Content-Type': 'application/json' }
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return await res.json();
    } catch (err) {
        console.error(`[UVCI API] ${endpoint}`, err);
        return null;
    }
}

// ---- Formater un nombre ----
function formatNumber(n) {
    if (n === null || n === undefined || n === '—') return '—';
    return Number(n).toLocaleString('fr-FR');
}

// ---- Formater une date ----
function formatDate(dateStr) {
    if (!dateStr) return '—';
    return new Date(dateStr).toLocaleDateString('fr-FR');
}

// ---- Badge HTML selon rôle / grade / statut ----
function roleBadge(role) {
    const map = {
        admin: ['badge--blue', 'Admin'],
        secretaire: ['badge--purple', 'Secrétaire'],
        enseignant: ['badge--green', 'Enseignant'],
    };
    const [cls, label] = map[role] || ['badge--gray', role];
    return `<span class="badge ${cls}">${label}</span>`;
}

function gradeBadge(grade) {
    const map = {
        assistant: ['badge--gray', 'Assistant'],
        maitre_assistant: ['badge--blue', 'M. Assistant'],
        professeur: ['badge--gold', 'Professeur'],
    };
    const [cls, label] = map[grade] || ['badge--gray', grade];
    return `<span class="badge ${cls}">${label}</span>`;
}

function statutBadge(statut) {
    const map = {
        permanent: ['badge--green', 'Permanent'],
        vacataire: ['badge--gold', 'Vacataire'],
    };
    const [cls, label] = map[statut] || ['badge--gray', statut];
    return `<span class="badge ${cls}">${label}</span>`;
}


// Récupérer le cookie CSRF
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return '';
}

// Version POST de apiFetch (avec CSRF)
async function apiPost(endpoint, body) {
    try {
        const res = await fetch(`${API_BASE}${endpoint}`, {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(body)
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return await res.json();
    } catch (err) {
        console.error(`[UVCI API POST] ${endpoint}`, err);
        return null;
    }
}