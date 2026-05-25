/* ============================================================
   DASHBOARD_ADMIN.JS — Données et actions spécifiques à l'admin
   ============================================================ */

window.addEventListener('DOMContentLoaded', () => {
    load_dashboard();
    initSearch();
    initReportCards();

    document.getElementById('btnRefresh')?.addEventListener('click', load_dashboard);
});

// ============================================================
// DASHBOARD — Stats + tableau volume horaire
// ============================================================
async function load_dashboard() {
    const annee = document.getElementById('anneeLabel')?.textContent || '';

    // Charger en parallèle
    const [teachers, courses, volume] = await Promise.all([
        apiFetch('/teachers/'),
        apiFetch('/courses/'),
        apiFetch(`/activities/volume/?annee=${annee}`)
    ]);

    // Stats
    document.getElementById('statTeachers').textContent =
        teachers ? teachers.length : '—';
    document.getElementById('statCourses').textContent =
        courses ? courses.length : '—';

    if (volume) {
        const totalH = volume.reduce((s, r) => s + r.total_heures, 0);
        const totalM = volume.reduce((s, r) => s + r.montant_du, 0);
        document.getElementById('statHeures').textContent = totalH.toFixed(1);
        document.getElementById('statMontant').textContent = formatNumber(Math.round(totalM));
    }

    // Tableau
    renderVolumeTable(volume || []);
}

function renderVolumeTable(data) {
    const tbody = document.getElementById('tbodyVolume');
    if (!tbody) return;

    if (!data.length) {
        tbody.innerHTML = `<tr><td colspan="6" class="table__loading">Aucune donnée disponible.</td></tr>`;
        return;
    }

    tbody.innerHTML = data.map(r => `
    <tr>
      <td><strong>${r.enseignant_nom}</strong></td>
      <td>${gradeBadge(r.grade.toLowerCase().replace(' ', '_').replace('-', '_').replace('î', 'i').replace('maître', 'maitre'))}</td>
      <td>${statutBadge(r.statut.toLowerCase())}</td>
      <td><strong>${r.total_heures.toFixed(1)} h</strong></td>
      <td>${formatNumber(r.taux_horaire)} FCFA</td>
      <td><strong>${formatNumber(Math.round(r.montant_du))} FCFA</strong></td>
    </tr>
  `).join('');
}

// ---- Recherche dans le tableau ----
function initSearch() {
    document.getElementById('searchTeacher')?.addEventListener('input', function () {
        const val = this.value.toLowerCase();
        document.querySelectorAll('#tbodyVolume tr').forEach(tr => {
            tr.style.display = tr.textContent.toLowerCase().includes(val) ? '' : 'none';
        });
    });
}

// ============================================================
// UTILISATEURS
// ============================================================
window.load_users = async function () {
    const data = await apiFetch('/accounts/users/');
    const tbody = document.getElementById('tbodyUsers');
    if (!tbody) return;

    if (!data || !data.length) {
        tbody.innerHTML = `<tr><td colspan="4" class="table__loading">Aucun utilisateur.</td></tr>`;
        return;
    }

    tbody.innerHTML = data.map(u => `
    <tr>
      <td><strong>${u.first_name} ${u.last_name}</strong></td>
      <td>${u.email}</td>
      <td>${roleBadge(u.role)}</td>
      <td>${u.is_active
            ? '<span class="badge badge--green">Actif</span>'
            : '<span class="badge badge--red">Inactif</span>'}</td>
    </tr>
  `).join('');
};

// ============================================================
// ENSEIGNANTS
// ============================================================
window.load_teachers = async function () {
    const data = await apiFetch('/teachers/');
    const tbody = document.getElementById('tbodyTeachers');
    if (!tbody) return;

    if (!data || !data.length) {
        tbody.innerHTML = `<tr><td colspan="6" class="table__loading">Aucun enseignant.</td></tr>`;
        return;
    }

    tbody.innerHTML = data.map(t => `
    <tr>
      <td><strong>${t.full_name}</strong></td>
      <td>${gradeBadge(t.grade)}</td>
      <td>${statutBadge(t.statut)}</td>
      <td>${t.department_nom || '—'}</td>
      <td>${t.email}</td>
      <td>${formatNumber(t.taux_horaire)} FCFA</td>
    </tr>
  `).join('');
};

// ============================================================
// COURS
// ============================================================
window.load_courses = async function () {
    const data = await apiFetch('/courses/');
    const tbody = document.getElementById('tbodyCourses');
    if (!tbody) return;

    if (!data || !data.length) {
        tbody.innerHTML = `<tr><td colspan="6" class="table__loading">Aucun cours.</td></tr>`;
        return;
    }

    tbody.innerHTML = data.map(c => `
    <tr>
      <td><strong>${c.intitule}</strong></td>
      <td>${c.filiere}</td>
      <td><span class="badge badge--blue">${c.niveau}</span></td>
      <td><span class="badge badge--gray">${c.semestre}</span></td>
      <td>${c.nombre_heures} h</td>
      <td>${c.credits} crédits</td>
    </tr>
  `).join('');
};

// ============================================================
// ACTIVITÉS
// ============================================================
window.load_activities = async function () {
    const data = await apiFetch('/activities/');
    const tbody = document.getElementById('tbodyActivities');
    if (!tbody) return;

    if (!data || !data.length) {
        tbody.innerHTML = `<tr><td colspan="6" class="table__loading">Aucune activité.</td></tr>`;
        return;
    }

    tbody.innerHTML = data.map(a => `
    <tr>
      <td><strong>${a.enseignant_nom}</strong></td>
      <td>${a.resource_titre}</td>
      <td>${a.type_activite === 'creation'
            ? '<span class="badge badge--blue">Création</span>'
            : '<span class="badge badge--purple">Mise à jour</span>'}</td>
      <td><strong>${a.heures} h</strong></td>
      <td>${formatDate(a.date_activite)}</td>
      <td>${a.annee_academique}</td>
    </tr>
  `).join('');
};

// ============================================================
// RAPPORTS
// ============================================================
window.load_reports = async function () {
    const data = await apiFetch('/reports/');
    const tbody = document.getElementById('tbodyReports');
    if (!tbody) return;

    if (!data || !data.length) {
        tbody.innerHTML = `<tr><td colspan="6" class="table__loading">Aucun rapport généré.</td></tr>`;
        return;
    }

    tbody.innerHTML = data.map(r => `
    <tr>
      <td>${r.type_label}</td>
      <td>${r.enseignant_nom || '—'}</td>
      <td>${r.annee_academique}</td>
      <td>${r.total_heures} h</td>
      <td>${formatNumber(Math.round(r.montant_total))} FCFA</td>
      <td>${formatDate(r.date_generation)}</td>
    </tr>
  `).join('');
};

// ============================================================
// PARAMÈTRES — Années académiques
// ============================================================
window.load_settings = async function () {
    const data = await apiFetch('/activities/annees/');
    const container = document.getElementById('anneesList');
    if (!container) return;

    if (!data || !data.length) {
        container.innerHTML = '<p style="color:var(--gray-muted);font-size:13px;">Aucune année configurée.</p>';
        return;
    }

    container.innerHTML = data.map(a => `
    <div class="annee-item ${a.en_cours ? 'annee-item--active' : ''}">
      <span>${a.libelle}</span>
      ${a.en_cours
            ? '<span class="badge badge--gold">En cours</span>'
            : `<span style="font-size:12px;color:var(--gray-muted)">${formatDate(a.date_debut)} — ${formatDate(a.date_fin)}</span>`}
    </div>
  `).join('');
};

// ============================================================
// CARDS RAPPORTS (cliquables)
// ============================================================
function initReportCards() {
    document.getElementById('rptPaiement')?.addEventListener('click', () => generateReport('paiement'));
    document.getElementById('rptGlobal')?.addEventListener('click', () => generateReport('global'));
    document.getElementById('rptStats')?.addEventListener('click', () => generateReport('statistique'));
}

async function generateReport(type) {
    const annee = document.getElementById('anneeLabel')?.textContent || '2025-2026';
    try {
        const res = await fetch(`${API_BASE}/reports/generate/`, {
            method: 'POST',
            credentials: 'include',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ type_report: type, annee_academique: annee })
        });
        if (res.ok) {
            alert(`Rapport "${type}" généré avec succès !`);
            load_reports();
        }
    } catch (err) {
        console.error(err);
    }
}