# Challenge Tecnico TSS

Bot trading implementado con la biblioteca Backtrader, donde se centra en la evaluación de señales basadas en el cruce de medias móviles simples para ejecutar órdenes de compra y venta.

## Indice

1. [Estructura del proyecto](#Estructura-del-proyecto)
2. [Dependencias](#Dependencias)
3. [Ejecutar bot](#Ejecutar-bot)
4. [Output](#Output)

## Estructura del proyecto

La estructura general del proyecto es la siguiente:

```
challenge-tecnico-TSS
|-- datafeeds
    |-- AAPL.csv
    |-- GOOG.csv
    |-- MSFT.csv
    |-- TSLA.csv
|-- logs
    |-- log_strategy.py
|-- strategies
    |-- base_strategy.py
    |-- cross_method.py
    |-- golden_death_cross.py
main.py
README.md
```

## Dependencias

Se debe contar con una version de python superior o igual a la 3.2. Luego debe ejecutar el siguiente comando para instalar backtrader

```bash
pip install backtrader[plotting]
```

## Ejecutar bot

Para correr el bot se debe correr el archivo `main.py`

```bash
python main.py
```

## Output

La salida del bot se almacena en el archivo `logs/app.log`. Alli se muestran las ordenes completadas, los trades cerrados, las variaciones en el valor del portfolio y su valor inicial y final. 
