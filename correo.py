class Correo:

    def __init__(self, correo, password):
        self.correo = correo
        self.password = password

    def __str__(self):
        return 'correo: {}, password: {}'.format(self.correo, self.password)

    def __repr__(self):
        return self.__str__()