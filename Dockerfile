ARG IMAGE_FROM
FROM ${IMAGE_FROM}
ENV PORT 5000
ADD tstamp.py requirements.txt entrypoint.sh /app/
WORKDIR /app
RUN useradd user && pip3 install -r requirements.txt
EXPOSE $PORT
USER user
ENTRYPOINT ["/app/entrypoint.sh"]
CMD []
