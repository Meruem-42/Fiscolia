FROM nginx:latest

RUN apt-get update
RUN apt-get install -y bison build-essential ca-certificates curl dh-autoreconf doxygen \
    flex gawk git iputils-ping libcurl4-gnutls-dev libexpat1-dev libgeoip-dev liblmdb-dev \
    libpcre2-dev libssl-dev libtool libxml2 libxml2-dev libyajl-dev locales \
    liblua5.3-dev pkg-config wget zlib1g-dev libxslt1-dev libgd-dev
RUN cd /opt \
    git clone --depth 1 -b v3/master https://github.com/SpiderLabs/ModSecurity \
    cd ModSecurity \
    git submodule update --init --recursive \
    ./build.sh \
    ./configure \
    make \
    sudo make install

COPY ./.conf /etc/nginx/templates/default.conf.template

CMD ["nginx", "-g", "daemon off;"]