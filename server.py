import socket
import threading
import pickle

# Zmienne stanu gry
starting = True
player_pick = "None"
computer_pick = "None"

HOST = '127.0.0.1'  # Adres pętli zwrotnej
PORT1 = 5555
PORT2 = 5556

# Słownik przechowujący numery graczy i odpowiadające im sockety
players = {}

def handle_client(client_socket, player_num):
    global players
    global starting
    global player_pick, computer_pick

    try:
        while starting:
            # Odbierz dane od klienta
            data = pickle.loads(client_socket.recv(1024))
            if not data:
                break

            # Aktualizuj zmienne dla danego gracza
            player_num = data.get("player_num", player_num)
            if player_num == 1:
                player_pick = data.get("player_pick", "None")
            elif player_num == 2:
                computer_pick = data.get("computer_pick", "None")

            
            # Wyświetl odebrane dane od gracza
            received_data = {
                "player_num": player_num,
                "player_pick": player_pick,
                "computer_pick": computer_pick
            }
            print(f"Received data from Player {player_num}: {received_data}")
            # Wysyłamy dane z powrotem do obu klientów
            for num, player_socket in players.items():
                if num != player_num:
                    player_socket.sendall(pickle.dumps({
                        "player_num": player_num,
                        "player_pick": player_pick,
                        "computer_pick": computer_pick,
                        "starting": starting
                    }))

    except Exception as e:
        print(f"Błąd obsługi klienta {player_num}: {e}")



    # Zamknij połączenie po rozłączeniu się klienta
    del players[player_num]
    client_socket.close()

# Funkcja obsługująca połączenia od klientów
def accept_connections():
    global players
    global starting

    while starting and len(players) < 2:
        try:
            client, addr = server.accept()
            print(f"Nowe połączenie od {addr}")

            # Przypisz numer gracza i dodaj klienta do listy
            player_num = len(players) + 1
            players[player_num] = client

            # Wybierz port na podstawie numeru gracza
            port = PORT1 if player_num == 1 else PORT2

            # Wypisz informację o liczbie połączonych klientów
            print(f"Liczba połączonych klientów: {len(players)}")

            # Rozpocznij obsługę klienta w nowym wątku
            client_handler = threading.Thread(target=handle_client, args=(client, player_num))
            client_handler.start()

        except Exception as e:
            print(f"Błąd akceptowania połączenia: {e}")
            break

# Definicje obiektów serwera
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT1))
server.listen()

server2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server2.bind((HOST, PORT2))
server2.listen()

# Wiadomość podczas uruchamiania
print("Serwer uruchomiony. Oczekiwanie na połączenia...")

# Definicje wątków
accept_thread = threading.Thread(target=accept_connections)
accept_thread.start()

while starting:
    try:
        client_socket, addr = server2.accept()
        received_data = pickle.loads(client_socket.recv(1024))
        print(received_data)
        pass
    except KeyboardInterrupt:
        print("Serwer zatrzymany.")
        starting = False
        break
    except Exception as e:
        print(f"Błąd w głównej pętli serwera: {e}")

# Zamknij wszystkie połączenia przed zakończeniem programu
for player_socket in players.values():
    player_socket.close()
accept_thread.join()
server.close()
server2.close()
