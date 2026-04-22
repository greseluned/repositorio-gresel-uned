# Repositorio digital de prensa histórica (GRESEL-UNED)

Este repositorio implementa una colección digital de prensa histórica construida a partir de la plantilla CollectionBuilder-CSV y desplegada mediante GitHub Actions.

El proyecto integra imágenes digitalizadas de periódicos con sus transcripciones generadas mediante OCR, permitiendo una exploración interactiva del contenido.

---

## Visualización e interacción

A diferencia de la configuración original de CollectionBuilder, que utiliza Universal Viewer, en este repositorio se ha optado por utilizar OpenSeadragon como visor principal.

OpenSeadragon permite:
- Visualización de imágenes en alta resolución (zoom y desplazamiento)
- Superposición de regiones (artículos) sobre las páginas
- Conexión directa entre cada región y su transcripción

Las regiones han sido previamente anotadas en Transkribus mediante coordenadas.

---

## Procesamiento de datos

Los datos originales proceden de Transkribus en formato XML.

Para su integración en la web:
- Los archivos XML se transforman en JSON mediante scripts en Python
- Los JSON contienen las coordenadas de las regiones y sus transcripciones
- Se generan archivos de texto (TXT) para permitir la búsqueda en el contenido

El texto es procesado para reconstruir palabras y párrafos afectados por el formato en columnas de los periódicos.

---

## Estructura del repositorio

Los datos se organizan en la carpeta `/newspapers/`:

- Cada carpeta corresponde a una cabecera (por ejemplo, *Fémina*, *La Vanguardia*)
- Las subcarpetas corresponden a fechas de publicación
- Cada una contiene:
  - Archivos XML (uno por página)
  - Imágenes asociadas
  - Archivos JSON generados
  - Archivos TXT para búsqueda

Los archivos XML e imágenes deben estar emparejados para garantizar el correcto funcionamiento del visor.

---

## Metadatos

La colección se gestiona mediante un archivo `metadata.csv`, que incluye:

- Título del periódico  
- Fecha de publicación  
- Lugar  
- Ruta al archivo JSON (para la visualización)  
- Ruta a la imagen de portada (thumbnail)  
- Ruta al archivo de texto (para búsqueda)  

---

## Búsqueda

El repositorio permite buscar no solo en los metadatos, sino también en el contenido de las transcripciones.

Esto se consigue mediante:
- Extracción y limpieza del texto
- Generación de archivos TXT
- Indexación del contenido para su consulta desde la interfaz

---

## CollectionBuilder

<https://collectionbuilder.github.io/>

CollectionBuilder es un framework open source desarrollado por la University of Idaho Library para la creación de colecciones digitales mediante tecnologías web estáticas.

---

## Licencia

La documentación y contenido web general de CollectionBuilder está licenciada bajo [Creative Commons Attribution-ShareAlike 4.0 International](http://creativecommons.org/licenses/by-sa/4.0/). 

El código de CollectionBuilder está licenciado bajo [MIT](https://github.com/CollectionBuilder/collectionbuilder-csv/blob/master/LICENSE).

Los datos (imágenes, transcripciones, etc.) pueden estar sujetos a licencias específicas indicadas en sus metadatos.

---

## Referencias

Gilman, I., Kishore, A., Thatcher, C., Salsbery, M., Vandecreme, A., Pearce, T., & Horák, J. (2026). OpenSeadragon (Version 6.0.2) [Computer software]. <https://github.com/openseadragon/openseadragon>

Williamson, E. P., Becker, D., & Wikle, O. (2021). CollectionBuilder-CSV (Version 1+) [Computer software]. <https://github.com/CollectionBuilder/collectionbuilder-csv>