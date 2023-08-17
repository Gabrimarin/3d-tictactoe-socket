import socket
import threading
import tablegui

global connection
global connection_accepted
global connection_thread

#HOST = "127.0.0.1"
HOST_IP = "0.0.0.0"
MY_IP = socket.gethostbyname(socket.gethostname())
PORT = 65434


def handle_receive():
    try:
        while True:
            data = connection.recv(1024)
            if not data:
                break
            decoded = data.decode().strip()
            message_type = decoded[0]
            message_body = decoded[1:]
            if message_type == '@':
                gui.append_message(f"Enemy: {message_body}")
            if message_type == '#':
                x, y, z = int(message_body[0]), int(message_body[2]), int(message_body[4])
                gui.make_move(x, y, z)
            if message_type == '$':  # give up
                gui.show_disconnected_screen()
                break

    except Exception as e:
        print(f"Error: {e}")
    finally:
        connection_thread.join()
        print("Connection closed.")
        connection.close()


def handle_connection_as_host():
    global connection
    global connection_accepted
    connection_accepted = False
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST_IP, PORT))
        s.listen()
        print("Server listening...")
        gui.show_waiting_screen(MY_IP, False)
        while True:
            connection, addr = s.accept()
            connection_accepted = True
            gui.start_game(handle_send_message, handle_send_move, handle_send_give_up, 1)
            handle_receive()
    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        s.close()


def handle_connection_as_guest(ip):
    global connection
    global connection_accepted
    connection_accepted = False
    gui.show_waiting_screen(ip, True)
    try:
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect((ip, PORT))
        connection_accepted = True
        gui.start_game(handle_send_message, handle_send_move, handle_send_give_up, 2)
        handle_receive()
    except Exception as e:
        gui.hide_waiting_screen()
        gui.show_connection_screen()
        print(f"Error: {e}")
    finally:
        connection.close()


def handle_start_connection(ip):
    if ip:
        connection_thread = threading.Thread(target=handle_connection_as_guest, args=(ip,)).start()
    else:
        connection_thread = threading.Thread(target=handle_connection_as_host).start()


gui = tablegui.TableGUI(handle_start_connection)

def handle_send_message(message):
    try:
        if connection_accepted:
            connection.sendall(f"@{message}".encode())
            return True
        return False
    except:
        return False


def handle_send_move(x, y, z):
    try:
        if connection_accepted:
            connection.sendall(f"#{x}x{y}x{z}".encode())
            return True
        return False
    except:
        return False

def handle_send_give_up():
    try:
        if connection_accepted:
            connection.sendall(f"$".encode())
            return True
        return False
    except:
        return False


def main():
    gui.mainloop()


if __name__ == "__main__":
    main()
