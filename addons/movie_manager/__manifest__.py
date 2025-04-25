{
    'name': 'Movie Manager',
    'version': '1.0',
    'summary': 'Gestión de películas desde API externa',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/movie_views.xml',
        'data/cron.xml'
    ],
    'installable': True,
    'application': True,
}