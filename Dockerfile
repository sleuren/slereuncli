FROM ubuntu

RUN apt-get update && apt-get -y install python3 && apt-get -y install pip
RUN pip install agent-cli

COPY agent-cli/test_cli.sh /

ENV api-key=""

#ENTRYPOINT [ "sleuren", "config", "save", "--api-key" ]
CMD ["sh", "-c", "sleuren config save --api-key ${api-key};sleuren sites list;./test_cli.sh"]
