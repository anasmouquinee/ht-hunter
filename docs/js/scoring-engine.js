/**
 * SCORING ENGINE MODULE
 * Provides client-side matching simulation tailored for Houda Tazi's Industrial Engineering profile.
 * Supports configurable category weights and missing skills detection.
 */

class ScoringEngine {
  constructor() {
    // Core profile target keywords for Houda Tazi (ENSA El Jadida - Génie Industriel)
    this.targetSkills = [
      { name: 'Lean Manufacturing & Kaizen', aliases: ['lean', 'kaizen', '5s', 'vsm', 'dmaic', 'smed', 'tpm', 'amelioration continue', 'amélioration continue'], category: 'lean', weight: 18 },
      { name: 'Gestion de Production & Méthodes', aliases: ['production', 'méthodes', 'methodes', 'industrialisation', 'chrono-analyse', 'équilibrage', 'trs', 'oee', 'ligne de production'], category: 'production', weight: 18 },
      { name: 'Supply Chain & Logistique', aliases: ['supply chain', 'logistique', 'gestion des stocks', 'approvisionnement', 'ordonnancement', 'planification', 'pic', 'pdp', 'flux'], category: 'supply', weight: 16 },
      { name: 'Management de la Qualité & MSP', aliases: ['qualité', 'qualite', 'assurance qualité', 'contrôle qualité', 'msp', 'spc', 'iso 9001', 'iatf 16949', '8d', 'ishikawa', 'qrqc'], category: 'quality', weight: 15 },
      { name: 'Optimisation & Simulation (CPLEX / Arena)', aliases: ['cplex', 'ibm ilog cplex', 'arena', 'simulation arena', 'recherche opérationnelle', 'recherche operationnelle'], category: 'tools', weight: 12 },
      { name: 'ERP, Odoo & Excel VBA', aliases: ['erp', 'odoo', 'vba', 'excel vba', 'gestion des achats', 'base de données', 'sql'], category: 'tools', weight: 11 },
      { name: 'CAO & Automatismes (CATIA / Simulink / TIA Portal)', aliases: ['catia', 'simulink', 'tia portal', 'automatisme', 'dessin industriel'], category: 'engineering', weight: 10 }
    ];

    // Seniority & Incompatibility exclusion terms
    this.exclusionPatterns = [
      { pattern: /\b([5-9]|\d{2})\+?\s*(ans?|ann[eé]es?)\s+(d['\u2019]exp[eé]rience|d['\u2019]anciennet[eé])\b/i, reason: 'Expérience professionnelle minimale requise supérieure à 5 ans' },
      { pattern: /\b(directeur usine|plant manager|directeur industriel|head of manufacturing)\b/i, reason: 'Intitulé de poste de direction d\'usine ou direction générale' },
      { pattern: /\b(téléconseiller|televente|call center|centre d['\u2019]appels?)\b/i, reason: 'Activité de centre d\'appels / télévente (hors périmètre ingénierie)' },
      { pattern: /\b(comptable|caissier|vendeur boutique)\b/i, reason: 'Poste tertiaire ou commercial en boutique' }
    ];

    // Remuneration indicators
    this.remunerationPatterns = [
      /\b(r[eé]mun[eé]r[eé]|gratifi[eé]|indemnit[eé]|prime\s+de\s+stage|salaire)\b/i
    ];
  }

  evaluateOfferText(text, weights = null) {
    if (!text || text.trim().length < 15) {
      return {
        score: 0,
        isEligible: false,
        detectedSkills: [],
        missingSkills: [],
        exclusions: ['Description de poste trop succincte pour une évaluation IA fiable'],
        isRemunerated: false,
        verdict: 'DONNÉES INSUFFISANTES',
        badgeClass: 'badge-danger',
        reasoning: 'Veuillez saisir un texte d\'offre ou coller une description complète pour déclencher l\'analyse.'
      };
    }

    const cleanText = text.toLowerCase();
    const exclusions = [];

    // 1. Verify Exclusion Rules
    for (const rule of this.exclusionPatterns) {
      if (rule.pattern.test(cleanText)) {
        exclusions.push(rule.reason);
      }
    }

    // 2. Check False-Positive Homonym: French "j'ai" vs "IA"
    const hasFalsePositiveIA = /\bj['\u2019]ai\b/i.test(cleanText) &&
      !/\bintelligence\s+artificielle\b/i.test(cleanText) &&
      !/\b(machine\s+learning|python|llm|deep\s+learning)\b/i.test(cleanText);

    if (hasFalsePositiveIA) {
      exclusions.push('Détection de faux-positif linguistique : présence de la forme verbale "j\'ai" confondue avec le sigle IA');
    }

    // 3. Detect Skills & Calculate Match Score with Configurable Weights
    const detectedSkills = [];
    const missingSkills = [];
    let earnedWeight = 0;
    let maxWeight = 0;

    for (const skill of this.targetSkills) {
      // Determine multiplier based on passed custom weights
      let multiplier = 1.0;
      if (weights) {
        if (typeof weights[skill.category] === 'number') {
          multiplier = weights[skill.category];
        } else if (typeof weights[skill.name] === 'number') {
          multiplier = weights[skill.name];
        }
      }

      const activeWeight = skill.weight * multiplier;
      maxWeight += activeWeight;
      let matched = false;

      // Check primary name
      if (cleanText.includes(skill.name.toLowerCase())) {
        matched = true;
      } else if (skill.aliases) {
        // Check aliases with regex word boundary
        for (const alias of skill.aliases) {
          const regex = new RegExp(`\\b${alias}\\b`, 'i');
          if (regex.test(cleanText)) {
            matched = true;
            break;
          }
        }
      }

      if (matched) {
        detectedSkills.push(skill.name);
        earnedWeight += activeWeight;
      } else {
        missingSkills.push(skill.name);
      }
    }

    // Baseline stage bonus if explicitly mentions PFE or stage fin d'études
    const isPfeMentioned = /\b(pfe|stage\s+de\s+fin\s+d['\u2019][eé]tudes?|stagiaire\s+pfe)\b/i.test(cleanText);
    let rawScore = maxWeight > 0 ? Math.round((earnedWeight / maxWeight) * 100) : 0;

    if (isPfeMentioned) rawScore = Math.min(100, rawScore + 10);
    const isRemunerated = this.remunerationPatterns.some(p => p.test(cleanText));
    if (isRemunerated) rawScore = Math.min(100, rawScore + 5);

    // If exclusions triggered, clamp score
    let finalScore = rawScore;
    let isEligible = true;
    let verdict = 'QUALIFIÉ POUR CANDIDATURE PFE';
    let badgeClass = 'badge-success';

    if (exclusions.length > 0) {
      finalScore = Math.min(35, rawScore);
      isEligible = false;
      verdict = 'REJET AUTOMATIQUE - CRITÈRES NON RESPECTÉS';
      badgeClass = 'badge-danger';
    } else if (finalScore < 50) {
      isEligible = false;
      verdict = 'FAIBLE CORRESPONDANCE TECHNIQUE';
      badgeClass = 'badge-warning';
    } else if (finalScore >= 80) {
      verdict = 'CANDIDATURE PRIORITAIRE - MATCH ÉLEVÉ';
      badgeClass = 'badge-cyan';
    }

    // Generate Explanatory Reasoning
    let reasoning = '';
    if (!isEligible) {
      reasoning = `L'offre a été écartée car elle présente ${exclusions.length} motif(s) d'exclusion : ${exclusions.join(' ; ')}. L'agent évite ainsi de postuler à des offres inadaptées.`;
    } else {
      reasoning = `L'offre correspond à ${finalScore}% aux compétences cibles de Houda Tazi. Les domaines identifiés (${detectedSkills.slice(0, 4).join(', ')}) s'alignent avec sa formation en Génie Industriel (ENSA El Jadida) et ses réalisations en production/Lean (Leoni, Sews Cabind, OCP). Recommandation : candidature qualifiée avec dossier_candidature_houda_tazi.pdf.`;
    }

    return {
      score: finalScore,
      isEligible: isEligible,
      detectedSkills: detectedSkills,
      missingSkills: missingSkills,
      exclusions: exclusions,
      isRemunerated: isRemunerated,
      isPfe: isPfeMentioned,
      verdict: verdict,
      badgeClass: badgeClass,
      reasoning: reasoning
    };
  }
}

// Global singleton instance
window.scoringEngine = new ScoringEngine();
