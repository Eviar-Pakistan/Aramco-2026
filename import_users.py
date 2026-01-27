import os
import django

# Set up Django environment using your project name
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aramco.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
created, skipped, errors = 0, 0, 0

with open("coco_aramco_users.txt", "r", encoding="utf-8") as file:
    for line in file:
        line = line.strip()
        if line and line.startswith("username:"):
            try:
                # Example line format:
                # username: PulseTiger01, password: Tiger@101 || Location: COCO ARAMCO 1 - LIBERTY
                parts = line.split("||")
                creds = parts[0].replace("username:", "").replace("password:", "").split(",")
                username = creds[0].strip()
                password = creds[1].strip()
                # location = parts[1].replace("Location:", "").strip()   # Uncomment if needed

                if User.objects.filter(username=username).exists():
                    print(f"SKIPPED (already exists): {username}")
                    skipped += 1
                    continue

                user = User.objects.create_user(
                    username=username,
                    password=password,
                    is_superuser=False,
                    is_staff=False,
                    is_active=True
                )
                user.save()
                print(f"CREATED: {username}")
                created += 1
            except Exception as e:
                print(f"ERROR on line: {line}\n  {e}")
                errors += 1

print(f"\nCompleted!\nCreated: {created}, Skipped: {skipped}, Errors: {errors}")