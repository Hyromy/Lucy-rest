FROM python:3.12-slim

RUN useradd --create-home --shell /bin/bash app

WORKDIR /home/app

COPY --chown=app:app requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

USER app

COPY --chown=app:app . .

RUN python manage.py collectstatic --no-input

EXPOSE 8000

CMD ["sh", "-c", "\
    set -o errexit && \
    python manage.py migrate && \
    python create_super_user.py && \
    gunicorn project.wsgi:application \
        --bind 0.0.0.0:8000 \
        --workers 1 \
        --worker-class sync \
"]
