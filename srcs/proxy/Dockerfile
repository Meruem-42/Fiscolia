FROM docker.io/owasp/modsecurity-crs:3-nginx

RUN apt-get update
COPY ./.conf /etc/nginx/templates/conf.d/default.conf.template

CMD ["nginx", "-g", "daemon off;"]