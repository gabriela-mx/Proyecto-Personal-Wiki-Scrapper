import urllib.request as urllib
import json
import csv

# Uds de personas

id_yuju = 426398
id_eunha = 426397
id_binnie = 446175
id_seolhyun = 178314
id_xiao = 494132
id_hani = 124396
id_sowon = 426395

def DecodificadorWeb(direccion_web):
	respuesta = urllib.urlopen(direccion_web)
	return json.loads(respuesta.read().decode('utf8'))

def indice_subcadena(lista_donde_buscar, subcadena):

    for i, cadena in enumerate(lista_donde_buscar):
        if subcadena in cadena:
              return i
    return None


def Encuentra_Indice_Altura(Diccionarios_Anidados_En_Lista):

	indice_elemento_altura = 0

	for elemento in range(len(Diccionarios_Anidados_En_Lista)):
		diccionario_actual= Diccionarios_Anidados_En_Lista[elemento]

		try:
			diccionarios_varios = list(diccionario_actual.values())
			#print(diccionarios_varios)
			posicion_lista = indice_subcadena(diccionarios_varios,'Estatura:')
			if posicion_lista is not None:
				indice_elemento_altura = elemento

		except ValueError:
			valor = None

		try:
			diccionarios_varios = list(diccionario_actual.values())
			#print(diccionarios_varios)
			posicion_lista = indice_subcadena(diccionarios_varios,'Height:')
			if posicion_lista is not None:
				indice_elemento_altura = elemento

		except ValueError:
			valor = None

		try:
			diccionarios_varios = list(diccionario_actual.values())
			#print(diccionarios_varios)
			posicion_lista = indice_subcadena(diccionarios_varios,'Altura:')
			if posicion_lista is not None:
				indice_elemento_altura = elemento

		except ValueError:
			valor = None

	if indice_elemento_altura == 0:
		return None

	return indice_elemento_altura

def Formatear_Nombre(nombre_bruto):
	nombre_formato = (nombre_bruto.replace('Name: ','').replace('Nombre: ','')).replace('Nombre','').replace('completo','').replace('real','').replace('artistico','').replace('artístico','').replace('Artístico','').replace('\xa0','').replace(' Real','').replace(' : ','').replace(':','')
	return nombre_formato

def Formatear_Altura(altura_bruto):
	try:
		altura_formato = (altura_bruto.replace('Estatura','' ).replace('Height','').replace('Altura','').replace(':','').replace('cms','').replace('\xa0','') ).replace('cm','').replace(' .','').replace(',','.')

		if altura_formato.endswith('.'):
			altura_formato=altura_formato[:-1]

		if altura_formato.startswith(' '):
			altura_formato=altura_formato[1:]


		if altura_formato == '':
			return

		altura_formato = float (altura_formato)
		if altura_formato%100 < 10:
			altura_formato = 100 * altura_formato
		return altura_formato
	except ValueError:
		return None

def AdquiereNombreYAltura(numero_identificador):

	numero_identificador = str(numero_identificador)
	direccion_web = "http://es.drama.wikia.com/api/v1/Articles/AsSimpleJson?id="+numero_identificador
	informacion_wiki = DecodificadorWeb(direccion_web)

	try:
		Diccionarios_Anidados_En_Lista = informacion_wiki['sections'][1] ["content"][0]["elements"]
	except KeyError:
		return [None, None]
	except IndexError:
		return [None, None]
	indice_elemento_altura = Encuentra_Indice_Altura(Diccionarios_Anidados_En_Lista)


	if indice_elemento_altura is not None:
		Altura = Formatear_Altura( informacion_wiki['sections'][1] ["content"][0]["elements"][indice_elemento_altura]['text'] )
	else:
		Altura = None

	try:		
		Nombre = Formatear_Nombre( informacion_wiki['sections'][1] ["content"][0]["elements"][0]['text'] )
	except KeyError:
		return [None, None]
	except IndexError:
		return [None, None]
	return [Nombre, Altura]



lote = 1
identificadores =[]

for k in range(7):
	direccion_consulta = "http://es.drama.wikia.com/api/v1/Search/List?query=Categor%C3%ADa%3AKBailarina&limit=99&minArticleQuality=60&batch="+str(lote)+"&namespaces=0%2C14"
	grupo_kbailarinas = DecodificadorWeb(direccion_consulta)
	identifcadores_actual = [ grupo_kbailarinas["items"][elemento]["id"] for elemento in range( len( grupo_kbailarinas["items"])) ]
	identificadores +=   identifcadores_actual
	lote += 1


Para_Exportar = [ AdquiereNombreYAltura( identificadores[elemento]) for elemento in range( len( identificadores)) ]

with open("alturas.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(Para_Exportar)