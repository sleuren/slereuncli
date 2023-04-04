FROM ubuntu

RUN apt-get update && apt-get -y install python3 && apt-get -y install pip
RUN pip install sleurencli

COPY sleurencli/test_cli.sh /

ENV api-key=""

#ENTRYPOINT [ "sleuren", "config", "save", "--api-key" ]
CMD ["sh", "-c", "sleuren config save --api-key ${api-key};sleuren sites list;./test_cli.sh"]
