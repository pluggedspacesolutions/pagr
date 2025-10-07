from django.core.management.base import BaseCommand
from users.models import Member
from whatsapp.utils import send_text_message
from django.utils import timezone

class Command(BaseCommand):
    help = "Send a scheduled message to all paid members (simple example)."

    def add_arguments(self, parser):
        parser.add_argument("--message", type=str, required=True, help="Message body to send")
        parser.add_argument("--paid-only", action="store_true", help="Send only to paid members")

    def handle(self, *args, **options):
        msg = options["message"]
        paid_only = options["paid_only"]

        qs = Member.objects.all()
        if paid_only:
            qs = qs.filter(is_paid=True)

        sent = 0
        for m in qs:
            try:
                send_text_message(m.phone, msg)
                sent += 1
            except Exception as e:
                self.stderr.write(f"Failed to send to {m.phone}: {e}")

        self.stdout.write(self.style.SUCCESS(f"Sent message to {sent} members at {timezone.now().isoformat()}"))