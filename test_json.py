import json

with open('correos.json') as f:
    datos = json.load(f)

for p in datos['correos']:
    print('correo: {}'.format(p['usuario']))
    print('password: {}'.format(p['password']))
