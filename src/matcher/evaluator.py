"""Scoring and filtering engine strictly tailored for Houda Tazi's Industrial Engineering profile."""

import re
from typing import List, Optional
from src.config import config
from src.models.offer import JobOffer
from src.utils.logger import logger
from src.utils.date_parser import is_recent_offer, parse_offer_age_days


class OfferEvaluator:
    """Evaluates, filters, and scores scraped job offers strictly for Industrial Engineering."""

    # Target Contract & Career Stage Identifiers (Includes CDI, CDD, Junior & Stages)
    TARGET_CONTRACT_KEYWORDS = [
        r'\bcdi\b',
        r'\bcdd\b',
        r'\bstage\b',
        r'\bpfe\b',
        r'projet de fin d[\'’]études',
        r'projet de fin d[\'’]etudes',
        r'stage pfe',
        r'stage pré-embauche',
        r'stage pre-embauche',
        r'stagiaire',
        r'pré-embauche',
        r'pre-embauche',
        r'jeune diplômé',
        r'jeune diplome',
        r'ingénieur débutant',
        r'ingenieur debutant',
        r'ingénieur junior',
        r'ingenieur junior',
        r'junior',
        r'recrutement',
        r'opportunité',
    ]

    # Industrial Engineering Core Keywords (Case-insensitive)
    INDUSTRIAL_CORE_KEYWORDS = [
        # Domain & Role
        r'génie industriel',
        r'genie industriel',
        r'ingénieur industriel',
        r'ingenieur industriel',
        r'ingénierie industrielle',
        r'ingenierie industrielle',
        r'ingénieur méthodes',
        r'ingenieur methodes',
        r'industrialisation',
        r'ingénieur production',
        r'ingenieur production',
        r'gestion de la production',
        r'ingénieur process',
        r'ingenieur process',
        r'ingénieur exploitation',

        # Lean Manufacturing & Continuous Improvement
        r'amélioration continue',
        r'amelioration continue',
        r'continuous improvement',
        r'lean manufacturing',
        r'lean production',
        r'lean six sigma',
        r'six sigma',
        r'\bkaizen\b',
        r'\b5s\b',
        r'\bvsm\b',
        r'value stream mapping',
        r'dmaic',
        r'\bsmed\b',
        r'\btpm\b',
        r'total productive maintenance',
        r'chrono-analyse',
        r'chrono analyse',
        r'équilibrage de postes',
        r'equilibrage de postes',
        r'ligne de production',
        r'chaîne de production',
        r'chaine de production',
        r'\btrs\b',
        r'\boee\b',
        r'poka[- ]yoke',
        r'\bkanban\b',
        r'juste-à-temps',
        r'just in time',
        r'élimination des gaspillages',

        # Supply Chain & Logistics
        r'supply chain',
        r'logistique',
        r'logistique industrielle',
        r'logistique inverse',
        r'gestion des stocks',
        r'gestion de stock',
        r'approvisionnement',
        r'approvisionnements',
        r'ordonnancement',
        r'planification',
        r'planificateur',
        r'\bpic\b',
        r'\bpdp\b',
        r'plan industriel et commercial',
        r'optimisation des flux',
        r'gestion des flux',
        r'entreposage',
        r'magasin industriel',
        r'gestion des achats',
        r'achats industriels',
        r'\bodoo\b',
        r'\berp\b',

        # Quality Management & Methodologies
        r'qualité',
        r'qualite',
        r'assurance qualité',
        r'assurance qualite',
        r'contrôle qualité',
        r'controle qualite',
        r'management de la qualité',
        r'\bmsp\b',
        r'\bspc\b',
        r'maîtrise statistique',
        r'maitrise statistique',
        r'minitab',
        r'iso 9001',
        r'iatf 16949',
        r'iso 14001',
        r'résolution de problèmes',
        r'resolution de problemes',
        r'\b8d\b',
        r'ishikawa',
        r'5 pourquoi',
        r'\bqrqc\b',
        r'audit qualité',
        r'amdec',
        r'\bfmea\b',

        # Industrial Modeling & Simulation Tools
        r'ibm ilog cplex',
        r'\bcplex\b',
        r'recherche opérationnelle',
        r'recherche operationnelle',
        r'simulation arena',
        r'\barena\b',
        r'\bcatia\b',
        r'simulink',
        r'dessin industriel',
        r'tia portal',
        r'automatisme',
        r'vba',
        r'excel vba',
    ]

    # Industrial Sector Boosters (High relevance in Morocco)
    INDUSTRIAL_SECTOR_BOOSTERS = [
        r'câblage', r'cablage', r'automobile', r'aéronautique', r'aeronautique',
        r'leoni', r'sews', r'yazaki', r'aptiv', r'stellantis', r'renault',
        r'ocp', r'chimie', r'plasturgie', r'métallurgie', r'metallurgie',
        r'agroalimentaire', r'pharma', r'cosumar', r'zone franche',
        r'nouaceur', r'midparc', r'berrechid', r'jorf lasfar', r'tanger automotive',
    ]

    # Non-industrial / Completely Unrelated roles to disqualify
    NON_INDUSTRIAL_DISQUALIFIERS = [
        r'téléconseiller',
        r'teleconseiller',
        r'télévente',
        r'televente',
        r'centre d[\'’]appel',
        r'call center',
        r'helpdesk',
        r'technicien fibre',
        r'câblage réseau',
        r'comptable',
        r'comptabilité',
        r'commercial boutique',
        r'vendeur',
        r'vendeuse',
        r'caissier',
        r'community manager',
        r'graphiste',
        r'secrétariat',
        r'secretariat',
        r'assistant(?:e)? de direction',
        r'réceptionniste',
        r'ressources humaines',
        r'relations humaines',
        r'human resources',
        r'\brh\b',
        r'\bhr\b',
        r'talent acquisition',
        r'recruteur',
        r'chargé(?:e)? de recrutement',
        r'gestionnaire de paie',
        r'\bpaie\b',
        r'juridique',
        r'avocat',
        r'développeur react native',
        r'flutter developer',
    ]

    # Senior Disqualifiers (Positions requiring > 5 years of experience or executive leadership)
    SENIOR_DISQUALIFIERS = [
        r'5 ans d[\'’]expérience',
        r'7 ans d[\'’]expérience',
        r'10 ans d[\'’]expérience',
        r'directeur de site',
        r'plant manager',
        r'directeur usine',
        r'directeur industriel',
        r'directeur des opérations',
    ]

    def is_industrial_offer(self, offer: JobOffer) -> bool:
        """Verifies if the offer is focused on Industrial Engineering, Production, Supply Chain, or Quality."""
        title = (offer.title or "").lower()
        desc = (offer.description or "").lower()
        combined = f"{title} {desc}"

        # 1. Reject if title explicitly states a non-industrial role
        for disq in self.NON_INDUSTRIAL_DISQUALIFIERS:
            if re.search(disq, title, re.IGNORECASE):
                return False

        # 2. Reject senior positions requiring > 5 years
        for sen in self.SENIOR_DISQUALIFIERS:
            if re.search(sen, combined, re.IGNORECASE):
                return False

        # 3. Check for Industrial Core Keywords
        for kw in self.INDUSTRIAL_CORE_KEYWORDS:
            if re.search(kw, combined, re.IGNORECASE):
                return True

        return False

    # Backwards compatibility alias
    is_tech_offer = is_industrial_offer

    def is_contract_match(self, offer: JobOffer) -> bool:
        """Verifies if the offer matches the targeted contracts (CDI, CDD, Junior, Stage Pré-embauche, PFE)."""
        title = (offer.title or "").lower()
        desc = (offer.description or "").lower()
        combined = f"{title} {desc}"

        # Check for senior disqualifiers
        for sen in self.SENIOR_DISQUALIFIERS:
            if re.search(sen, combined, re.IGNORECASE):
                return False

        # If any target contract is matched, or general industrial opening
        for kw in self.TARGET_CONTRACT_KEYWORDS:
            if re.search(kw, combined, re.IGNORECASE):
                return True

        return True

    # Backwards compatibility aliases
    is_tech_offer = is_industrial_offer
    is_ai_offer = is_industrial_offer
    is_pfe_offer = is_contract_match

    def is_recent_enough(self, offer: JobOffer, max_days: Optional[int] = None) -> bool:
        """Verifies offer recency within max_offer_age_days or custom max_days."""
        effective_max = max_days if max_days is not None else config.max_offer_age_days
        if not effective_max:
            return True
        date_str = getattr(offer, 'posted_date', None) or getattr(offer, 'published_date', None)
        if not date_str:
            return True
        age = parse_offer_age_days(date_str)
        return age is None or age <= effective_max

    def score_offer(self, offer: JobOffer) -> int:
        """
        Calculates a score from 0 to 100 representing suitability for Houda Tazi.
        Evaluates matches across Production, Supply Chain, Lean, Quality and Tools.
        """
        if not self.is_industrial_offer(offer):
            return 0

        title = (offer.title or "").lower()
        desc = (offer.description or "").lower()
        combined = f"{title} {desc}"

        score = 50  # Baseline
        matched_skills = []

        # Keyword matching with weight
        for kw in self.INDUSTRIAL_CORE_KEYWORDS:
            clean_kw = kw.replace(r'\b', '').replace(r'\s*', ' ').replace('\\', '')
            if re.search(kw, combined, re.IGNORECASE):
                score += 5
                matched_skills.append(clean_kw.capitalize())

        # Title match bonus
        for kw in [r'industriel', r'méthodes', r'production', r'supply chain', r'logistique', r'qualité', r'lean']:
            if re.search(kw, title, re.IGNORECASE):
                score += 15
                break

        # Industrial sector booster bonus
        for b in self.INDUSTRIAL_SECTOR_BOOSTERS:
            if re.search(b, combined, re.IGNORECASE):
                score += 8
                break

        # Remuneration / salary bonus
        for rk in config.remuneration_keywords:
            if re.search(r'\b' + rk + r'\b', combined, re.IGNORECASE):
                score += 5
                offer.is_remunerated = True
                break

        # Geographic bonus
        for city in config.target_cities:
            if city.lower() in combined:
                score += 5
                break

        # Deduplicate and cap matched skills
        seen = set()
        unique_skills = []
        for s in matched_skills:
            normalized = s.lower()
            if normalized not in seen:
                seen.add(normalized)
                unique_skills.append(s)

        offer.matched_skills = unique_skills[:8]
        return min(max(score, 0), 100)

    def evaluate(self, offer: JobOffer) -> JobOffer:
        """Evaluates a single offer, attaching score and matched skills."""
        offer.score = self.score_offer(offer)
        return offer

    def evaluate_all(self, offers: List[JobOffer]) -> List[JobOffer]:
        """Filters and scores a collection of job offers, returning qualified ones sorted by score."""
        evaluated = []
        for offer in offers:
            evaluated_offer = self.evaluate(offer)
            if (evaluated_offer.score or 0) >= 50:
                evaluated.append(evaluated_offer)

        evaluated.sort(key=lambda o: (o.score or 0), reverse=True)
        logger.info("OfferEvaluator qualified %d / %d offers for Houda Tazi", len(evaluated), len(offers))
        return evaluated
