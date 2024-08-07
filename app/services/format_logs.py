import datetime
import logging
import os

def formatLogs(name):
    #esta ruta debe se debe cambiar de acuerdo a su pc
    ruta_log = os.environ.get('LOG_ROUTE') # ruta de carpeta donde guardar los logs
    nombre_log = name + '.log'
    ruta_arch_log = os.path.join(ruta_log, nombre_log)
    my_logger = logging.getLogger(name)# podemos pasarle el nombre que queramos, por convención es recomendable que sea el nombre del módulo

    my_logger.setLevel(logging.WARNING)# Creamos un Handler para manejar el logger, le indicamos un nombre del archivo que guarde los logs

    if not my_logger.handlers:
        handler = logging.FileHandler(ruta_arch_log)# Creamos un Handler para manejar el logger, le indicamos un nombre del archivo que guarde los logs
        my_format = logging.Formatter('%(asctime)s - %(threadName)s - %(processName)s - %(levelname)s - %(message)s')# Creamos un formato
        handler.setFormatter(my_format) # seteamos el formato al handler
        my_logger.addHandler(handler)# Asociamos el handler al logger 
        my_logger.propagate = False# Para que se disasocie con el logger global, entonces los mensajes de este log tampoco vayan al log global
        
    #Para borrar, faltan algunas cosas 
    # Buscar archivos de logs antiguos y eliminarlos
    #for filename in os.listdir(ruta_log):
     #   if filename.endswith('.log'):
      #      filepath = os.path.join(ruta_log , filename)
       #     file_mtime = datetime.datetime.fromtimestamp(os.path.getmtime(filepath))
        #    try:
         #       if (datetime.datetime.now() - file_mtime).days > days_to_keep or os.path.getsize(filepath) > max_size:
          #          os.remove(filepath)
           # except OSError as e:
            #    my_logger.error(f"No se pudo eliminar el archivo {filepath}: {e}")
    return my_logger


