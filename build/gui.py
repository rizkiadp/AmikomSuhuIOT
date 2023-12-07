from tkinter import Tk, Canvas, PhotoImage
from pathlib import Path
import paho.mqtt.client as mqtt
import ssl

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Asus\Downloads\Tkinter-Designer-master\Tkinter-Designer-master\DahboardIot\build\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.geometry("600x400")
        self.root.configure(bg="#FFFFFF")

        self.canvas = Canvas(
            root,
            bg="#FFFFFF",
            height=400,
            width=600,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        # Load the image
        self.head_img_path = relative_to_assets("head_img.png")
        self.head_img = PhotoImage(file=self.head_img_path)

        # Display the image on the left side of the canvas
        self.canvas.create_image(40, 10, anchor="nw", image=self.head_img)

        # Display text on the canvas
        self.label_kelembaban = self.canvas.create_text(
            25.0,
            309.0,
            anchor="nw",
            text="Kelembaban: ",
            fill="#000000",
            font=("Inter", 12 * -1)
        )

        self.label_suhu = self.canvas.create_text(
            25.0,
            289.0,
            anchor="nw",
            text="Suhu: ",
            fill="#000000",
            font=("Inter", 12 * -1)
        )

        # MQTT Configuration
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT broker")
                client.subscribe("iot/dashboard")
            else:
                print("Connection failed with code", rc)

        def on_message(client, userdata, msg):
            payload = msg.payload.decode()
            if "kelembaban" in payload:
                self.update_kelembaban(payload.split(":")[1])
            elif "suhu" in payload:
                self.update_suhu(payload.split(":")[1])

        ssl_settings = ssl.SSLContext(ssl.PROTOCOL_TLS)
        auth = {'username': 'hivemq.webclient.1701962686944', 'password': ':cEi;1A4LlaYS>5?h0bJ'}
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = on_connect
        self.mqtt_client.on_message = on_message
        self.mqtt_client.username_pw_set(auth['username'], auth['password'])
        self.mqtt_client.tls_set_context(ssl_settings)

        self.mqtt_client.connect('ec15c3ca151c4ebdacb8f1643f951a48.s1.eu.hivemq.cloud', port=8883)
        self.mqtt_client.loop_start()

    def update_kelembaban(self, value):
        self.canvas.itemconfig(self.label_kelembaban, text=f"Kelembaban: {value}%")

    def update_suhu(self, value):
        self.canvas.itemconfig(self.label_suhu, text=f"Suhu: {value}°C")

if __name__ == "__main__":
    root = Tk()
    dashboard = Dashboard(root)
    root.mainloop()
