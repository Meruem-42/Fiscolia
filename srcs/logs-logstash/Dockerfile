FROM logstash:9.2.8

COPY ./conf/logstash.conf /etc/logstash/conf.d/logstash.conf

EXPOSE 12201/udp

EXPOSE 9600

CMD ["logstash", "-f", "/etc/logstash/conf.d/logstash.conf"]