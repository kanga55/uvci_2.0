/* ============================================================
   DASHBOARD_ENSEIGNANT.JS
   L'enseignant ne voit que ses propres données.
   On récupère d'abord son profil Teacher via /api/accounts/me/
   puis on filtre toutes les requêtes sur son enseignant_id.
   ============================================================ */

let myTeacherId = null;
let myTeacher = null;

window.addEventListener('DOMContentLoaded', async () => {
    await initTeacherProfile();
    load_dashboard();
});

// ---- Récupérer le profil Teacher lié au compte connecté ----
async function initTeacherProfile() {
    // On récupère tous les enseignants et on cherche celui qui correspond à l'email
    const teachers = await apiFetch('/teachers/');
    if (!teachers) return;

    const userEmail = user.email;
    myTeacher = teachers.find(t => t.email === userEmail) || null;

    if (myTeacher) {
        myTeacherId = myTeacher.id;
        renderProfile(myTeacher);
    }
}

function renderProfile(t) {
    const initial = t.prenom ? t.prenom.charAt(0).toUpperCase() : '?';
    const el = (id) => document.getElementById(id);

    if (el('profileAvatar')) el('profileAvatar').textContent = initial;
    if (el('profileName')) el('profileName').textContent = t.full_name;
    if (el('profileGrade')) el('profileGrade').textContent = t.grade;
    if (el('profileDept')) el('profileDept').textContent = t.department_nom || '—';
    if (el('profileTaux')) el('profileTaux').textContent = formatNumber(t.taux_horaire) + ' FCFA';
    if (el('profileStatut')) el('profileStatut').textContent = t.statut;
}

// ============================================================
// DASHBOARD
// ============================================================
async function load_dashboard() {
    if (!myTeacherId) {
        document.getElementById('statMyActivities').textContent = '0';
        document.getElementById('statMyHeures').textContent = '0';
        document.getElementById('statMyMontant').textContent = '0';
        document.getElementById('statHeuresComp').textContent = '0';
        return;
    }

    const annee = document.getElementById('anneeLabel')?.textContent || '';

    const [activities, volume] = await Promise.all([
        apiFetch(`/activities/?enseignant=${myTeacherId}&annee=${annee}`),
        apiFetch(`/activities/volume/?annee=${annee}`)
    ]);

    // Stats
    document.getElementById('statMyActivities').textContent =
        activities ? activities.length : '0';

    // Volume de l'enseignant connecté
    const myVolume = volume ? volume.find(v => v.enseignant_id === myTeacherId) : null;
    const totalH = myVolume ? myVolume.total_heures : 0;
    const montant = myVolume ? myVolume.montant_du : 0;
    const taux = myTeacher ? parseFloat(myTeacher.taux_horaire) : 0;
    // Heures complémentaires = heures au-delà du seuil standard (exemple : 192h)
    const seuilStandard = 192;
    const heuresComp = Math.max(0, totalH - seuilStandard);

    document.getElementById('statMyHeures').textContent = totalH.toFixed(1);
    document.getElementById('statMyMontant').textContent = formatNumber(Math.round(montant));
    document.getElementById('statHeuresComp').textContent = heuresComp.toFixed(1);

    // Dernières activités
    const tbody = document.getElementById('tbodyRecent');
    const recent = (activities || []).slice(0, 5);

    if (!recent.length) {
        tbody.innerHTML = `<tr><td colspan="5" class="table__loading">Aucune activité enregistrée.</td></tr>`;
    } else {
        tbody.innerHTML = recent.map(a => `
      <tr>
        <td><strong>${a.resource_titre}</strong></td>
        <td>${a.type_activite === 'creation'
                ? '<span class="badge badge--blue">Création</span>'
                : '<span class="badge badge--purple">Mise à jour</span>'}</td>
        <td><span class="badge badge--gray">${a.complexite || '—'}</span></td>
        <td><strong>${a.heures} h</strong></td>
        <td>${formatDate(a.date_activite)}</td>
      </tr>
    `).join('');
    }
}

// ============================================================
// MES ACTIVITÉS
// ============================================================
window.load_activities = async function () {
    if (!myTeacherId) return;
    const data = await apiFetch(`/activities/?enseignant=${myTeacherId}`);
    const tbody = document.getElementById('tbodyActivities');
    if (!tbody) return;

    if (!data || !data.length) {
        tbody.innerHTML = `<tr><td colspan="5" class="table__loading">Aucune activité.</td></tr>`;
        return;
    }

    tbody.innerHTML = data.map(a => `
    <tr>
      <td><strong>${a.resource_titre}</strong></td>
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
// MON VOLUME HORAIRE
// ============================================================
window.load_volume = async function () {
    const container = document.getElementById('volumeContent');
    if (!container || !myTeacherId) return;

    // On récupère toutes les activités sans filtre d'année
    // pour regrouper par année académique
    const data = await apiFetch(`/activities/?enseignant=${myTeacherId}`);

    if (!data || !data.length) {
        container.innerHTML = '<p style="color:var(--gray-muted);font-size:13px;">Aucune activité enregistrée.</p>';
        return;
    }

    // Regrouper par année académique
    const byAnnee = {};
    data.forEach(a => {
        if (!byAnnee[a.annee_academique]) {
            byAnnee[a.annee_academique] = { total: 0, count: 0 };
        }
        byAnnee[a.annee_academique].total += parseFloat(a.heures);
        byAnnee[a.annee_academique].count += 1;
    });

    const taux = myTeacher ? parseFloat(myTeacher.taux_horaire) : 0;

    const html = Object.entries(byAnnee)
        .sort(([a], [b]) => b.localeCompare(a))
        .map(([annee, info]) => `
      <div class="volume-annee-block">
        <div class="volume-annee-block__header">
          <h4>${annee}</h4>
          <span class="badge badge--gold">${info.count} activité${info.count > 1 ? 's' : ''}</span>
        </div>
        <div class="volume-annee-block__body">
          <div class="volume-stat">
            <span class="volume-stat__label">Total heures</span>
            <span class="volume-stat__value">${info.total.toFixed(1)} h</span>
          </div>
          <div class="volume-stat">
            <span class="volume-stat__label">Taux horaire</span>
            <span class="volume-stat__value">${formatNumber(taux)} FCFA</span>
          </div>
          <div class="volume-stat">
            <span class="volume-stat__label">Montant estimé</span>
            <span class="volume-stat__value">${formatNumber(Math.round(info.total * taux))} FCFA</span>
          </div>
          <div class="volume-stat">
            <span class="volume-stat__label">Heures complémentaires</span>
            <span class="volume-stat__value">${Math.max(0, info.total - 192).toFixed(1)} h</span>
          </div>
        </div>
      </div>
    `).join('');

    container.innerHTML = `<div class="volume-detail">${html}</div>`;
};

// ============================================================
// MON RÉCAPITULATIF (rapports générés par l'admin)
// ============================================================
window.load_recap = async function () {
    const data = await apiFetch('/reports/');
    const tbody = document.getElementById('tbodyRecap');
    if (!tbody) return;

    // Filtrer uniquement les rapports de cet enseignant
    const myReports = (data || []).filter(r => r.enseignant === myTeacherId);

    if (!myReports.length) {
        tbody.innerHTML = `<tr><td colspan="5" class="table__loading">Aucun état disponible pour vous.</td></tr>`;
        return;
    }

    tbody.innerHTML = myReports.map(r => `
    <tr>
      <td>${r.type_label}</td>
      <td>${r.annee_academique}</td>
      <td><strong>${r.total_heures} h</strong></td>
      <td><strong>${formatNumber(Math.round(r.montant_total))} FCFA</strong></td>
      <td>${formatDate(r.date_generation)}</td>
    </tr>
  `).join('');
};