FROM nginx:latest

RUN apt-get update && apt-get install -y openssl
RUN mkdir /etc/nginx/ssl && openssl req -x509 -nodes -days 365 -out /etc/nginx/ssl/fiscolia.crt -keyout /etc/nginx/ssl/fiscolia.key -subj "/C=FR/ST=IDF/L=Paris/O=42/OU=42/CN=lflayeux.42.fr/UID=fiscolia"

COPY ./.conf /etc/nginx/templates/default.conf.template

CMD ["nginx", "-g", "daemon off;"]