# Proyecto Prueba Odoo 



## Descripción 

El módulo principal del proyecto es movie, el cual está diseñado para gestionar y sincronizar información de películas desde una fuente externa hacia Odoo. Este módulo no solo permite almacenar y visualizar datos de películas dentro del sistema, sino que también automatiza el proceso de actualización mediante tareas programadas y expone una API REST para obtener el top 10 de películas.



### Paso 1 

clonamos el proyecto y nos posicionamos en la rama develop

```bash

git clone https://github.com/staylomak/prueba-odoo.git

git checkout develop 

```

### Paso 2

Posicionados en la carpeta clonada ejecutar el comando docker, esto levantará el ambiente de odoo 17 y la BD.

```bash

docker-compose up --build

```

### Paso 3

una vez este corriendo el docker consultamos la ruta

```bash

http://localhost:8069

```



### Paso 4

Nos creamos una cuenta en la vista que nos presenta **odoo**



### Paso 5

Para esta prueba necesitamos setear ruta y apikey para nuestro cron, nos vamos a **setting** y buscamos **Activate the developer mode**, luego en la barra de navegación nos aparecerá un menú llamado **Technical** y ahí buscamos **System Parameters** 



```bash

movie_manager.api_url =  https://random-data-api.com/api/v3/projects/a2bebcc5-69e3-4b4e-b8c0-4a2f4306f0da

movie_manager.api_key =  ZN-BE0NeUFPRYdYrRZf7CQ

```



### Paso 6

Luego vamos al menú principal **apps** y activamos el módulo "Movie Manager" una vez que este activado por detrás corre un cron cada **1 minuto** que nos alimenta de películas la BD (title, ranking), se puede ver reflejado en el menú superior izquierdo donde dice **películas** o se puede ver en los **logs**, el comportamiento de este cron el cual puede crear, actualizar o mostrar si se presenta un error (path: "logs/odoo.log").



El log se vería así, donde se intenta resaltar con **MODELS.MOVIE.API:::** donde **MODELS** hace alusión al **folder** donde este se encuentra, **MOVIE** hace alusión a la **clase** y **API** hace alusión que el log pertenece a las **api** (si en un futuro existieran muchas apis se tendría que ser aun más específico )



```bash

2025-04-25 18:51:57,057 1 INFO prueba odoo.addons.base.models.ir_cron: Starting job `Fetch Movies from API`. 

2025-04-25 18:51:57,060 1 INFO prueba odoo.addons.movie_manager.models.movie: MODELS.MOVIE.API::: Consultando API externa... 

2025-04-25 18:51:57,691 1 INFO prueba odoo.addons.movie_manager.models.movie: MODELS.MOVIE.API::: Película 'Dr. Demon' creada con ranking 3 

2025-04-25 18:51:57,691 1 INFO prueba odoo.addons.base.models.ir_cron: Job done: `Fetch Movies from API` (0.633s). 

```

### Paso 7
Prueba del REST el cual obtiene el top 10 de las peliculas con ranking de mayor a menor 
```bash
type GET
http://localhost:8069/api/top_movies

```
