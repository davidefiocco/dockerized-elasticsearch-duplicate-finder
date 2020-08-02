# Use elastic opensource version as runtime
FROM docker.elastic.co/elasticsearch/elasticsearch-oss:7.8.0

USER root
RUN chown elasticsearch:elasticsearch ./config/elasticsearch.yml
RUN echo "indices.query.bool.max_clause_count: 1000000" >> /usr/share/elasticsearch/config/elasticsearch.yml
RUN echo "discovery.type: single-node" >> /usr/share/elasticsearch/config/elasticsearch.yml
RUN cat /usr/share/elasticsearch/config/elasticsearch.yml
