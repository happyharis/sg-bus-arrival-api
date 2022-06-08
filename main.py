from flask import Flask, request
import requests
from flask_cors import CORS


app = Flask('app')
CORS(app)

@app.route('/')
def query_bus_id():
    id = request.args.get('id')
    if (id):
        timings = get_bus_stop_timings(id)
        return timings

    else:
      return '''
      <p>
      To use, you have type in the bus stop number (e.g. <strong>18141</strong>) as such :

      https://sg-bus-arrival.haris-samingan.repl.co/?id=<strong>18141</strong>
      </p>
      '''


def get_bus_stop_timings(bus_stop_id):
    bus_timings = []
    api_url = f'https://arrivelah2.busrouter.sg/?id={bus_stop_id}'
    response = requests.get(api_url)
    services = response.json()['services']
    if (not services): return {"response": f'Bus stop {bus_stop_id} not found' }
    for service in services:
        bus_no = service['no']
        next_bus = service['next']
        next_bus_mins = round(next_bus['duration_ms'] / 1000 / 60)
        bus_timings.append({'bus_no': bus_no, 'next_bus_mins': next_bus_mins})

    return {"bus_stop_id": bus_stop_id, "services": bus_timings}


app.run(host='0.0.0.0', port=8080)
