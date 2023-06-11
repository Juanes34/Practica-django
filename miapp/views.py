from django.shortcuts import render,HttpResponse,redirect
from miapp.models import Article
from django.db.models import Q
from miapp.forms import FormArticle
from django.contrib import messages
# Create your views here.
# MVC = Modelo Vista Controlador -> acciones (metodos)
# MVT = Modelo Template Vista -> acciones (metodos)

layout = """
<h1>Sitio web con django</h1>
<hr>
<ul>
    <li><a href="/">Inicio</a></li>
    <li><a href="/holamundo">Hola Mundo</a></li>
    <li><a href="/pagina-pruebas">Pagina pruebas</a></li>
    <li><a href="/contacto">Contacto</a></li>
</ul>
<hr>
"""

def index(request):
    """
    html = ""
        <h1>Inicio</h1>
        <p>Años hasta el 2050</p>
        <ul>
    ""
    year = 2023
    while year <=2050:
        if year%2 ==0:
            html += f"<li>{str(year)}</li>"
        year += 1
    html +="</ul>"
    """
    year = 2023
    hasta = range(year,2051)
    nombre = 'Juanes'
    lenguajes = ['Javascript','Python','PHP','C']

    return render(request,'index.html',{
        'title':'Inicio',
        'mi_variable':'Soy un dato',
        'nombre':nombre,
        'lenguajes':lenguajes,
        'years':hasta,
    })

def holamundo(request):
    return render(request,'hola_mundo.html')

def pagina(request,redirigir=0):
    if redirigir==1:
        return redirect('Contacto',nombre = "Juan")
    return render(request,'pagina.html',{
        'texto':'Este es mi texto',
        'lista':['uno','dos','tres'],
    })

def contacto(request,nombre="",apellidos=""):
    html =""
    if nombre and apellidos:
        html = f"<h3>{nombre} {apellidos}</h3>"
    return HttpResponse(layout+f"""
        <h1>Contacto</h1>
    """+html)

def crear_articulo(request,title,content,public):
    articulo = Article(
        title = title,
        content = content,
        public = public,
    )

    articulo.save()

    return HttpResponse(f'Articulo Creado: {articulo.title} - {articulo.content}')

def save_articulo(request):
    if request.method=='POST':
        title = request.POST['title']

        if len(title)<=5:
            return HttpResponse("<h2>El titulo es muy pequeño</h2>")
        content = request.POST['content']
        public = request.POST['public']

        articulo = Article(
            title = title,
            content = content,
            public = public,
        )

        articulo.save()
        return HttpResponse(f'Articulo Creado: {articulo.title} - {articulo.content}')
    else:
        return HttpResponse("<h2>No se ha podido crear</h2>")
    
    
def create_article(request):

    return render(request,'create_article.html')

def create_full_article(request):
    if request.method == 'POST':
        formulario = FormArticle(request.POST)
        if formulario.is_valid():
            data_form = formulario.cleaned_data

            title = data_form.get('title')
            content = data_form['content']
            public = data_form['public']

            articulo = Article(
                title = title,
                content = content,
                public = public,
            )

            articulo.save()

            # crear mensaje flash(sesion que solo se muestra una vez)
            messages.success(request,f'Has creado correctamente el articulo {articulo.id}')

            return redirect('articulos')
            #return HttpResponse(articulo.title+' - '+articulo.content+' - '+str(articulo.public))
    else:
        formulario = FormArticle()

    return render(request,'create_full_article.html',{
        'form':formulario
        })
def articulo(request):
    articulo = Article.objects.get(title='tercer articulo')
    return HttpResponse(f"Articulo:<br> {articulo.id} {articulo.title}")

def editar_articulo(request,id):
    articulo = Article.objects.get(id=id)
    articulo.title = "Batman"
    articulo.content = "Pelicula del 2017"
    articulo.public = True
    articulo.save()
    return HttpResponse(f'Articulo editado: {articulo.title} - {articulo.content}')

def articulos(request):
    articulos = Article.objects.filter(public=True).order_by('id')
    #articulos = Article.objects.order_by('title')[1:3]

    #articulos = Article.objects.filter(title="Batman",id=1)
    #articulos = Article.objects.filter(title__contains="articulo")
    #articulos = Article.objects.filter(title__exact="Batman")
    #articulos = Article.objects.filter(title__iexact="Batman")

    #articulos = Article.objects.filter(public=True).exclude(title__contains='articulo')


    #articulos = Article.objects.raw("SELECT * FROM miapp_article WHERE title='articulo' and public=True")

    """articulos = Article.objects.filter(
                                        Q(title__contains='rt') | Q(title__contains='la')
                                        )"""
    return render(request,'articulos.html',{
        'articulos':articulos,
    })

def borrar_articulos(request,id):
    articulo = Article.objects.get(id=id)
    articulo.delete()
    return redirect('articulos')