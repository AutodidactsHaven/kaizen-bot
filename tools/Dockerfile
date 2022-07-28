FROM ubuntu:18.04

RUN apt-get update && apt-get install -y \
 build-essential \
 clang \
 clang-tidy \
 clang-format \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
ADD tools/lint.sh /
RUN chmod +x /lint.sh

CMD ["/lint.sh"]