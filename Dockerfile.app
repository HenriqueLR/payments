FROM henriquelr89/ubuntu-versions:20.04
MAINTAINER henrique.lr89@gmail.com

RUN mkdir -p /deploy/apps/payments/
ADD . /deploy/apps/payments/

WORKDIR /deploy/apps/payments
RUN ./env/app/install.sh
COPY ./env/app/entrypoint.sh /deploy/apps/payments

RUN chown -R payments:payments /deploy/apps/payments/

USER payments

ENTRYPOINT ["sh", "/deploy/apps/payments/env/app/entrypoint.sh"]
