import socket
import threading
import tablegui

global connection
global connection_accepted
global connection_thread

#HOST = "127.0.0.1"
HOST_IP = "0.0.0.0"
PORT = 65434

def get_my_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    return IP

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
                gui.hide_game_screen()
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
        MY_IP = get_my_ip()
        s.bind((MY_IP, PORT))
        s.listen()
        print("Server listening...")
        gui.hide_connection_screen()
        gui.show_waiting_screen(MY_IP, False)
        while True:
            connection, addr = s.accept()
            connection_accepted = True
            gui.hide_waiting_screen()
            gui.start_game(handle_send_message, handle_send_move, handle_send_give_up, 1)
            handle_receive()
    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        s.close()
        connection_thread.join()


def handle_connection_as_guest(ip):
    global connection
    global connection_accepted
    connection_accepted = False
    gui.hide_connection_screen()
    gui.show_waiting_screen(ip, True)
    try:
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect((ip, PORT))
        connection_accepted = True
        gui.hide_waiting_screen()
        gui.start_game(handle_send_message, handle_send_move, handle_send_give_up, 2)
        handle_receive()
    except Exception as e:
        gui.show_connection_screen()
        print(f"Error: {e}")
    finally:
        connection.close()
        connection_thread.join()


def handle_start_connection(ip):
    global connection_thread
    if ip:
        connection_thread = threading.Thread(target=handle_connection_as_guest, args=(ip,))
    else:
        connection_thread = threading.Thread(target=handle_connection_as_host)
    connection_thread.start()


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
            gui.hide_game_screen()
            gui.show_disconnected_screen()
            return True
        return False
    except:
        return False


def main():
    gui.mainloop()


if __name__ == "__main__":
    main()
