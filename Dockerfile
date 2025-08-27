# epaal-backend/Dockerfile
FROM python:3.11-slim

# سیستم‌دیپندنسی‌ها
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential pkg-config libpq-dev libjpeg-dev zlib1g-dev wget \
  && rm -rf /var/lib/apt/lists/*

# کاربر امن + مسیر
RUN adduser --system --home /home/appuser --group appuser
WORKDIR /home/appuser/web

# پکیج‌ها
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# کد + entrypoint
COPY . .
COPY entrypoint.sh /home/appuser/web/entrypoint.sh
RUN chmod +x /home/appuser/web/entrypoint.sh \
 && mkdir -p /home/appuser/web/vol/static /home/appuser/web/vol/media \
 && chown -R appuser:appuser /home/appuser/web

USER appuser
EXPOSE 8000
CMD ["/home/appuser/web/entrypoint.sh"]
