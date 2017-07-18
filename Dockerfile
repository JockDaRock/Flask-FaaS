FROM python:alpine

ADD https://github.com/alexellis/faas/releases/download/0.5.6-alpha/fwatchdog /usr/bin
RUN chmod +x /usr/bin/fwatchdog

WORKDIR /root/

RUN pip install flask

ENV fprocess="python3 handler.py"

COPY handler.py .
HEALTHCHECK --interval=1s CMD [ -e /tmp/.lock ] || exit 1

CMD ["fwatchdog"]