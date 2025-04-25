import requests
import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class Movie(models.Model):
    _name = 'movie.movie'
    _description = 'Movie'
    _rec_name = 'title'
    _order = 'ranking desc'

    title = fields.Char(string='Título de la Película', required=True, index=True)
    ranking = fields.Integer(string='Ranking', required=True)
    last_update = fields.Datetime(string='Última Actualización', readonly=True)
    
    _sql_constraints = [
        ('title_uniq', 'unique(title)', 'El título de la película debe ser único!')
    ]

    @api.model
    def fetch_movies_from_api(self):
        level_code = "MODELS.MOVIE.API:::"
        # Configuration parameters
        config = self.env['ir.config_parameter'].sudo()
        api_url = config.get_param('movie_manager.api_url')
        api_key = config.get_param('movie_manager.api_key')

        if not api_url or not api_key:
            _logger.error(f"{level_code} API URL o Key no configurados")
            return False

        try:
            _logger.info(f"{level_code} Consultando API externa...")

            response = requests.get(f"{api_url}?api_key={api_key}", timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                # Validate that the required fields are in the response
                if 'movie_title' in data and 'ranking_movie' in data:
                    title = data['movie_title']
                    ranking = int(data['ranking_movie'])
                    
                    # Search for existing movie or create a new one
                    movie = self.search([('title', '=', title)], limit=1)
                    
                    # Update or create the movie record
                    if movie:
                        movie.write({
                            'ranking': ranking,
                            'last_update': fields.Datetime.now()
                        })
                        _logger.info(f"{level_code} Película '{title}' actualizada con ranking {ranking}")
                    else:
                        self.create({
                            'title': title,
                            'ranking': ranking,
                            'last_update': fields.Datetime.now()
                        })
                        _logger.info(f"{level_code} Película '{title}' creada con ranking {ranking}")
                    
                    return True
                else:
                    missing_fields = []
                    if 'movie_title' not in data:
                        missing_fields.append('movie_title')
                    if 'ranking_movie' not in data:
                        missing_fields.append('ranking_movie')
                    
                    _logger.warning(f"{level_code} Datos incompletos recibidos. Campos faltantes: {', '.join(missing_fields)}")
                    _logger.warning(f"{level_code} Respuesta recibida: {data}")
                    return False
            else:
                _logger.error(f"{level_code} Error en respuesta API: {response.status_code} - {response.text}")
                return False
        except requests.exceptions.Timeout:
            _logger.error(f"{level_code} Timeout al consultar la API externa (después de 10 segundos)")
            return False
        except requests.exceptions.ConnectionError:
            _logger.error(f"{level_code} Error de conexión al consultar la API externa")
            return False
        except Exception as e:
            _logger.exception(f"{level_code} Error inesperado al consultar API externa: {e}")
            return False