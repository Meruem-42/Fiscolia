FROM kibana:9.2.8

COPY ./conf/kibana.yml /usr/share/kibana/config/kibana.yml

COPY ./conf/init_dashboard.sh /tmp/script.sh

USER root
RUN chmod +rwx /tmp/script.sh
USER kibana

CMD /tmp/script.sh & /usr/local/bin/kibana-docker
