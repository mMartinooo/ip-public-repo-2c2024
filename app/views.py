# capa de vista/presentación

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from app.layers.persistence import repositories
from app.layers.utilities import translator
from app.models import Favourite
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados que corresponden a las imágenes de la API y los favoritos del usuario, y los usa para dibujar el correspondiente template.
# si el opcional de favoritos no está desarrollado, devuelve un listado vacío.
def home(request):
    images = services.getAllImages()
    favourite_list = services.getAllFavourites(request)

    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })

def search(request):
    search_msg = request.POST.get('query', '')

    # si el texto ingresado no es vacío, trae las imágenes y favoritos desde services.py,
    # y luego renderiza el template (similar a home).
    if (search_msg != ''):
        images = services.getAllImages(search_msg)
        favourite_list = services.getAllFavourites(request)

        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    else:
        return redirect('home')


# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    favourite_list = repositories.getAllFavourites(request.user)
    return render(request, 'favourites.html', { 'favourite_list': favourite_list })

@login_required
def saveFavourite(request):
    if request.method == 'POST':
        try:
            fav = translator.fromTemplateIntoCard(request)  # Se transforma el request en una "Card".
            fav.user = request.user  # Asignamos el usuario correspondiente.

            # Guardamos el favorito
            repositories.saveFavourite(fav)

            # Redirigimos a la página de favoritos después de guardar
            return redirect('favoritos')  # 'favourites' es el nombre de la URL donde deseas redirigir al usuario

        except Exception as e:
            # Si hay un error, puedes manejarlo y devolver una respuesta adecuada
            return HttpResponse(f"Error al guardar el favorito: {str(e)}", status=500)

    else:
        # Si no es un POST, puedes devolver una respuesta adecuada
        return HttpResponse("Método no permitido", status=405)

@login_required
def deleteFavourite(request):
    if request.method == 'POST':
        # Obtener el ID del favorito a eliminar desde el formulario
        fav_id = request.POST.get('id')

        # Verificar que el ID sea válido
        if fav_id:
            # Obtener el favorito correspondiente al ID (si no existe, devolver 404)
            favourite = get_object_or_404(Favourite, id=fav_id, user=request.user)

            # Eliminar el favorito
            favourite.delete()

            # Redirigir a la página de favoritos
            return redirect('favoritos')  # Asegúrate de que la URL 'favourites' esté definida

        return HttpResponse("No se pudo eliminar el favorito.", status=400)

    return HttpResponse("Método no permitido.", status=405)

@login_required
def exit(request):
    return redirect('logout')