FROM rclone/rclone:1.66 as rclone

FROM mongo:7.0.11-jammy

COPY --from=rclone /usr/local/bin/rclone /usr/local/bin/rclone

RUN apt-get -yqq update && apt-get install -yq  --no-install-recommends \
    curl \
    unzip \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

COPY copy_config.sh /usr/local/bin/copy_config.sh
RUN chmod +x /usr/local/bin/copy_config.sh

COPY backup.sh /usr/local/bin/backup.sh
RUN chmod +x /usr/local/bin/backup.sh

ENTRYPOINT [ "/usr/local/bin/copy_config.sh" ]
CMD [ "bash", "-c", "/usr/local/bin/backup.sh" ]