import csv
import statistics
import matplotlib.pyplot as plt


informacion_nombre_altura = list( csv.reader( open('alturas.csv') ))

contenedor_alturas = [ informacion_nombre_altura[elemento][1] for elemento in range( len(informacion_nombre_altura)) ]

contenedor_alturas =  list( filter(None,contenedor_alturas))

alturas_numero = [float(contenedor_alturas[elemento]) for elemento in range( len( contenedor_alturas ) ) ]
alturas_numero.sort()

alturas_filtradas = [alturas_numero[elemento] for elemento in range(len(alturas_numero)) if alturas_numero[elemento] < 174]

print( statistics.mean(alturas_filtradas))

print(alturas_filtradas)

plt.boxplot(alturas_filtradas)


plt.plot(1,172, color = 'red', label = 'Persona 1', marker = 'o')
plt.plot(1,167, color = 'pink', label = 'Persona 2', marker = 'o')
plt.plot(1,163, color = 'purple', label = 'Persona 3', marker = 'o')
plt.plot(1,171, color = 'green', label = 'Persona 4', marker = 'o')
plt.plot(1,167, color = 'black', label = 'Persona 5', marker = 'o')
plt.plot(1,165, color = 'yellow', label = 'Persona 6', marker = 'o')

plt.ylabel("Altura en cm")
plt.title("Diagrama de caja y bigotes de la alturas")
 plt.legend()
plt.show()
