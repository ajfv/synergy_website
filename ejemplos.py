"""
Este script crea sitios de prueba y los agrega a la aplicación para que pueda
probar el buscador. También puede regresar la base de datos a su estado anterior.
"""
from base import db, Sitio, Hilo, Publicacion
import sys

def mostrar_uso():
    "Ayuda de la herramienta"
    mensaje = (
        "Uso: python ejemplos.py opcion \n"
        "Descripción: Agrega y elimina páginas de prueba de la aplicación.\n"
        "Opciones:\n"
        "--crear : Agrega las páginas.\n"
        "--eliminar Elimina las páginas."
    )
    print(mensaje)
    
def crear_paginas():
    "Crea tres páginas de muestra."
    
    s1 = Sitio("usb","Universidad Simon Bolivar")
    s2 = Sitio("perros","Perros")
    s3 = Sitio("futbol","Futbol")

    s1.contenido = "La Universidad Simon Bolivar (USB por sus iniciales), es una universidad publica Venezolana creada en 1967. Con un fuerte enfasis en la investigacion cientifica y tecnologica, es una de las mas importantes y prestigiosas del pais. Inicio sus actividades academicas en 1970 en el Valle de Sartenejas en Caracas y siete anhos mas tarde en el Valle de Camuri Grande en Vargas. Cuenta actualmente con estas dos sedes. Su rectorado esta en la sede de Sartenejas, ubicada en el Municipio Baruta del estado Miranda. La USB ha graduado aproximadamente 25.000 Ingenieros, Arquitectos, Urbanistas y Licenciados. Ademas se han graduado 7.232 estudiantes con el titulo de Tecnico Superior Universitario (TSU) en las distintas modalidades dictadas en la sede del litoral. Junto con 5.000 especialistas, magister y doctores. Segun un estudio realizado a nivel de America Latina por el QS World University Rankings para el anho 2015, la USB se encuentra en el puesto numero 2 a nivel nacional, mientras que ocupa el puesto numero 34 en America Latina.6"
    s1.imagenes = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/USB_logo.svg/250px-USB_logo.svg.png"
    s2.contenido = "El perro o perro domestico (Canis lupus familiaris)1 2 3 4 o tambien llamado can es un mamifero carnivoro de la familia de los canidos, que constituye una subespecie del lobo (Canis lupus). Un estudio publicado por la revista Nature revela que, gracias al proceso de domesticacion, el organismo del perro se ha adaptado6 a cierta clase de alimentos, en este caso el almidon.7 Su tamanho o talla, su forma y pelaje es muy diverso segun la raza. Posee un oido y olfato muy desarrollados, siendo este ultimo su principal organo sensorial. En las razas pequenhas puede alcanzar una longevidad de cerca de 20 anhos, con atencion esmerada por parte del propietario, de otra forma su vida en promedio es alrededor de los 15 anhos. \n\nSe cree que el lobo gris, del que es considerado una subespecie, es el antepasado mas inmediato. Las pruebas arqueologicas demuestran que el perro ha estado en convivencia cercana con los humanos desde hace al menos 9000 anhos, pero posiblemente desde hace 14 000 anhos. Las pruebas fosiles demuestran que los antepasados de los perros modernos ya estaban asociados con los humanos hace 100 000 anhos. Las investigaciones mas recientes indican que el perro fue domesticado por primera vez en el este de Asia, posiblemente en China. "
    s2.imagenes = "https://i.ytimg.com/vi/VPD8W53SxD4/hqdefault.jpg"
    s3.contenido = "El futbol o futbol2 (del ingles britanico football), tambien conocido como balompie, es un deporte de equipo jugado entre dos conjuntos de once jugadores cada uno "

    db.session.add(s1)
    db.session.add(s2)
    db.session.add(s3)
    db.session.commit()

    h1 = Hilo(sitio=s1)
    h2 = Hilo(sitio=s2)
    h3 = Hilo(sitio=s3)
    db.session.add(h1)
    db.session.add(h2)
    db.session.add(h3)
    db.session.commit()

    p1 = Publicacion(s1.titulo, s1.titulo, hilo=h1)
    p2 = Publicacion(s2.titulo, s2.titulo, hilo=h2)
    p3 = Publicacion(s3.titulo, s3.titulo, hilo=h3)
    db.session.add(p1)
    db.session.add(p2)
    db.session.add(p3)
    db.session.commit()
    print("Se agregaron tres páginas de ejemplo a la aplicación.")

def eliminar_pagina(id_pagina):
    "Elimina la página con el título especificado."
    pag = Sitio.query.filter_by(id=id_pagina).first()
    if pag is None:
        return False
    hilo = pag.hilo
    for pub in hilo.publicaciones:
        db.session.delete(pub)
    db.session.commit()
    db.session.delete(hilo)
    db.session.commit()
    db.session.delete(pag)
    db.session.commit()
    return True
    
def eliminar_paginas():
    "Regresa la base de datos a su estado anterior."
    paginas = ["usb", "perros", "futbol"]
    resultados = [eliminar_pagina(id_pagina) for id_pagina in paginas]
    for i in range(3):
        if not resultados[i]:
            print('La página con id "%s" no pudo hallarse en la base de datos.'%paginas[i])
    if all(resultados):
        print("Las tres páginas de prueba se borraron exitosamente.")
        
if __name__ == '__main__':
    if len(sys.argv) != 2 or sys.argv[1] not in ['--crear', '--eliminar']:
        mostrar_uso()
    elif sys.argv[1] == '--crear':
        crear_paginas()
    else:
        eliminar_paginas()
