# ������� ����� � Python
FROM python:3.12-slim-bullseye

# ������������� ���������� ��������� ��� Python
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_ROOT_USER_ACTION=ignore

# ������������� ������� ���������� ������ ����������
WORKDIR /bestcar

# ������������� ��������� �� UTC
RUN ln -snf /usr/share/zoneinfo/UTC /etc/localtime && \
    echo "UTC" > /etc/timezone

# �������� ���� ������������ � ���������
COPY requirements.txt ./

# ������������� ��������� ����������� � ����������� Python
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    netcat && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# �������� ���� ��� ������� � ���������
COPY . .

# �������� entrypoint.sh � ������ ��� ����������
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# ��������� ����, ������� ����� ������������ Django (�� ��������� 8000)
EXPOSE 8000

# ������������� ����� ����� ��� ����������
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# ��������� ������� �� ��������� ��� ������� Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]