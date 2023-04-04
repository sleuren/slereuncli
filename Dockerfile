FROM ubuntu

RUN apt-get update && apt-get -y install python3 && apt-get -y install pip
RUN pip install sleurencli

COPY sleurencli/test_cli.sh /

ENV api-key=""

#ENTRYPOINT [ "sleurencli", "config", "save", "--api-key" ]
CMD ["sh", "-c", "sleurencli config save --api-key ${api-key};sleurencli sites list;./test_cli.sh"]
