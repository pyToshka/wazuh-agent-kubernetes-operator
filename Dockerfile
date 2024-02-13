FROM python:3.9-slim AS build-env
LABEL description='Wazuh Agent Kubernetes operator'
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1
COPY ./ /app
WORKDIR app
RUN pip install --no-cache-dir --upgrade -r requirements.txt && cp $(which kopf) /app  && rm -rf requirements.txt

FROM gcr.io/distroless/python3:nonroot
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/usr/local/lib/python3.9/site-packages
COPY --from=build-env /app /app
COPY --from=build-env /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
WORKDIR /app
CMD ["kopf", "run", "-A", "--standalone", "/app/main.py"]
