FROM registry1.dso.mil/ironbank/opensource/python:v3.12

USER python

RUN if [ ! -f /tmp/debug.txt ]; then touch /tmp/debug.txt ; fi && \
    chmod a=rwx /tmp/debug.txt && \
    mkdir -p /tmp/app/eccr-cis

WORKDIR /tmp/app/eccr-cis

COPY --chown=python:python . .

COPY --chown=python:python --chmod=755 start-server.sh start-app.sh /tmp/app/eccr-cis/

ENV PYTHONPATH /tmp/app/eccr-cis/.cache/python-packages
ENV PATH $PATH:/tmp/app/eccr-cis/.cache/python-packages/bin

RUN rm -rf /home/python/.cache/python-packages/tornado/test/test.key \
    /tmp/app/.cache/python-packages/tornado/test/test.key \
    /tmp/app/eccr-cis/.cache/python-packages/tornado/test/test.key

# start server
EXPOSE 8020
STOPSIGNAL SIGTERM
