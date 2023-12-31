import canopen


class CANOpen:
    def __init__(self, interface="can0"):
        self.nw = canopen.Network()
        self.nw.connect(bustype="socketcan", channel=interface)

    def send_high(self, message_id='0x240'):
        print(f"sending high to {message_id}")
        id = int(message_id, 16)
        self.nw.send_message(id, b'\x01', remote=False)

    def send_low(self, message_id='0x240'):
        print(f"sending low to {message_id}")
        id = int(message_id, 16)
        self.nw.send_message(id, b'\x00', remote=False)

    def send_message(self, message=b'\x00', message_id='0x240'):
        print(f"sending message to {message_id}")
        id = int(message_id, 16)
        self.nw.send_message(id, message, remote=False)

    def on_message_received(self, cob_id, data, timestamp):
        # Log the received message
        # print("Received message: cob_id={}, data={}, timestamp={}".format(cob_id, data, timestamp))

        # Es un código de ejemplo, se recomienda editar este callback para que haga lo que se necesite
        if data[0] == 1:
            print("HIGH")

        if data[0] == 0:
            print("LOW")

    def subscribe(self, message_id='0x260', callback_function=None):
        id = int(message_id, 16)
        listener = self.nw.subscribe(id, callback_function)
        print(f"subscribed to {message_id}")

    # Tambien es ejemplo, no es necesario utilizarlo
    def run(self):
        # Keep the program running to receive messages
        while True:
            # para ejecutar la funcion send_high y send_low cuando se reciba las teclas w y s de la terminal
            key = input("Enter a key: ")
            if key == "w":
                self.send_high()
            elif key == "s":
                self.send_low()
            else:
                print("Invalid key, please enter a valid key.")


import time

CAN_INTERFACE = 'can0'
TRIGGER_IN_MESSAGE_ID = '0xC8'
TRIGGER_OUT_MESSAGE_ID = '0xCD'


def message_callback(cob_id, data, timestamp):
    print(data)


def main():
    can_red = CANOpen(CAN_INTERFACE)
    can_red.subscribe(TRIGGER_IN_MESSAGE_ID, message_callback)

    # Bucle para seguir ejecutando el programa
    while True:
        can_red.send_message(message=b'\x01\x02\x03', message_id=TRIGGER_OUT_MESSAGE_ID)
        time.sleep(1)
        


if __name__ == '__main__':
    main()
