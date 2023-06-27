# =====================
# --- Builder Stage ---
# =====================
FROM postgres:14.6 AS builder

ENV POSTGRES_PASSWORD=password
ENV POSTGRES_USER=postgres
ENV POSTGRES_DB=app
ENV POSTGRES_HOST_AUTH_METHOD=trust
ENV PGDATA=/data

COPY docker/scripts/db-import.sh /docker-entrypoint-initdb.d/
COPY ietfa.torchbox.latest.gz /

RUN ["sed", "-i", "s/exec \"$@\"/echo \"skipping...\"/", "/usr/local/bin/docker-entrypoint.sh"]
RUN ["/usr/local/bin/docker-entrypoint.sh", "postgres"]

# ===================
# --- Final Image ---
# ===================
FROM postgres:14.6
LABEL maintainer="IETF Tools Team <tools-discuss@ietf.org>"

COPY --from=builder /data $PGDATA

ENV POSTGRES_PASSWORD=password
ENV POSTGRES_USER=postgres
ENV POSTGRES_DB=app
ENV POSTGRES_HOST_AUTH_METHOD=trust
