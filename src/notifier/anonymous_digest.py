"""Anonymous Career Opportunities Digest Notifier for Houda Tazi."""

import html
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import List, Optional

from src.config import config
from src.models.offer import JobOffer
from src.utils.logger import logger


class AnonymousDigestNotifier:
    """
    Formats and dispatches a clean, executive career digest presenting the top qualified
    industrial offers directly to Houda Tazi's personal email (tazihouda1108@gmail.com).
    
    Styled completely neutrally as an automated career intelligence alert service,
    allowing the results to be delivered as an inspiring professional surprise.
    """

    def __init__(self):
        self.recipient = config.digest_recipient
        self.sender_name = config.digest_sender_name

    def build_digest_html(self, offers: List[JobOffer], title: Optional[str] = None) -> str:
        """Builds a high-craft, mobile-responsive HTML newsletter email for job alerts."""
        date_str = datetime.now().strftime("%d/%m/%Y")
        offers_count = len(offers)

        cards_html = ""
        for i, offer in enumerate(offers, 1):
            title = html.escape(offer.title or "Ingénieur(e) Génie Industriel")
            company = html.escape(offer.company or "Entreprise Industrielle")
            location = html.escape(offer.location or "Casablanca-Settat / Maroc")
            url = html.escape(offer.url or "#")
            score = offer.score or 85

            skills_badges = ""
            if offer.matched_skills:
                for skill in offer.matched_skills[:5]:
                    skills_badges += f'<span style="display:inline-block;background:#f1f5f9;color:#334155;font-size:11px;padding:3px 8px;border-radius:12px;margin:2px 4px 2px 0;font-weight:600;">{html.escape(skill)}</span>'

            cards_html += f"""
            <div style="background:#ffffff;border:1px solid #e2e8f0;border-radius:12px;padding:20px;margin-bottom:16px;box-shadow:0 2px 4px rgba(0,0,0,0.03);">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px;">
                <span style="background:#e0f2fe;color:#0284c7;font-size:11px;font-weight:700;padding:3px 10px;border-radius:12px;letter-spacing:0.02em;">OFFRE RECOMMANDÉE · ADÉQUATION {score}%</span>
                <span style="color:#64748b;font-size:12px;">{location}</span>
              </div>
              <h3 style="margin:8px 0 4px 0;font-size:17px;color:#0f172a;line-height:1.3;">{title}</h3>
              <p style="margin:0 0 12px 0;font-size:14px;color:#475569;font-weight:600;">🏢 {company}</p>
              
              <div style="margin-bottom:14px;">
                {skills_badges}
              </div>

              <div style="text-align:right;">
                <a href="{url}" target="_blank" style="display:inline-block;background:#0284c7;color:#ffffff;text-decoration:none;font-size:13px;font-weight:600;padding:8px 18px;border-radius:8px;">Consulter l'offre &amp; Postuler →</a>
              </div>
            </div>
            """

        full_html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <title>Veille Opportunités Industrielles</title>
</head>
<body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;background-color:#f8fafc;color:#1e293b;margin:0;padding:24px 12px;">
  <div style="max-width:640px;margin:0 auto;background:#ffffff;border-radius:16px;overflow:hidden;border:1px solid #e2e8f0;box-shadow:0 4px 12px rgba(0,0,0,0.05);">
    
    <!-- Header Banner -->
    <div style="background:linear-gradient(135deg, #0f172a 0%, #1e293b 100%);padding:32px 24px;text-align:center;color:#ffffff;">
      <span style="display:inline-block;background:rgba(2,132,199,0.25);color:#38bdf8;font-size:12px;font-weight:700;padding:4px 14px;border-radius:20px;margin-bottom:12px;letter-spacing:0.05em;">VEILLE CARRIÈRE &amp; INGÉNIERIE</span>
      <h1 style="margin:0 0 8px 0;font-size:22px;font-weight:800;letter-spacing:-0.02em;">Sélection d'Opportunités · Génie Industriel</h1>
      <p style="margin:0;font-size:14px;color:#94a3b8;">
        {offers_count} opportunité(s) ciblée(s) en Production, Supply Chain, Lean &amp; Qualité sélectionnée(s) pour votre profil au {date_str}.
      </p>
    </div>

    <!-- Content Body -->
    <div style="padding:24px 20px;background:#f8fafc;">
      {cards_html}
    </div>

    <!-- Footer -->
    <div style="padding:20px 24px;text-align:center;background:#ffffff;border-top:1px solid #e2e8f0;font-size:12px;color:#64748b;">
      <p style="margin:0 0 6px 0;">Ce bulletin de veille professionnelle est généré automatiquement pour accompagner les jeunes ingénieurs d'État dans leur insertion industrielle.</p>
      <p style="margin:0;font-weight:600;color:#0f172a;">Excellence opérationnelle &amp; Plein succès dans vos démarches professionnelles !</p>
    </div>

  </div>
</body>
</html>"""
        return full_html

    render_digest_html = build_digest_html

    def send_digest(self, offers: List[JobOffer], force_live: bool = False) -> bool:
        """
        Dispatches the digest email to Houda Tazi.
        Respects Dry-Run mode by default (writing output to letters/digest_preview_houda_tazi.html).
        """
        if not offers:
            logger.info("No qualified offers to dispatch in digest.")
            return False

        html_content = self.build_digest_html(offers)
        date_str = datetime.now().strftime("%d/%m/%Y")
        subject = f"🎯 [Veille Carrière] {len(offers)} Opportunités en Génie Industriel sélectionnées pour vous ({date_str})"

        # Dry-run handling: write preview to disk
        preview_file = config.letters_dir / "digest_preview_houda_tazi.html"
        try:
            config.letters_dir.mkdir(parents=True, exist_ok=True)
            with open(preview_file, "w", encoding="utf-8") as f:
                f.write(html_content)
            logger.info("Digest preview successfully written to %s", preview_file)
        except Exception as e:
            logger.warning("Could not write digest preview: %s", e)

        if config.dry_run and not force_live:
            print("\n" + "=" * 65)
            print("📬 [SIMULATION DRY-RUN] DIGEST ANONYME D'OFFRES")
            print("=" * 65)
            print(f"Destinataire : {self.recipient}")
            print(f"Expéditeur   : {self.sender_name} <{config.gmail_user}>")
            print(f"Objet        : {subject}")
            print(f"Contenu HTML : {len(offers)} offre(s) formatée(s)")
            print(f"Aperçu local : {preview_file}")
            print("=" * 65 + "\n")
            return True

        # Live dispatch via SMTP if credentials available
        if config.gmail_user and config.gmail_app_password:
            try:
                msg = MIMEMultipart("alternative")
                msg["Subject"] = subject
                msg["From"] = f"{self.sender_name} <{config.gmail_user}>"
                msg["To"] = self.recipient

                part = MIMEText(html_content, "html", "utf-8")
                msg.attach(part)

                with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=15) as server:
                    server.login(config.gmail_user, config.gmail_app_password)
                    server.sendmail(config.gmail_user, [self.recipient], msg.as_string())

                logger.info("Live anonymous digest successfully delivered to %s", self.recipient)
                print(f"✅ Digest anonyme envoyé avec succès à {self.recipient} !")
                return True
            except Exception as e:
                logger.error("Failed to send live digest via SMTP: %s", e)
                return False
        else:
            logger.info("SMTP credentials not provided; live dispatch skipped.")
            return False
