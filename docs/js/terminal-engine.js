/**
 * TERMINAL CLI ENGINE MODULE
 * Provides interactive developer & engineering CLI shell for Houda Tazi's portfolio.
 */

class TerminalEngine {
  constructor(outputElementId = 'terminal-output', inputElementId = 'terminal-input') {
    this.output = document.getElementById(outputElementId);
    this.input = document.getElementById(inputElementId);
    this.container = document.getElementById('terminal-shell') || document.querySelector('.terminal-window');
    this.form = document.getElementById('terminal-form');

    this.history = [];
    this.historyIndex = -1;

    this.commands = {
      help: this.cmdHelp.bind(this),
      bio: this.cmdBio.bind(this),
      skills: this.cmdSkills.bind(this),
      projects: this.cmdProjects.bind(this),
      leoni: this.cmdLeoni.bind(this),
      sews: this.cmdSews.bind(this),
      ocp: this.cmdOcp.bind(this),
      cplex: this.cmdCplex.bind(this),
      status: this.cmdStatus.bind(this),
      offers: this.cmdOffers.bind(this),
      theme: this.cmdTheme.bind(this),
      mode: this.cmdMode.bind(this),
      contact: this.cmdContact.bind(this),
      'download-cv': this.cmdDownloadCv.bind(this),
      cv: this.cmdDownloadCv.bind(this),
      clear: this.cmdClear.bind(this)
    };
  }

  init() {
    if (!this.input || !this.output) return;

    if (this.form) {
      this.form.addEventListener('submit', (e) => {
        e.preventDefault();
        const raw = this.input.value.trim();
        if (!raw) return;

        this.history.push(raw);
        this.historyIndex = this.history.length;
        this.execute(raw);
        this.input.value = '';
      });
    }

    this.input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        const raw = this.input.value.trim();
        if (raw) {
          this.history.push(raw);
          this.historyIndex = this.history.length;
          this.execute(raw);
          this.input.value = '';
        }
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        if (this.historyIndex > 0) {
          this.historyIndex--;
          this.input.value = this.history[this.historyIndex];
        }
      } else if (e.key === 'ArrowDown') {
        e.preventDefault();
        if (this.historyIndex < this.history.length - 1) {
          this.historyIndex++;
          this.input.value = this.history[this.historyIndex];
        } else {
          this.historyIndex = this.history.length;
          this.input.value = '';
        }
      } else if (e.key === 'Tab') {
        e.preventDefault();
        this.handleAutocomplete();
      }
    });

    // Quick action buttons
    const quickBar = document.getElementById('terminal-quick-bar') || document.querySelector('.terminal-quick-bar') || document.querySelector('.terminal-quick-actions');
    if (quickBar) {
      quickBar.addEventListener('click', (e) => {
        const btn = e.target.closest('.terminal-quick-btn');
        if (btn) {
          const cmd = btn.getAttribute('data-cmd');
          if (cmd) this.execute(cmd);
        }
      });
    }

    // Initial greeting
    this.appendRaw(
      '<div class="terminal-line"><span class="term-cyan" style="font-weight: 700;">➜ Houda Tazi IndustrialShell [v3.0.0]</span>' +
      '<span class="term-muted">Tapez <code class="term-success" style="font-weight: 600;">help</code> pour découvrir les commandes ou appuyez sur <code class="term-indigo">Tab</code> pour l\'autocomplétion.</span></div>'
    );
  }

  handleAutocomplete() {
    const val = this.input.value.trim().toLowerCase();
    const commandNames = Object.keys(this.commands);

    if (!val) {
      this.appendRaw(
        `<div class="terminal-line term-muted">Commandes disponibles : ${commandNames.join(', ')}</div>`
      );
      this.output.scrollTop = this.output.scrollHeight;
      return;
    }

    const matches = commandNames.filter(c => c.startsWith(val));
    if (matches.length === 1) {
      this.input.value = matches[0];
    } else if (matches.length > 1) {
      this.appendRaw(
        `<div class="terminal-line term-muted">Suggestions : ${matches.join(', ')}</div>`
      );
      this.output.scrollTop = this.output.scrollHeight;
      let prefix = val;
      for (let i = val.length; ; i++) {
        const char = matches[0][i];
        if (!char || !matches.every(m => m[i] === char)) break;
        prefix += char;
      }
      this.input.value = prefix;
    }
  }

  execute(rawCmd) {
    const parts = rawCmd.trim().split(/\s+/);
    const commandName = parts[0].toLowerCase();

    this.appendRaw(
      `<div class="terminal-line"><div class="terminal-prompt-row">` +
      `<span class="terminal-prompt-user">visitor@houda-tazi</span>:<span class="terminal-prompt-path">~</span>$ ` +
      `<span>${escapeHtml(rawCmd)}</span></div></div>`
    );

    if (this.commands[commandName]) {
      this.commands[commandName](parts.slice(1));
    } else {
      this.appendRaw(
        `<div class="terminal-line term-danger">Commande non reconnue: '${escapeHtml(commandName)}'. Tapez <strong>help</strong> pour l'aide.</div>`
      );
    }

    this.output.scrollTop = this.output.scrollHeight;
  }

  appendRaw(htmlString) {
    const div = document.createElement('div');
    div.innerHTML = htmlString;
    while (div.firstChild) {
      this.output.appendChild(div.firstChild);
    }
  }

  cmdHelp() {
    this.appendRaw(`
      <div class="terminal-line term-muted" style="margin-top: 4px;">
        <span class="term-cyan" style="font-weight: 700;">COMMANDES DISPONIBLES :</span><br>
        • <strong class="term-success">bio</strong>         : Profil académique &amp; diplôme d'ingénieur d'État de Houda Tazi (ENSA)<br>
        • <strong class="term-success">skills</strong>      : Compétences en Production, Lean Manufacturing, Supply Chain et Qualité<br>
        • <strong class="term-success">projects</strong>    : Vue d'ensemble des réalisations industrielles phares<br>
        • <strong class="term-success">leoni</strong>       : Stage PFE : Efficience ligne LAD MERGE P2JO PPL (Lean, chrono-analyse)<br>
        • <strong class="term-success">sews</strong>        : Stage 2A : Productivité chaîne LAD Porta Ducato (VSM, 5S, Muda)<br>
        • <strong class="term-success">ocp</strong>         : Stage 1A : Bilan matière 1800T/j P2O5 et élimination des goulots<br>
        • <strong class="term-success">cplex</strong>       : Recherche Opérationnelle : Problème du Sac à Dos &amp; Simulation Arena<br>
        • <strong class="term-success">status</strong>      : Statut opérationnel de l'agent de veille industrielle<br>
        • <strong class="term-success">offers</strong>      : Top des offres industrielles qualifiées (≥ 80%)<br>
        • <strong class="term-success">contact</strong>     : Coordonnées professionnelles, LinkedIn et Email<br>
        • <strong class="term-success">download-cv</strong> : Télécharger le dossier officiel de candidature PDF<br>
        • <strong class="term-success">clear</strong>       : Nettoyer la console
      </div>
    `);
  }

  cmdBio() {
    this.appendRaw(`
      <div class="terminal-line term-muted">
        <strong class="term-cyan">Houda TAZI</strong> — Ingénieure d'État en Génie Industriel<br>
        École Nationale des Sciences Appliquées (ENSA), El Jadida (Promotion 2026, mention Bien)<br>
        Spécialisation : <span class="term-indigo">Production, Supply Chain, Lean Manufacturing &amp; Amélioration Continue</span><br>
        Disponibilité : CDI, CDD, Emploi Premier Poste / Junior &amp; Stages Pré-embauche (Mobilité Casablanca-Settat, El Jadida, Tanger, Tout le Maroc).
      </div>
    `);
  }

  cmdSkills() {
    this.appendRaw(`
      <div class="terminal-line term-muted">
        <span class="term-cyan" style="font-weight: 700;">COMPÉTENCES TECHNIQUES CŒURS :</span><br>
        • <strong>Lean &amp; Production :</strong> 5S, Kaizen, VSM, DMAIC, SMED, TPM, TRS/OEE, Chrono-analyse, Équilibrage des postes<br>
        • <strong>Supply Chain &amp; Logistique :</strong> Gestion des stocks, Approvisionnements, Ordonnancement, PIC/PDP, Odoo, ERP<br>
        • <strong>Qualité &amp; Méthodes :</strong> MSP (SPC), MiniTab, ISO 9001, IATF 16949, Résolution 8D, Ishikawa, QRQC, AMDEC<br>
        • <strong>Modélisation &amp; Outils :</strong> IBM ILOG CPLEX, Simulation Arena, CATIA, Simulink, TIA Portal, Excel VBA, Python, SQL
      </div>
    `);
  }

  cmdProjects() {
    this.appendRaw(`
      <div class="terminal-line term-muted">
        <span class="term-cyan" style="font-weight: 700;">RÉALISATIONS PHARES :</span><br>
        1. <strong>LEONI Wiring Systems :</strong> Stage PFE — Efficience de la ligne LAD MERGE P2JO PPL (Lean, chrono-analyse).<br>
        2. <strong>SEWS CABIND Maroc :</strong> Stage 2A — Productivité de la chaîne LAD Porta Ducato MY21 (Cartographie VSM, 5S).<br>
        3. <strong>OCP Group / PMP :</strong> Stage 1A — Bilan matière pour 1800T/j de P2O5 et détection des goulots d'étranglement.<br>
        4. <strong>Recherche Opérationnelle :</strong> Optimisation du chargement de conteneurs sous CPLEX et simulation sous Arena.
      </div>
    `);
  }

  cmdLeoni() {
    this.appendRaw(`
      <div class="terminal-line term-muted">
        <strong class="term-cyan">LEONI Wiring Systems (Berrechid)</strong> — Stage de Fin d'Études (2026)<br>
        • Mission : Amélioration continue de l'efficience de la ligne de production LAD MERGE P2JO PPL.<br>
        • Actions : Chrono-analyse des postes, équilibrage dynamique des cadences, réduction des goulots et chantiers Kaizen.<br>
        • Outils : Lean Manufacturing, VSM, TRS/OEE, 5S, Standards de travail.
      </div>
    `);
  }

  cmdSews() {
    this.appendRaw(`
      <div class="terminal-line term-muted">
        <strong class="term-cyan">SEWS CABIND Maroc (Ain Sebaa, Casablanca)</strong> — Stage Ingénieur 2A (2025)<br>
        • Mission : Amélioration de la productivité de la chaîne de production LAD - Projet Porta Ducato MY21.<br>
        • Actions : Analyse des temps opératoires, cartographie VSM et élimination active des gaspillages (Muda).<br>
        • Groupe : Sumitomo Electric Group.
      </div>
    `);
  }

  cmdOcp() {
    this.appendRaw(`
      <div class="terminal-line term-muted">
        <strong class="term-cyan">OCP Group / Pakistan Maroc Phosphore (Jorf Lasfar, El Jadida)</strong> — Stage Ingénieur 1A (2024)<br>
        • Mission : Bilan matière pour la production de 1800T(P2O5)/jour au niveau de l'attaque filtration.<br>
        • Actions : Analyse physico-chimique des flux, identification des pertes de rendement et traitement des goulots.<br>
        • Domaine : Procédés industriels et industrie chimique lourde.
      </div>
    `);
  }

  cmdCplex() {
    this.appendRaw(`
      <div class="terminal-line term-muted">
        <strong class="term-cyan">Recherche Opérationnelle &amp; Simulation Logistique</strong><br>
        • Sujet : Application du problème du Sac à Dos (Knapsack Problem) au chargement optimal des conteneurs maritimes.<br>
        • Outils : IBM ILOG CPLEX (programmation linéaire en nombres entiers), Arena (simulation dynamique des files d'attente).<br>
        • Résultat : Réduction du volume inoccupé et optimisation des cadences de manutention portuaire.
      </div>
    `);
  }

  cmdStatus() {
    const stats = window.dataEngine?.stats || { totalScraped: 370, highMatchCount: 71, remuneratedCount: 69, dispatchedCount: 153 };
    this.appendRaw(`
      <div class="terminal-line term-muted">
        <span class="term-cyan" style="font-weight: 700;">STATUT VEILLE INDUSTRIELLE :</span><br>
        • Portails Surveillés : 6 / 6 (ReKrute, LinkedIn, Emploi.ma, DreamJob, MarocAnnonces, Joblia)<br>
        • Bassins Couverts : Casablanca-Settat, Berrechid, El Jadida (Jorf Lasfar), Tanger, Rabat, Tout le Maroc<br>
        • Filtre Actif : Profil Ingénieur Génie Industriel (Production, Supply Chain, Qualité, Lean)<br>
        • Mode Opérationnel : Sécurisé (Dry-Run actif) avec Digest Anonyme automatique
      </div>
    `);
  }

  cmdOffers() {
    this.appendRaw(`
      <div class="terminal-line term-muted">
        Consultez l'onglet <strong class="term-cyan">Dashboard</strong> pour explorer l'ensemble des offres d'emploi industriel qualifiées avec recherche temps réel et filtres par filière.
      </div>
    `);
  }

  cmdTheme(args) {
    const mode = args[0]?.toLowerCase();
    if (mode === 'light') {
      document.documentElement.setAttribute('data-theme', 'light');
      this.appendRaw(`<div class="terminal-line term-success">Thème <strong>clair</strong> activé.</div>`);
    } else if (mode === 'dark') {
      document.documentElement.setAttribute('data-theme', 'dark');
      this.appendRaw(`<div class="terminal-line term-success">Thème <strong>sombre</strong> activé.</div>`);
    } else {
      this.appendRaw(`<div class="terminal-line term-muted">Usage: <code>theme dark</code> ou <code>theme light</code>.</div>`);
    }
  }

  cmdMode(args) {
    const target = args[0]?.toLowerCase();
    if (target === 'mission' || target === 'dashboard') {
      if (typeof switchMode === 'function') switchMode('mission-control');
      this.appendRaw(`<div class="terminal-line term-success">Navigation vers <strong>Dashboard Opérationnel</strong></div>`);
    } else if (target === 'portfolio') {
      if (typeof switchMode === 'function') switchMode('portfolio');
      this.appendRaw(`<div class="terminal-line term-success">Navigation vers <strong>Portfolio Professionnel</strong></div>`);
    } else {
      this.appendRaw(`<div class="terminal-line term-muted">Usage: <code>mode dashboard</code> ou <code>mode portfolio</code>.</div>`);
    }
  }

  cmdContact() {
    this.appendRaw(`
      <div class="terminal-line term-muted">
        • Email : <a href="mailto:tazihouda1108@gmail.com" target="_blank" class="term-cyan">tazihouda1108@gmail.com</a><br>
        • Téléphone : +212 695-957464<br>
        • Localisation : Hay El Fath, El Gara, Berrechid / Casablanca-Settat<br>
        • LinkedIn : <a href="https://www.linkedin.com/in/houda-tazi-625b11389" target="_blank" class="term-cyan">linkedin.com/in/houda-tazi-625b11389</a>
      </div>
    `);
  }

  cmdDownloadCv() {
    this.appendRaw(`
      <div class="terminal-line term-success">
        ⚡ Téléchargement du dossier de candidature initié...
      </div>
    `);
    const link = document.createElement('a');
    link.href = 'dossier_candidature_houda_tazi.pdf';
    link.download = 'Dossier_Candidature_TAZI_Houda.pdf';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }

  cmdClear() {
    this.output.innerHTML = '';
  }
}

function escapeHtml(str) {
  if (!str) return '';
  return str.toString()
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

window.TerminalEngine = TerminalEngine;
