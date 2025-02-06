FROM python:3.12-slim-bookworm as builder

# Copy the necessary files for Poetry to the generate the requirements file from
COPY ../pyproject.toml ../poetry.lock /tmp/workdir/

RUN pip3 install poetry==1.8.* poetry-plugin-export

RUN cd /tmp/workdir && poetry export --without-hashes -f requirements.txt -o requirements.txt


FROM rclone/rclone:1.66 as rclone

FROM python:3.12-slim-bookworm

# Set environment variables to reduce output from debconf
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y --no-install-recommends \
    wget \
    gnupg \
    lsb-release \
    tini \
    sudo \
    && rm -rf /var/lib/apt/lists/*

RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor -o /usr/share/keyrings/postgresql-archive-keyring.gpg

RUN echo "deb [signed-by=/usr/share/keyrings/postgresql-archive-keyring.gpg] http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list

RUN apt update && apt install -y \
    postgresql-client-16 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=rclone /usr/local/bin/rclone /usr/local/bin/rclone

COPY --from=builder /tmp/workdir/requirements.txt /tmp/requirements.txt

RUN pip3 install -r /tmp/requirements.txt

COPY main.py /main.py

ENTRYPOINT ["/usr/bin/tini", "--"]

CMD [ "python", "-u", "/main.py" ]