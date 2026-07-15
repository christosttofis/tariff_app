"""
Email notifications via Microsoft Graph API (OAuth2 client credentials).

The app sends mail on behalf of TARIFF_EMAIL_FROM using an Azure AD app
registration with Mail.Send application permission granted by an admin.

No passwords — only the client secret from the Azure app registration.
"""

import html
import logging
import os
import threading

import msal
import requests

logger = logging.getLogger(__name__)


def _esc(v) -> str:
    """HTML-escape a value before interpolating it into an email body — tariff
    names, supplier names, and rejection reasons are all user-controlled and
    would otherwise let a supplier inject markup/links into an HTML email
    rendered in someone else's mail client (admin or supplier)."""
    return html.escape(str(v), quote=True)

TENANT_ID     = os.getenv("AZURE_TENANT_ID", "")
CLIENT_ID     = os.getenv("AZURE_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET", "")
FROM_EMAIL    = os.getenv("TARIFF_EMAIL_FROM", "")
ADMIN_TO      = os.getenv("TARIFF_ADMIN_EMAIL", "")
BASE_URL      = os.getenv("TARIFF_BASE_URL", "http://localhost:8000").rstrip("/")

_GRAPH_SCOPE  = ["https://graph.microsoft.com/.default"]
_msal_app: msal.ConfidentialClientApplication | None = None


def _get_msal_app() -> msal.ConfidentialClientApplication:
    global _msal_app
    if _msal_app is None:
        _msal_app = msal.ConfidentialClientApplication(
            CLIENT_ID,
            client_credential=CLIENT_SECRET,
            authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        )
    return _msal_app


def _get_token() -> str:
    app = _get_msal_app()
    result = app.acquire_token_for_client(scopes=_GRAPH_SCOPE)
    if "access_token" not in result:
        raise RuntimeError(result.get("error_description") or result.get("error") or "Unknown MSAL error")
    return result["access_token"]


# ── Template helpers (table-based, inline styles — Outlook compatible) ────────

_FONT = "font-family:'Segoe UI',Arial,sans-serif"
_BLUE = "#1e3a5f"


def _btn(url: str, label: str) -> str:
    """CTA button that renders correctly in both Outlook and Gmail."""
    return (
        f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin-top:16px">'
        f'<tr><td style="background:{_BLUE};padding:9px 20px">'
        f'<a href="{url}" style="color:#ffffff;text-decoration:none;font-size:13px;font-weight:600;{_FONT};display:inline-block">'
        f'{label}</a></td></tr></table>'
    )


def _row(label: str, value: str) -> str:
    """A label/value row inside a detail table."""
    return (
        f'<tr>'
        f'<td style="padding:6px 0;font-size:13px;color:#8b93a1;width:130px;padding-right:12px;vertical-align:top;{_FONT}">{label}</td>'
        f'<td style="padding:6px 0;font-size:13px;color:#1c2530;vertical-align:top;{_FONT}">{value}</td>'
        f'</tr>'
    )


def _detail_table(rows_html: str) -> str:
    return (
        f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:12px 0">'
        f'{rows_html}'
        f'</table>'
    )


def _html(head_title: str, body_html: str) -> str:
    return f"""<!DOCTYPE html>
<html xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<!--[if mso]>
<noscript><xml><o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch></o:OfficeDocumentSettings></xml></noscript>
<![endif]-->
</head>
<body style="margin:0;padding:0;background:#f3f4f6;{_FONT};font-size:14px;color:#1c2530">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#f3f4f6">
  <tr>
    <td align="center" style="padding:32px 16px">
      <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="520"
             style="width:520px;max-width:520px;background:#ffffff;border:1px solid #d7dae0">
        <tr>
          <td style="background:#ffffff;padding:16px 24px;border-bottom:1px solid #eceef1">
            <table role="presentation" cellpadding="0" cellspacing="0" border="0">
              <tr>
                <td style="vertical-align:middle;padding-right:14px">
                  <img src="{BASE_URL}/Logo_Transparent.png" alt="CERA" width="57" height="44" style="display:block;height:44px;width:57px;border:0">
                </td>
                <td style="vertical-align:middle">
                  <p style="color:{_BLUE};font-size:16px;font-weight:600;margin:0;{_FONT}">{head_title}</p>
                  <p style="color:#8b93a1;font-size:11px;margin:4px 0 0;{_FONT}">CERA Tariff Comparison Tool</p>
                </td>
              </tr>
            </table>
          </td>
        </tr>
        <tr>
          <td style="padding:24px;{_FONT};font-size:14px;color:#1c2530">
            {body_html}
          </td>
        </tr>
        <tr>
          <td style="padding:14px 24px;border-top:1px solid #eceef1;font-size:11px;color:#8b93a1;{_FONT}">
            Cyprus Energy Regulatory Authority &middot; Automated message &mdash; do not reply.
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>
</body>
</html>"""


# ── Core send ─────────────────────────────────────────────────────────────────

def _send_bg(to: list[str], subject: str, html: str) -> None:
    """Fire-and-forget via Graph API — never raises, errors are logged."""
    if not all([TENANT_ID, CLIENT_ID, CLIENT_SECRET, FROM_EMAIL]):
        logger.warning("Email skipped — Azure credentials not configured: %s", subject)
        return
    recipients = [r for r in to if r]
    if not recipients:
        logger.warning("Email skipped — no recipients: %s", subject)
        return

    def _send():
        try:
            token = _get_token()
            payload = {
                "message": {
                    "subject": subject,
                    "body": {"contentType": "HTML", "content": html},
                    "toRecipients": [
                        {"emailAddress": {"address": r}} for r in recipients
                    ],
                }
            }
            resp = requests.post(
                f"https://graph.microsoft.com/v1.0/users/{FROM_EMAIL}/sendMail",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                },
                json=payload,
                timeout=15,
            )
            if resp.status_code == 202:
                logger.info("Email sent → %s | %s", recipients, subject)
            else:
                logger.error("Graph API error %s → %s | %s", resp.status_code, resp.text, subject)
        except Exception as exc:
            logger.error("Email failed → %s | %s | %s", recipients, subject, exc)

    threading.Thread(target=_send, daemon=True).start()


# ── Notification helpers ──────────────────────────────────────────────────────

def notify_admin_new_tariff(tariff_name: str, supplier: str) -> None:
    if not ADMIN_TO:
        return
    body = (
        f'<p style="margin:0 0 12px;{_FONT}">A new tariff has been submitted and is awaiting your review.</p>'
        + _detail_table(_row("Tariff", f"<strong>{_esc(tariff_name)}</strong>") + _row("Supplier", _esc(supplier)))
        + _btn(f"{BASE_URL}/admin.html", "Open Admin Panel")
    )
    _send_bg([ADMIN_TO],
        f"[CERA Tariff] New submission pending review — {tariff_name}",
        _html("New tariff submission", body))


def notify_admin_resubmit(tariff_name: str, supplier: str) -> None:
    if not ADMIN_TO:
        return
    body = (
        f'<p style="margin:0 0 12px;{_FONT}">A tariff has been edited and resubmitted. It requires re-approval before going live.</p>'
        + _detail_table(_row("Tariff", f"<strong>{_esc(tariff_name)}</strong>") + _row("Supplier", _esc(supplier)))
        + _btn(f"{BASE_URL}/admin.html", "Review in Admin Panel")
    )
    _send_bg([ADMIN_TO],
        f"[CERA Tariff] Tariff resubmitted — {tariff_name}",
        _html("Tariff resubmitted for review", body))


def notify_supplier_approved(to_emails: list[str], tariff_name: str, supplier: str) -> None:
    if not to_emails:
        return
    body = (
        f'<p style="margin:0 0 12px;{_FONT}">Your tariff has been reviewed and '
        f'<strong style="color:#2f6f4e">approved</strong>. '
        f'It is now live on the CERA electricity tariff comparison tool.</p>'
        + _detail_table(_row("Tariff", f"<strong>{_esc(tariff_name)}</strong>") + _row("Supplier", _esc(supplier)))
        + _btn(f"{BASE_URL}/supplier.html", "View in Supplier Portal")
    )
    _send_bg(to_emails,
        f"[CERA Tariff] Your tariff has been approved — {tariff_name}",
        _html("Tariff approved", body))


def notify_supplier_rejected(to_emails: list[str], tariff_name: str, supplier: str, reason: str = "") -> None:
    if not to_emails:
        return
    rows = _row("Tariff", f"<strong>{_esc(tariff_name)}</strong>") + _row("Supplier", _esc(supplier))
    if reason:
        rows += _row("Reason", _esc(reason))
    body = (
        f'<p style="margin:0 0 12px;{_FONT}">Your tariff has been reviewed and was '
        f'<strong style="color:#a6403a">not approved</strong> at this time.</p>'
        + _detail_table(rows)
        + f'<p style="margin:12px 0;{_FONT}">Please log in to the supplier portal to review your tariff '
        f'and resubmit after making any necessary changes.</p>'
        + _btn(f"{BASE_URL}/supplier.html", "Open Supplier Portal")
    )
    _send_bg(to_emails,
        f"[CERA Tariff] Your tariff was not approved — {tariff_name}",
        _html("Tariff not approved", body))


def notify_password_reset(to_email: str, reset_url: str) -> None:
    body = (
        f'<p style="margin:0 0 12px;{_FONT}">A password reset was requested for this account.</p>'
        f'<p style="margin:0 0 12px;{_FONT}">Click the button below to set a new password. '
        f'This link is valid for <strong>1 hour</strong> and can only be used once.</p>'
        + _btn(reset_url, "Reset my password")
        + f'<p style="margin:20px 0 0;font-size:11px;color:#8b93a1;{_FONT}">'
        f'If you did not request a password reset, you can safely ignore this email.</p>'
    )
    _send_bg([to_email],
        "[CERA Tariff] Password reset request",
        _html("Password reset", body))


def notify_account_locked(to_email: str, lockout_minutes: int, role: str) -> None:
    portal_url = f"{BASE_URL}/{'admin' if role == 'admin' else 'supplier'}.html"
    body = (
        f'<p style="margin:0 0 12px;{_FONT}">We detected multiple failed login attempts on your account '
        f'and have temporarily locked it for <strong>{lockout_minutes} minutes</strong> as a security measure.</p>'
        f'<p style="margin:0 0 12px;{_FONT}">You can try again after {lockout_minutes} minutes. '
        f'If you have forgotten your password, use the <em>Forgot password</em> link on the login page to reset it.</p>'
        + _btn(portal_url, "Go to login page")
        + f'<p style="margin:20px 0 0;font-size:12px;color:#a6403a;{_FONT}">'
        f'<strong>If this was not you</strong>, your account may be under a brute-force attack. '
        f'Please contact your CERA administrator immediately.</p>'
    )
    _send_bg([to_email],
        "[CERA Tariff] Your account has been temporarily locked",
        _html("Account temporarily locked", body))


def send_otp_code(to_email: str, code: str) -> None:
    body = (
        f'<p style="margin:0 0 12px;{_FONT}">A sign-in attempt was made for your account. '
        f'Enter the code below to complete login.</p>'
        f'<div style="margin:20px 0;text-align:center">'
        f'<span style="font-size:32px;font-weight:700;letter-spacing:10px;font-family:monospace;color:{_BLUE}">{code}</span>'
        f'</div>'
        f'<p style="margin:0 0 12px;font-size:13px;color:#8b93a1;{_FONT}">This code is valid for <strong>10 minutes</strong> and can only be used once.</p>'
        f'<p style="margin:20px 0 0;font-size:11px;color:#a6403a;{_FONT}">'
        f'<strong>If you did not attempt to log in</strong>, someone may have your password. '
        f'Contact your CERA administrator immediately and change your password.</p>'
    )
    _send_bg([to_email],
        "[CERA Tariff] Your login verification code",
        _html("Verification code", body))


def notify_new_message(to_emails: list[str], subject: str) -> None:
    if not to_emails:
        return
    body = (
        f'<p style="margin:0 0 8px;{_FONT}">Έχετε μια νέα ειδοποίηση στην Πύλη Προμηθευτών σας. '
        f'Συνδεθείτε στον λογαριασμό σας για να τη δείτε.</p>'
        f'<p style="margin:0 0 16px;{_FONT}">You have a new notification in your Supplier Portal. '
        f'Log in to your account to view it.</p>'
        + _btn(f"{BASE_URL}/supplier.html", "Είσοδος στην Πύλη Προμηθευτών / Login to Supplier Portal")
    )
    _send_bg(to_emails,
        f"[CERA Tariff] {subject}",
        _html("Ειδοποίηση από τη ΡΑΕΚ / Notification from CERA", body))


def notify_password_expiring(to_email: str, days_left: int, role: str = "supplier") -> None:
    portal_url = f"{BASE_URL}/{'admin' if role == 'admin' else 'supplier'}.html"
    body = (
        f'<p style="margin:0 0 8px;{_FONT}">Ο κωδικός πρόσβασής σας λήγει σε <strong>{days_left} ημέρες</strong>. '
        f'Συνδεθείτε και αλλάξτε τον κωδικό σας για να αποφύγετε τον αποκλεισμό της πρόσβασής σας.</p>'
        f'<p style="margin:0 0 16px;{_FONT}">Your password expires in <strong>{days_left} day(s)</strong>. '
        f'Log in and change it to avoid losing access to your account.</p>'
        + _btn(portal_url, "Login / Σύνδεση")
    )
    _send_bg([to_email],
        "[CERA Tariff] Ο κωδικός σας λήγει σύντομα / Your password is expiring soon",
        _html("Λήξη κωδικού πρόσβασης / Password expiring", body))


def notify_supplier_invite(to_email: str, supplier_name: str, invite_url: str) -> None:
    body = (
        f'<p style="margin:0 0 12px;{_FONT}">You have been invited to manage tariffs for '
        f'<strong>{_esc(supplier_name)}</strong> on the Cyprus Energy Regulatory Authority '
        f'Tariff Comparison Tool.</p>'
        f'<p style="margin:0 0 12px;{_FONT}">Click the button below to set up your password '
        f'and activate your account. This link is valid for <strong>7 days</strong>.</p>'
        + _btn(invite_url, "Set up my account")
        + f'<p style="margin:20px 0 0;font-size:11px;color:#8b93a1;{_FONT}">'
        f'If you were not expecting this invitation, you can safely ignore this email.</p>'
    )
    _send_bg([to_email],
        "[CERA Tariff] You have been invited to the Supplier Portal",
        _html("Welcome to CERA Tariff Tool", body))
