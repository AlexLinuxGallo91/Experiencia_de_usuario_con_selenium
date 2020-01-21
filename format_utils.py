class FormatUtils:

    #remueve los espacios en los textos de los elementos HTML
    @staticmethod
    def remover_backspaces(cadena):
        return cadena.replace('&nbsp;', ' ')

    