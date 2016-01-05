import sys
import socket #Para conexão externa
import string #
import wikipedia
import requests
#Importing Proxy Library
import socks

def main():
    HOST="YOUR HOST HERE"
    PORT=6667
    NICK="NICKNAME"
    PASSWORD = "PASSWORD"
    IDENT="IDENTITY"
    REALNAME="REAL NAME"
    CHANNEL = "#default"
    JOINSTRING = " JOIN :" + CHANNEL

    wikipedia.set_lang("pt") #Set the Wikipedia Language


    MENSAGENS = []


    #CONFIGURA O SOCKET

    s=socket.socket( )

    # Para funcionar com proxy teria de usar a linha comentada nos imports e excluir a linha de cima!
    #s = socks.socksocket()#abre o socket com o socksipy
    # PROXY DE ISRAEL!
    # PROXYS: COREANO(125.143.136.21:8080) CHINÊS(117.187.10.140:80)
    #s.setproxy(socks.PROXY_TYPE_SOCKS5, '213.57.90.253', 18000)# - trocar localhost por ip do proxy
    # Acessar porta encriptada do IRC, para proteção!
    s.connect((HOST, PORT))
    s.settimeout(None)
    s.send(bytes("NICK " + NICK + "\r\n", "utf-8"))
    s.send(bytes("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME), "utf-8"))
    #JOIN MAIN CHANNEL HERE AFTER WE JOIN THE OTHER CHANNELS!
    s.send(bytes("JOIN #" + CHANNEL + "\r\n", "utf-8"))
    s.send(bytes('PRIVMSG NickServ :IDENTIFY {}\n'.format(PASSWORD), 'utf-8'))

    while True:
        # list channels before joining
        # /list on IRC
        # JOIN ALL CHANNELS!!!!!! <= VEWY IMPORTANT
        # Dont join &server, only # ones
        buffer = s.recv(12288)
        textodecodado = buffer.decode("utf-8")
        print(textodecodado)
        if textodecodado.find('PING') != -1:
                dividido = textodecodado.split(":")
                dividido = dividido[1].split("PRIVMSG ")
                stringnova = ("PONG " + dividido[0] + "\r\n")
                s.send(bytes(stringnova,"utf-8"))


        #CREATE THE -H COMMAND, THE HELPER!
        if textodecodado.find('Hello ' + NICK) != -1:
                textodecodado2 = textodecodado.split(":")
                nomedouser = textodecodado2[1].split("!")
                nomedouser = nomedouser[0]
                if nomedouser == "limecd":
                    s.send(bytes('PRIVMSG #' + CHANNEL + ' :Hello my lord ' + nomedouser + ' ! \r\n',"utf-8"))
                else:
                    s.send(bytes('PRIVMSG #' + CHANNEL + ' :Hello ' + nomedouser + ' ! \r\n',"utf-8"))


        if textodecodado.find('-w') != -1:
                stringseparate = ("#" + CHANNEL + " :")
                separadao = textodecodado.split(stringseparate)
                separadao = separadao[1].split("-w ")
                busca = separadao[1]

                try:
                    print(wikipedia.summary(busca, sentences=1))
                    LimitedSearch = wikipedia.summary(busca, sentences=1).strip()
                    s.send(bytes('PRIVMSG #' + CHANNEL + ' : ' + LimitedSearch[:450] + "\r\n", "utf-8"))
                except:
                    s.send(bytes('PRIVMSG #' + CHANNEL + " : I couldnt find any result for: " + busca + "\r\n", "utf-8"))



        if textodecodado.find('-s') != -1:

                URLSeparada01 = textodecodado.split("#" + CHANNEL + " :")
                try:
                    UrlParaEncurtar = URLSeparada01[1].split("-s ")
                    link = "http://tinyurl.com/create.php?source=indexpage&url=%s&submit=Make+TinyURL!&alias=" %(UrlParaEncurtar[1])
                    r = requests.get(link)
                    hook = r.text.find("and resulted in the following TinyURL")
                    urlEncurtadaTotal = r.text[r.text.find("<b>", hook)+3:r.text.find("</b>", hook)]
                    s.send(bytes('PRIVMSG #' + CHANNEL + " : Shorten: " +  urlEncurtadaTotal + "\r\n", "utf-8"))
                except:
                    print("Hello world")

        if textodecodado.find("PRIVMSG #" + CHANNEL) != -1:
                # IF para saber quando logou
                # IF ocorre quando isto aparecer: :NickServ!services@cloaked.host NOTICE NICK :Password accepted - you are now recognized.
                # IF para não escrever mensagens de hello:
                # IF ocorre quando :inexbot!~inexbot@cloaked.host PRIVMSG #CHANNEL :Hello limebot!
                # APENDAR DATA JUNTO A MENSAGEM, ASSIM PEGAREMOS O DIA E HORA!
                MENSAGENS.append(textodecodado)


        if textodecodado.find(JOINSTRING) != -1:
                textodecodado2 = textodecodado.split(":")
                nomedouser = textodecodado2[1].split("!")
                nomedouser = nomedouser[0]
                print(nomedouser)
                if nomedouser == NICK:
                    s.send(bytes('I joined this channel','utf-8'))
                else:
                    s.send(bytes('PRIVMSG #' + CHANNEL + ' :U r very welcome here ' + nomedouser + ' !!! \r\n', 'utf-8'))

        textoArquivo = open("irc.txt", "a")
        for item in MENSAGENS:

            # ENCRIPTAR MENSAGENS PARA SOMENTE COM A CHAVE DESCOBRIR O QUE SIGNIFICAM
            textoArquivo.write(item) # escrever as mensagens com as datas, acompanhar acontecimentos do irc!

        textoArquivo.close()


if __name__ == "__main__":
    main()
