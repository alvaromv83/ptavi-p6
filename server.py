#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import SocketServer
import sys
import os


class EchoHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        """
        Método para recibir en el manejador y establecer comunicación SIP
        """
        # Escribe dirección y puerto del cliente (de tupla client_address)
        client_ip = str(self.client_address[0])
        client_port = str(self.client_address[1])
        print "IP cliente: " + client_ip + "| Puerto cliente: " + client_port

        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()

            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break
            else:
                # Evaluación de los parámetros que nos envía el cliente
                print "Recibido:\n" + line
                try:
                    parameters = line.split()
                    method = parameters[0]
                    protocol = parameters[1].split(':')[0]
                    address = parameters[1].split(':')[1]
                    login = address.split('@')[0]
                    server_ip = address.split('@')[1]
                    client_version = parameters[2]
                    if protocol != 'sip' or client_version != 'SIP/1.0'\
                        and client_version != 'SIP/2.0':
                        response = version + " 400 Bad Request\r\n\r\n"
                        self.wfile.write(response)
                        print "Enviado:\n" + response
                        break
                except:
                    response = version + " 400 Bad Request\r\n\r\n"
                    self.wfile.write(response)
                    print "Enviado:\n" + response
                    break

                # Evaluación del método que nos envía el cliente
                if method == 'INVITE':
                    response = version + " 100 Trying\r\n\r\n"
                    response += version + " 180 Ringing\r\n\r\n"
                    response += version + " 200 OK\r\n\r\n"
                    self.wfile.write(response)
                    print "Enviado:\n" + response
                elif method == 'BYE':
                    response = version + " 200 OK\r\n\r\n"
                    self.wfile.write(response)
                    print "Enviado:\n" + response
                elif method == 'ACK':
                    # --------------------- Envío RTP -------------------------
                    toRun = "./mp32rtp -i " + client_ip + " -p 23032 < "\
                            + AUDIO_FILE
                    print "Enviando contenido RTP al cliente..."
                    os.system(toRun)
                    print "Finalizado envío RTP"
                else:
                    response = version + " 405 Method Not Allowed\r\n\r\n"
                    self.wfile.write(response)
                    print "Enviado:\n" + response


if __name__ == "__main__":

    # Versión del protocolo SIP
    version = "SIP/2.0"

    # Evaluación de parámetros de la línea de comandos
    try:
        MY_IP = sys.argv[1]
        MY_PORT = int(sys.argv[2])
        AUDIO_FILE = sys.argv[3]
        if not os.path.isfile(AUDIO_FILE):
            sys.exit("Usage: python server.py ServerIP ServerPort audio_file")
    except:
        print ("Usage: python server.py ServerIP ServerPort audio_file")
        raise SystemExit

    # Creamos servidor de eco y escuchamos
    serv = SocketServer.UDPServer((MY_IP, MY_PORT), EchoHandler)
    print "Listening..."
    serv.serve_forever()
