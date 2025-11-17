import smtplib
from datetime import datetime, timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from bson import ObjectId
from loguru import logger

from src.tasks.celery_app import celery_app
from src.db.mongo import get_client, get_sync_client
from src.config import settings
from src.common.constants import EMAILS_LOG_COL, STATS_LOG_COL, ARTICLES_COL


@celery_app.task(name="src.tasks.worker.send_welcome_email")
def send_welcome_email(user_id: str, email: str, name: str):
    """Sending real email via SMTP + log to MongoDB."""
    client = get_client()
    db = client[settings.MONGO_DB]

    subject = "Welcome to ArticleHub"
    body = f"Hello {name}, welcome to ArticleHub! 🎉"

    msg = MIMEMultipart()
    msg["From"] = settings.SMTP_USER
    msg["To"] = email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)

        logger.info(f"[EMAIL SENT] to={email} user_id={user_id}")

        entry = {
            "user_id": ObjectId(user_id),
            "email": email,
            "name": name,
            "subject": subject,
            "body": body,
            "created_at": datetime.now(timezone.utc),
            "status": "sent",
        }
        db[EMAILS_LOG_COL].insert_one(entry)

    except Exception as e:
        logger.error(f"Error sending email to {email}: {e}")
        entry = {
            "user_id": ObjectId(user_id),
            "email": email,
            "name": name,
            "subject": subject,
            "body": body,
            "created_at": datetime.now(timezone.utc),
            "status": "failed",
            "error": str(e),
        }
        db[EMAILS_LOG_COL].insert_one(entry)


@celery_app.task(name="src.tasks.worker.daily_articles_stats")
def daily_articles_stats():
    client = get_client()
    db = client[settings.MONGO_DB]
    count = db[ARTICLES_COL].count_documents({})

    rec = {
        "ts": datetime.now(timezone.utc),
        "articles_total": count,
    }
    db[STATS_LOG_COL].insert_one(rec)
    logger.info(f"[STATS] total_articles={count}")


@celery_app.task(name="src.tasks.worker.analyze_article")
def analyze_article(article_id: str) -> dict:
    client = get_sync_client()
    db = client[settings.MONGO_DB]

    doc = db[ARTICLES_COL].find_one({"_id": ObjectId(article_id)})
    if not doc:
        logger.warning(f"[ANALYZE] article not found id={article_id}")
        return {"status": "not_found"}

    content = doc.get("content") or ""
    tags = doc.get("tags") or []

    word_count = len(content.split())
    unique_tags = len(set(tags))
    analysis = {"word_count": word_count, "unique_tags": unique_tags}

    db[ARTICLES_COL].update_one(
        {"_id": ObjectId(article_id)},
        {"$set": {"analysis": analysis, "updated_at": datetime.now(timezone.utc)}},
    )
    logger.info(f"[ANALYZE] article_id={article_id} -> {analysis}")
    return {"status": "ok", **analysis}
