# capa de servicio/lógica de negocio

from django.shortcuts import redirect
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user
from ..transport import transport
def getAllImages(input=None):
    # obtiene un listado de datos "crudos" desde la API, usando a transport.py.
    json_collection = transport.getAllImages(input)
    

    # recorre cada dato crudo de la colección anterior, lo convierte en una Card y lo agrega a images.
    images = []
    for object in json_collection:
        card = translator.fromRequestIntoCard(object)
        images.append(card)
    
    # json_collection = AllImages()
    # for item in json_collection:
    #     images.append({
    #         'url': item.get('image'),
    #         'name': item.get('name'),
    #         'status': item.get('status'),
    #         'last_location': item.get('location',{}).get('name'),
    #         'first_seen': item.get('episode', {}) [0] if item.get('episode') else 'desconocido',
    #     })
    return images

# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    card = ''
    fav =  card # transformamos un request del template en una Card.
    fav.user = request.user # le asignamos el usuario correspondiente.

    return repositories.saveFavourite(fav) # lo guardamos en la base.

# usados desde el template 'favourites.html'
def getAllFavourites(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        user = get_user(request)

        favourite_list = repositories.getAllFavourites(user) # buscamos desde el repositories.py TODOS los favoritos del usuario (variable 'user').
        mapped_favourites = []

        for favourite in favourite_list:
            card = '' # transformamos cada favorito en una Card, y lo almacenamos en card.
            mapped_favourites.append(card)

        return mapped_favourites

def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.deleteFavourite(favId) # borramos un favorito por su ID.