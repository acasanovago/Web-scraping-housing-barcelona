# Tipología y ciclo de vida de los datos
#### Práctica 1: Web scraping

## El contexto
Esta práctica se ha realizado bajo el contexto de la asignatura Tipología y ciclo de vida de los datos, perteneciente al
Máster en Ciencia de Datos de la Universitat Oberta de Catalunya. En ella, se aplican técnicas de web scraping mediante 
el lenguaje de programación Python para extraer datos de la web de idealista y generar un dataset.

## Miembros del equipo
La actividad ha sido realizada conjuntamente por **Albert Casanova González** y **Xuan Zheng**.

## Objetivos del proyecto

Obtener un dataset con los datos de los pisos en venta en la web de idealista de tres zonas del este de Barcelona. Por
cada zona recorreremos los barrios y obtendremos la información disponible en las N primeras páginas.

Los datos obtenidos por cada uno de los pisos en venta son los siguientes:

``` python
['price', 'room', 'space', 'name', 'link', 'city', 'area', 'subarea', 'page']
```

* Price: precio del piso publicado.
* Room: número de habitaciones.
* Space: m2 disponibles en el piso.
* Name: nombre del anuncio publicado.
* Link: enlace al detalle del anuncio.
* City: ciudad en la que se encuentra el piso.
* Area: área en la que se ha realizado la búsqueda.
* Subarea: zona dentro del área elegida.
* Page: página en la paginación de Subarea en la que se encontraba el anuncio.

## Estructura del proyecto

* csv/
  * csv/housing-barcelona.csv
* src/
  * src/idealista_scraper.py
* .gitignore
* LICENSE
* README.md
* requirements.txt

1. La carpeta csv/ contiene el fichero **housing-barcelona.csv** con el resultado del último scraping.
2. La carpeta src/ contiene el código fuente de la aplicación:
   * 2.1 src/idealista.scraper.py contiene la implementación del scraper que recoge los datos de la web de idealista.
3. .gitignore contiene las carpetas y archivos que queremos ignorar al subir el código al repositorio.
4. LICENSE corresponde a la licencia del proyecto.
5. README.md es el archivo que estás leyendo, con la explicación del proyecto.
6. requirements.txt son las dependencias a instalar.

## Utilización

### Instalar los requerimientos

Debemos instalar los requerimientos del proyecto. Si se quiere, se puede crear un entorno virtual, pero esto
es a elección de la persona que utiliza el paquete.
```bash
$ pip install -r  requeriments.txt
```

### Ejecutar el scraper


#### Scraper de la web de idealista para obtener los datos de Barcelona zona Este.

En la primera ejecución, el scraper se va a descargar el geckodriver si no lo tienes para poder utilizar Selenium con 
Firefox. Idealista utiliza el Captcha de Google para bloquear las peticiones que parecen de robots, por lo que en la
primera llamada el programa esperará que pulsemos ENTER después de solucionar el captcha a mano. 

El captcha empieza a saldar a partir de la segunda ejecución, por lo que, si al ejecutar el programa no salta, lo ideal 
es pararlo con CONTROL + C y después volver a ejecutarlo hasta que aparezca el captcha en la primera llamada (en los 
tests realizados siempre ha aparecido a partir de la segunda ejecución del día).

Una vez solucionado el captcha una vez, en esa sesión no volverá a saltar y ya no será necesario pausar la aplicación.
Es posible que este comportamiento cambie en un futuro, lo que requeriría cambios en el código si este
comportamiento no es el esperado.

Los pasos de ejecución son los siguientes:

```bash
$ python ./src/idealista_scraper.py
```
* Verificamos en el navegador de Selenium si ha saltado el Captcha.
  * En caso afirmativo, solucionamos el Captcha y pulsamos ENTER.
  * En caso negativo, pulsamos CONTROL + C para parar la ejecución y volvemos a empezar.
* Comprobamos los logs que saldrán por pantalla que el scraper no lance ninguna excepción.
* Comprobamos el resultado del fichero csv/housing-barcelona.csv para verificar el dataset obtenido.

### Configuración del comportamiento del scraper

El scraper funciona con cualquier barrio de idealista, permite modificar la url base por si en lugar de idealista.com
se quiere utilizar un proxy, permite elegir el número de páginas entre 1 y 6 (se podría
subir dicho límite si se implementa la funcionalidad que pulse el botón "Siguiente" en la paginación, ya que desde la
primera página solo hay las 6 primeras disponibles), también permite modificar el tiempo de espera (en segundos) entre 
llamadas por si cambia el comportamiento y 1s de espera no es suficiente, permite elegir el path dónde guardaremos el 
csv resultante y, finalmente, permite elegir esperar o no al Captcha la primera vez si se implementa una solución que
lo evite. Las variables globales para configurar el scraper se encuentaran en src/idealista_scraper.py:

```python
URL_BASE = "https://www.idealista.com" # cambiar si se utiliza un proxy
MAX_PAGES = 5 # páginas por zona que vamos a analizar, mínimo 1 máximo 6
SLEEP = 1 # tiempo de espera entre peticiones en segundos
PATH = './csv/housing-barcelona.csv' # path donde guardaremos el csv resultante
WAIT_CAPTCHA = True # configuración si queremos esperar a resolver el Captcha inicial o no
```

Y, inicialmente, se pasan en la variable locations la lista de barrios que queremos scrapear:

```python
locations = ["/venta-viviendas/barcelona/nou-barris/mapa", "/venta-viviendas/barcelona/sant-andreu/mapa", "/venta-viviendas/barcelona/sant-marti/mapa"]
```
En nuestro caso Nous Barris, Sant Andreu i Sant Martí; el este de Barcelona.

## DOI de Zenodo del dataset generado

Dataset publicado en Zenodo: https://zenodo.org/record/6436017#.YlMK2tNBzIV

El DOI es el siguiente: https://doi.org/10.5281/zenodo.6436017

Aunque también se encuentra en este mismo repositorio, en csv/housing-barcelona.csv
