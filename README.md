-Carpeta data
	-Carpeta annotations: Contiene los archivos XML de cada una de las imagenes de las tarjetas bancarias.
	-Carpeta images: Contiene las imagenes de las tarjetas bancarias con las que se realizaron los XML.
	-Archivo train.record: Es el archivo TFRecord que se supone servira de entrenamiento para el modelo de aprendizaje automatico
-Carpeta models:Sirve para ejecutar el script de generar_TFRecord.py.
-Carpeta tarjetas: Contiene las imagenes de las tarjetas bancarias.
-Archivo generar_TFRecord.py: Script para generar el archivo TFRecord de entrenamiento.
-Archivo interfaz: En teoría, después de haber terminado el modelo de aprendizaje automatico se implementara en esta interfaz de PyQt5.
