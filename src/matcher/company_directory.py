"""Directory of verified recruitment contacts for Moroccan tech and multinational employers."""

import re
from typing import Optional, Tuple
from src.utils.logger import logger

# Moroccan Industrial, Automotive, Aerospace, Logistics, Pharma & Engineering Corporate Inboxes
MOROCCO_TECH_DIRECTORY = [
    # Automotive, Cabling & Industrial Manufacturing (High Priority for Houda Tazi)
    (r'\bleoni\b', "recrutement.maroc@leoni.com", "LEONI Wiring Systems"),
    (r'\bsews\b|\bsumitomo\b', "recrutement.sews@sews-eeb.com", "SEWS CABIND Maroc"),
    (r'\byazaki\b', "recrutement.maroc@yazaki-europe.com", "Yazaki Morocco"),
    (r'\baptiv\b', "recrutement.maroc@aptiv.com", "Aptiv Services Maroc"),
    (r'\brenault\b', "recrutement.maroc@renault.com", "Renault Group Maroc"),
    (r'\bstellantis\b|\bpsa\b', "recrutement.kenitra@stellantis.com", "Stellantis"),
    (r'\blear\b', "recrutement.maroc@lear.com", "Lear Corporation"),
    (r'\bsnop\b', "recrutement.tanger@snop.eu", "SNOP Automotive Maroc"),
    (r'\bhirschmann\b', "recrutement.maroc@hirschmann-automotive.com", "Hirschmann Automotive"),
    (r'\bvaleo\b', "recrutement.maroc@valeo.com", "Valeo Maroc"),
    (r'\bfaurecia\b|\bforvia\b', "recrutement.maroc@forvia.com", "FORVIA (Faurecia) Maroc"),
    (r'\bproma\b', "recrutement@promagroup.com", "Proma Industries"),
    (r'\bdenso\b', "recrutement.maroc@denso.com", "Denso Thermal Systems Maroc"),
    (r'\bpolydesign\b', "recrutement@polydesignsystems.com", "Polydesign Systems"),
    (r'\bvarroc\b', "recrutement.maroc@varroc.com", "Varroc Lighting Systems"),
    (r'\bnexans\b', "recrutement.maroc@nexans.com", "Nexans Maroc"),
    (r'\balstom\b', "recrutement.maroc@alstomgroup.com", "Alstom Maroc"),

    # Aerospace & High-Tech Industry
    (r'\bsafran\b', "recrutement.maroc@safrangroup.com", "Safran Maroc"),
    (r'\bspirit\s*aerosystems\b', "recrutement.maroc@spiritaero.com", "Spirit AeroSystems Maroc"),
    (r'\bstelia\b|\bairbus\b', "recrutement.maroc@stelia-aerospace.com", "Stelia Aerospace Maroc"),
    (r'\bratier[\s-]*figeac\b|\bcollins\b', "recrutement.maroc@collins.com", "Ratier-Figeac / Collins Aerospace Maroc"),

    # Heavy Industry, Chemicals, Steel, Construction & Energy
    (r'\bocp\b', "recrutement@ocpgroup.ma", "OCP Group"),
    (r'\bmaghreb\s*steel\b', "recrutement@maghrebsteel.ma", "Maghreb Steel"),
    (r'\bsonasid\b', "recrutement@sonasid.ma", "Sonasid"),
    (r'\blafarge\b|\bholcim\b', "recrutement.maroc@lafargeholcim.com", "LafargeHolcim Maroc"),
    (r'\bciments\s*du\s*maroc\b', "recrutement@cimentsdumaroc.com", "Ciments du Maroc"),
    (r'\bmanagem\b', "recrutement@managemgroup.com", "Managem Group"),
    (r'\bcosumar\b', "recrutement@cosumar.co.ma", "Cosumar"),
    (r'\bmasen\b', "recrutement@masen.ma", "MASEN"),
    (r'\boncf\b', "recrutement@oncf.ma", "ONCF"),

    # Supply Chain, Logistics, Pharma & FMCG
    (r'\bdachser\b', "recrutement.maroc@dachser.com", "DACHSER Maroc"),
    (r'\bdislog\b', "recrutement@disloggroup.com", "Dislog Group"),
    (r'\bmarsa\s*maroc\b', "recrutement@marsamaroc.co.ma", "Marsa Maroc"),
    (r'\btanger\s*med\b', "recrutement@tangermed.ma", "Tanger Med"),
    (r'\bsothema\b', "recrutement@sothema.com", "Sothema"),
    (r'\bcooper\s*pharma\b', "recrutement@cooperpharma.ma", "Cooper Pharma"),
    (r'\bcentrale\s*danone\b|\bdanone\b', "recrutement.maroc@danone.com", "Centrale Danone"),
    (r'\blesieur\b', "recrutement@lesieur-cristal.co.ma", "Lesieur Cristal"),
    (r'\blabel\s*[\'’]?vie\b|\bcarrefour\b', "recrutement@labelvie.ma", "Label'Vie Carrefour"),

    # Engineering Consulting, Recruitment & Multinationals
    (r'\bcapgemini\b', "recrutementmaroc.ceg@capgemini.com", "Capgemini Morocco"),
    (r'\bsofrecom\b|\borange\b', "recrutement.maroc@sofrecom.com", "Sofrecom / Orange Maroc"),
    (r'\balten\b', "recrutement.maroc@alten.com", "Alten Maroc"),
    (r'\bsqli\b', "recrutement-maroc@sqli.com", "SQLI Maroc"),
    (r'\bcgi\b', "carrieres.maroc@cgi.com", "CGI Maroc"),
    (r'\batos\b|\beviden\b', "maroc.recrutement@atos.net", "Atos / Eviden"),
    (r'\bdxc\b', "dxc-recrutement-maroc@dxc.com", "DXC Technology Maroc"),
    (r'\bleyton\b', "recrutement-maroc@leyton.com", "Leyton Maroc"),
    (r'\bsopra\s*steria\b', "recrutement.maroc@soprasteria.com", "Sopra Steria Maroc"),
    (r'\bdell\b', "morocco.careers@dell.com", "Dell Technologies Casablanca"),
    (r'\bintelcia\b', "recrutement.it@intelcia.com", "Intelcia IT Solutions"),
    (r'\binwi\b|\bwana\b', "recrutement@inwi.ma", "inwi"),
    (r'\bmaroc\s*telecom\b|\biam\b', "recrutement@iam.ma", "Maroc Telecom"),
    (r'\bthales\b', "recrutement.maroc@thalesgroup.com", "Thales Maroc"),
    (r'\bcoface\b', "recrutement-maroc@coface.com", "Coface"),
    (r'\battijari\b|\battijariwafa\b', "recrutement@attijariwafa.com", "Attijariwafa bank"),
    (r'\bbank\s*of\s*africa\b|\bbmce\b', "recrutement@bankofafrica.ma", "Bank of Africa"),
    (r'\bbanque\s*populaire\b|\bbcp\b', "recrutement@cpm.ma", "Banque Populaire"),
    (r'\bcih\b', "recrutement@cihbank.ma", "CIH Bank"),
    (r'\bcr[ée]dit\s*du\s*maroc\b|\bcdm\b', "recrutement@cdm.ma", "Crédit du Maroc"),
    (r'\bsoci[ée]t[ée]\s*g[ée]n[ée]rale\b|\bsgabs\b', "recrutement@socgen.com", "Société Générale Maroc"),
    (r'\bmanpower\b', "recrutement@manpower-maroc.com", "Manpower Maroc"),
    (r'\bakkodis\b|\bakka\b', "recrutement.maroc@akkodis.com", "Akkodis Maroc"),
    (r'\badecco\b', "recrutement@adecco.ma", "Adecco Maroc"),
    (r'\bmichael\s*page\b', "contact.maroc@michaelpage.com", "Michael Page Maroc"),
    (r'\bum6p\b', "recrutement@um6p.ma", "UM6P"),
    (r'\bmascir\b', "recrutement@mascir.com", "MAScIR"),
    (r'\bcnss\b', "recrutement@cnss.ma", "CNSS"),
]


def resolve_company_email(company_name: str, description: str = "") -> Tuple[Optional[str], Optional[str]]:
    """
    Attempts to match a company name or description against verified recruitment inboxes.
    Returns (verified_email, standardized_company_name) or (None, None).
    """
    if not company_name:
        return None, None

    search_target = f"{company_name} {description}".lower()

    for pattern, email, standard_name in MOROCCO_TECH_DIRECTORY:
        if re.search(pattern, search_target, re.IGNORECASE):
            logger.info("Resolved recruitment contact for '%s' -> %s (%s)", company_name, email, standard_name)
            return email, standard_name

    return None, None
