#           TRACCIA 2
# Creare un web server semplice in Python che possa 
# servire file statici (come HTML, CSS, immagini) e 
# gestire richieste HTTP GET di base. 
# Il server deve essere in grado di 
# gestire più richieste simultaneamente e 
# restituire risposte appropriate ai client.


import socket
import threading
import os

def client_handle(client_socket):
    try:
        # Ricevo la richiesta del client
        request = client_socket.recv(1024).decode('utf-8')
        print(f"Richiesta ricevuta: {request}")
        
        # Estraggo il file della richiesta HTTP GET
        lines = request.split('\n')
        if len(lines) > 0:
            parts = lines[0].split(' ')
            if len(parts) > 1:
                filename = parts[1]
                if filename == '/':
                    filename = '/index.html'
                
                # Percorso del file
                filepath = f".{filename}"
                
                # Verifico se il file esiste e invio il contenuto
                if os.path.isfile(filepath):
                    with open(filepath, 'rb') as f:
                        content = f.read()
                    
                    # Determino il content type in base all'estensione del file
                    if filename.endswith(".html"):
                        content_type = "text/html"
                    elif filename.endswith(".css"):
                        content_type = "text/css"
                    elif filename.endswith(".txt"):
                        content_type = "text/plain"
                    elif filename.endswith(".jpg") or filename.endswith(".jpeg"):
                        content_type = "image/jpeg"
                    elif filename.endswith(".png"):
                        content_type = "image/png"
                    else:
                        content_type = "application/octet-stream"
                    
                    # Costruisco la risposta HTTP
                    response = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\nContent-Length: {len(content)}\r\n\r\n".encode()
                    response += content
                else:
                    # File non trovato, restituisco 404
                    response = b"HTTP/1.1 404 Not Found\r\n\r\n<html><body><h1>404 Not Found</h1></body></html>"
            else:
                # Richiesta non valida, restituisco 400
                response = b"HTTP/1.1 400 Bad Request\r\n\r\n<html><body><h1>400 Bad Request</h1></body></html>"
        else:
            # Richiesta non valida, restituisco 400
            response = b"HTTP/1.1 400 Bad Request\r\n\r\n<html><body><h1>400 Bad Request</h1></body></html>"
        
        # Invio la risposta al client
        client_socket.send(response)
    except Exception as e:
        print(f"Errore: {e}")
    finally:
        client_socket.close()  # Chiudo la connessione con il client

# Creo il socket del server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creo un socket TCP/IP
server_socket.bind(('localhost', 8080))  # Binding
server_socket.listen(10)  # Metto il socket in ascolto, coda di massimo 10 connessioni
print("Server in ascolto...")

# Inizio un ciclo infinito per accettare le connessioni in arrivo
while True:
    client_socket, addr = server_socket.accept()  # Accetto la connessione e restituisco un nuovo socket per la comunicazione
    print(f"Connessione da: {addr}")  # Stampo l'indirizzo del client che si è connesso
    
    # Gestisco ogni client in un thread separato
    client_handler = threading.Thread(target=client_handle, args=(client_socket,))  # Creo un nuovo thread per gestire la connessione del client
    client_handler.start()