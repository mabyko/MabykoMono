FROM ubuntu:26.04@sha256:2260313b31c8c011cd2eebe728008efac1b3982be73eb71348ea2648d2c0e09b

ENV DEBIAN_FRONTEND=noninteractive
ENV UV_PYTHON=/usr/bin/python3 UV_PYTHON_DOWNLOADS=never
ENV PYTHONHASHSEED=0 TZ=UTC LANG=C.UTF-8

# Bootstrap HTTPS using the same snapshot's CA package; keep TLS verification on.
ADD --checksum=sha256:f7025ab9b24cd73215510931037b02d6960d89584d0d00afba81851abdbe6ef1 https://snapshot.ubuntu.com/ubuntu/20260905T000000Z/pool/main/c/ca-certificates/ca-certificates_20260223_all.deb /tmp/ca-certificates.deb
RUN dpkg-deb -x /tmp/ca-certificates.deb /tmp/ca-bootstrap \
    && mkdir -p /etc/ssl/certs \
    && cat /tmp/ca-bootstrap/usr/share/ca-certificates/mozilla/*.crt > /etc/ssl/certs/ca-certificates.crt \
    && echo 'Acquire::https::CaInfo "/etc/ssl/certs/ca-certificates.crt";' > /etc/apt/apt.conf.d/99ca-bootstrap \
    && rm -rf /tmp/ca-bootstrap /tmp/ca-certificates.deb \
    && sed -i 's|^URIs:.*|URIs: https://snapshot.ubuntu.com/ubuntu/20260905T000000Z/|' /etc/apt/sources.list.d/ubuntu.sources \
    && apt-get -o Acquire::Check-Valid-Until=false -o APT::Update::Error-Mode=any update \
    && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    fontconfig \
    fontforge \
    git \
    libharfbuzz-bin \
    python3 \
    unzip \
    xz-utils \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.12.10@sha256:2bb3ebca0a796a155094a27773d290c4b074572e6107f171d88d086682fd2500 /uv /usr/local/bin/uv

WORKDIR /work

CMD ["bash"]
