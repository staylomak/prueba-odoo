from odoo import http
from odoo.http import request, Response
import json
import logging

_logger = logging.getLogger(__name__)

class MovieAPIController(http.Controller):

    @http.route('/api/top_movies', type='http', auth='public', methods=['GET'], cors='*')
    def get_top_ten_movies(self, limit=10, **kw):
        try:
            level_code = "CONTROLLER.MOVIE_API_CONTROLLER:::"
            _logger.info(f"{level_code} Solicitud recibida para top películas. Limit: {limit}")
            
            # Convert limit to int and validate
            try:
                limit = int(limit)
                if limit <= 0 or limit > 100:
                    limit = 10
            except (ValueError, TypeError):
                limit = 10

            # Search movie with ranking order and limit
            movies = request.env['movie.movie'].sudo().search(
                [], 
                order='ranking DESC', 
                limit=limit
            )

            if not movies:
                _logger.info(f"{level_code} No se encontraron películas")
                return Response(
                    json.dumps({
                        'status': 'success',
                        'message': 'No se encontraron películas',
                        'data': []
                    }),
                    content_type='application/json',
                    status=200
                )
            
            movies_data  = movies.read(['id', 'title', 'ranking'])
            
            return Response(
                json.dumps({
                    'status': 'success',
                    'count': len(movies_data),
                    'data': movies_data
                }),
                content_type='application/json',
                status=200
            )
        except Exception as e:
            _logger.exception(f"{level_code} Error al procesar solicitud: {e}")
            return Response(
                json.dumps({
                    'status': 'error',
                    'message': 'Internal server error'
                }),
                content_type='application/json',
                status=500
            )
