import cv2
import base64
import json
import http.client

# Cargamos una imagen, luego va a base64, a un mapa y a un JSON
img = cv2.imread('austin1.tif')
png_encoded_img = cv2.imencode('.jpg', img)
base64_encoded_img = base64.b64encode(png_encoded_img[1])
message = {'img': base64_encoded_img.decode('UTF-8')}
json_message = json.dumps(message)

# Creamos conexión, cabecera y enviamos el mensaje con un POST
headers = {'Content-type': 'application/json'}
connection = http.client.HTTPConnection('127.0.0.1', port=8000)
connection.request('POST','', json_message, headers)

# Esperamos la respuesta y la pintamos por pantalla
resp = connection.getresponse()
result = json.loads(resp.read().decode())
print(result["result"])

