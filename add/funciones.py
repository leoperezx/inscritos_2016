def eliminar_nuevaLinea(col):
    '''
    Eliminar nueva linea de un string.
    '''
    colNombres = col.str.replace('\n', '')
    return colNombres
