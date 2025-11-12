from app.workers.tasks import send_welcome_email


class CeleryMailer:
    async def send_welcome(self, user_id: str, email: str, name: str) -> None:
        send_welcome_email.delay(user_id, email, name)
