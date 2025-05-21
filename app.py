from flask import Flask, request
import RPi.GPIO as GPIO


LED_PIN = 17 # physical pin 11
BUTTON_PIN = 27 # physical pin 13
app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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

@app.route('/button', methods=['POST'])
def button_state():
    state = GPIO.input(BUTTON_PIN)
    return {"pressed": state == GPIO.LOW}


@app.route("/")
def index():
    return """
        <h1>LED Controller</h1>
        <form method="POST" action="/led" onsubmit="send(event)">
            <button type="button" onclick="toggle('on')">Turn ON</button>
            <button type="button" onclick="toggle('off')">Turn OFF</button>
        </form>
        <div id="status" style="margin-top: 20px; font-weight: bold;">Tila: Tuntematon</div>
        <div id="buttonState" style="margin-top: 10px; font-size: 18px; color: white; background: gray; display: inline-block; padding: 10px; border-radius: 5px;">
            Painikkeen tila: Tuntematon
        </div>

        <script>
            function toggle(state) {
                fetch('/led', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({state: state})
                }).then(r => r.json()).then(data => {
                    document.getElementById("status").textContent = "Tila: " + (data.status || data.error);
                });
            }

            // Pollaa /button endpointtia 1 sekunnin välein
            setInterval(() => {
                fetch('/button')
                    .then(r => r.json())
                    .then(data => {
                        const el = document.getElementById("buttonState");
                        if (data.pressed) {
                            el.textContent = "Painikkeen tila: Painettu";
                            el.style.background = "blue";
                        } else {
                            el.textContent = "Painikkeen tila: Ei painettu";
                            el.style.background = "gray";
                        }
                    });
            }, 1000);
        </script>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
