# Cifrado César - Análisis de Algoritmos

El propósito de nuestro proyecto es lograr descifrar mensajes codificados con el método de Cifrado César, probando y ejecutando diferentes algoritmos para comprobar sus rendimientos y efectividad.

Se utiliza una interfaz gráfica sencilla para una mejor comprensión visual de la ejecución y comparativa entre los diferentes algoritmos ejecutados.

## Descripción

El Cifrado César es una técnica de cifrado simple y rápida, se basa en la sustitución de cada letra de un texto original por otra letra que se encuentra en un número fijo de posiciones más adelante en el alfabeto.

Es un método fácil de implementar y ideal para introducir conceptos básicos de criptografía. Sin embargo, este método es fácil de descifrar y carece de seguridad, por lo que es muy venerable y se considera obsoleto para aplicaciones prácticas en la actualidad.
## Requisitos

Versión de Python:
- `Python 3.10+`

Librerias:
- `matplotlib` (pip install matplotlib)
- `tkinter` (Viene incluido con Python)
- `collections` (Incluido en Python)
- `time` (Incluido en Python)
- `tracemalloc` (Incluido en Python)

> [!WARNING]
> La ausencia de cualquier requisito puede generar errores en la ejecución o directamente no ejecutar el programa del proyecto.

## Algoritmos Implementados

1. Fuerza bruta - Prueba todos los desplazamientos posibles
2. Divide y Vencerás - Analiza por partes para optimizar la búsqueda
3. Algoritmo Voraz - Utiliza análisis de frecuencia de letras
4. Branch & Bound - Filtra soluciones no prometedoras

## Instrucciones de Ejecución

Ejecutar el arcchivo `proyecto_cesar.py` ubicado en la carpeta `src/`:
```
python src/proyecto_cesar.py
```

> [!IMPORTANT]
> Verificar tener instalado todos los requisitos necesarios antes de su ejecución.
