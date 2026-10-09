# postgres:17.2
FROM postgres@sha256:3267c505060a0052e5aa6e5175a7b41ab6b04da2f8c4540fc6e98a37210aa2d3

# Adding permissions to postgres user
USER 0
RUN mkdir -p /var/lib/postgresql/data && \
    chown -R 999:999 /var/lib/postgresql/data /var/run/postgresql && \
    chmod 700 /var/lib/postgresql/data && \
    chmod 775 /var/run/postgresql
USER 999