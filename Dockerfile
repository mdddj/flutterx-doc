FROM python:3.13-slim AS builder

ARG SITE_URL="https://mdddj.github.io/flutterx-doc/"
ARG ALT_LINK_ZH="/flutterx-doc/zh/"
ARG ALT_LINK_EN="/flutterx-doc/en/"
ARG ALT_LINK_JA="/flutterx-doc/ja/"

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    NO_MKDOCS_2_WARNING=1 \
    SITE_URL="${SITE_URL}" \
    ALT_LINK_ZH="${ALT_LINK_ZH}" \
    ALT_LINK_EN="${ALT_LINK_EN}" \
    ALT_LINK_JA="${ALT_LINK_JA}"

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY docs ./docs
COPY overrides ./overrides
COPY mkdocs.yml README.md ./

RUN mkdocs build --clean --strict


FROM nginx:1.27-alpine

COPY nginx.conf /etc/nginx/nginx.conf
COPY --from=builder /app/site /usr/share/nginx/html

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD wget -q -O /dev/null http://127.0.0.1/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
