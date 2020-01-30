from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('video', '/')
    config.add_route('delete', '/delete/{video_id}')
    config.add_route('add_video', '/add_video')
    config.add_route('list_themes', '/list_themes')
    config.add_route('thumbs_up', '/thumbs_up/{video_id}')
    config.add_route('thumbs_down', '/thumbs_down/{video_id}')
    config.scan()
    return config.make_wsgi_app()
