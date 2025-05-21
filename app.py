from flask import Flask, request
import RPI.GPIO as GPIO


LED_PIN = 17 # physical pin 11
app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

@app.route('/led', methods=['POST'])
def control_led():
    data = request.get_json()
    state = data.get("state")

    if state == "on":
        GPIO.output(LED_PIN, GPIO.HIGH)
        return  {"status": "LED turned on"}, 200
    elif state == "off":
        GPIO.output(LED_PIN, GPIO.LOW)
        return {"status": "LED turned off"}, 200
    else:
        return {"error": "Invalid state. Use 'on' or 'off'."}, 400


@app.route("/")
def index():
    return """
        <h1>LED Controller</h1>
        <form method="POST" action="/led" onsubmit="send(event)">
            <button type="button" onclick="toggle('on')">Turn ON</button>
            <button type="button" onclick="toggle('off')">Turn OFF</button>
        </form>
        <script>
            function toggle(state) {
                fetch('/led', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({state: state})
                }).then(r => r.json()).then(data => alert(data.status || data.error));
            }
        </script>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
