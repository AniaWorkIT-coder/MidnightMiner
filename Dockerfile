# Etap 1: Budowanie środowiska zależności
FROM python:3.12 AS build

WORKDIR /app

COPY requirements.txt .

# Instalacja zależności w osobnym katalogu (lepsza warstwizacja i cache)
RUN pip install --user --no-cache-dir -r requirements.txt

# Etap 2: Docelowy obraz aplikacji
FROM python:3.12

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY --from=build /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

COPY . .

# Dla najbardziej typowego startu, np. aplikacji webowej
CMD ["python", "miner.py", "--no-donation", "--workers", "1"]
