/* ============================================================
   DASHBOARD_SECRETAIRE.JS
   ============================================================ */

window.addEventListener('DOMContentLoaded', () => {
    load_dashboard();
});

async function load_dashboard() {
    const annee = document.getElementById('anneeLabel')?.textContent || '';
    const [teachers, courses, activities, volume] = await Promise.all([
        apiFetch('/teachers/'),
        apiFetch('/courses/'),
        apiFetch(`/activities/?annee=${annee}`),
        apiFetch(`/activities/volume/?annee=${annee}`)
    ]);

    document.getElementById('statTeachers').textContent = teachers ? teachers.length : '—';
    document.getElementById('statCourses').textContent = courses ? courses.length : '—';
    document.getElementById('statActivities').textContent = activities ? activities.length : '—';

    if (volume) {
        const totalH = volume.reduce((s, r) => s + r.total_heures, 0);
        document.getElementById('statHeures').textContent = totalH.toFixed(1);
    }

    // Dernières activités (5 max)
    const tbody = document.getElementById('tbodyRecent');
    const recent = (activities || []).slice(0, 5);
    if (!recent.length) {
        tbody.innerHTML = `<tr><td colspan="5" class="table__loading">Aucune activité.</td></tr>`;
    } else {
        tbody.innerHTML = recent.map(a => `
      <tr>
        <td><strong>${a.enseignant_nom}</strong></td>
        <td>${a.resource_titre}</td>
        <td>${a.type_activite === 'creation'
                ? '<span class="badge badge--blue">Création</span>'
                : '<span class="badge badge--purple">Mise à jour</span>'}</td>
        <td><strong>${a.heures} h</strong></td>
        <td>${formatDate(a.date_activite)}</td>
      </tr>
    `).join('');
    }
}

window.load_teachers = async function () {
    const data = await apiFetch('/teachers/');
    const tbody = document.getElementById('tbodyTeachers');
    if (!tbody) return;
    if (!data || !data.length) {
        tbody.innerHTML = `<tr><td colspan="5" class="table__loading">Aucun enseignant.</td></tr>`;
        return;
    }
    tbody.innerHTML = data.map(t => `
    <tr>
      <td><strong>${t.full_name}</strong></td>
      <td>${gradeBadge(t.grade)}</td>
      <td>${statutBadge(t.statut)}</td>
      <td>${t.department_nom || '—'}</td>
      <td>${t.email}</td>
    </tr>
  `).join('');
};

window.load_courses = async function () {
    const data = await apiFetch('/courses/');
    const tbody = document.getElementById('tbodyCourses');
    if (!tbody) return;
    if (!data || !data.length) {
        tbody.innerHTML = `<tr><td colspan="5" class="table__loading">Aucun cours.</td></tr>`;
        return;
    }
    tbody.innerHTML = data.map(c => `
    <tr>
      <td><strong>${c.intitule}</strong></td>
      <td>${c.filiere}</td>
      <td><span class="badge badge--blue">${c.niveau}</span></td>
      <td><span class="badge badge--gray">${c.semestre}</span></td>
      <td>${c.nombre_heures} h</td>
    </tr>
  `).join('');
};

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

window.load_volume = async function () {
    const annee = document.getElementById('anneeLabel')?.textContent || '';
    const data = await apiFetch(`/activities/volume/?annee=${annee}`);
    const tbody = document.getElementById('tbodyVolume');
    if (!tbody) return;
    if (!data || !data.length) {
        tbody.innerHTML = `<tr><td colspan="6" class="table__loading">Aucune donnée.</td></tr>`;
        return;
    }
    tbody.innerHTML = data.map(r => `
    <tr>
      <td><strong>${r.enseignant_nom}</strong></td>
      <td>${gradeBadge('maitre_assistant')}</td>
      <td>${statutBadge('permanent')}</td>
      <td><strong>${r.total_heures.toFixed(1)} h</strong></td>
      <td>${formatNumber(r.taux_horaire)} FCFA</td>
      <td><strong>${formatNumber(Math.round(r.montant_du))} FCFA</strong></td>
    </tr>
  `).join('');
};

window.load_reports = async function () {
    const data = await apiFetch('/reports/');
    const tbody = document.getElementById('tbodyReports');
    if (!tbody) return;
    if (!data || !data.length) {
        tbody.innerHTML = `<tr><td colspan="6" class="table__loading">Aucun rapport.</td></tr>`;
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