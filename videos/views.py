from bson import ObjectId
from pyramid.httpexceptions import HTTPFound

from pyramid.view import view_config



@view_config(route_name='video', renderer="templates/video.jinja2")
def video_view(request):
    videos = request.db_Videos.video.find()
    return {
        'videos': videos,
    }


@view_config(route_name='delete', renderer="templates/video.jinja2")
def delete_video(request):
    request.db_Videos.video.delete_one({"_id": ObjectId(request.matchdict['video_id'])})

    return HTTPFound(request.route_path('video'))


@view_config(route_name='add_video', renderer="templates/add_video.jinja2")
def add_video(request):
    if request.method == "POST":

        request.db_Videos.video.insert_one(
            {"name": request.POST["name"], "theme": request.POST["theme"], "thumbs_up": 0, "thumbs_down": 0})
        return HTTPFound(request.route_path('video'))
    else:
        return {}


@view_config(route_name='thumbs_up', renderer="templates/video.jinja2")
def thumbs_up(request):
    request.db_Videos.video.update_one({"_id": ObjectId(request.matchdict['video_id'])}, {"$inc": {"thumbs_up": 1}})
    return HTTPFound(request.route_path('video'))


@view_config(route_name='thumbs_down', renderer="templates/video.jinja2")
def thumbs_down(request):
    request.db_Videos.video.update_one({"_id": ObjectId(request.matchdict['video_id'])}, {"$inc": {"thumbs_down": 1}})
    return HTTPFound(request.route_path('video'))


@view_config(route_name='list_themes', renderer="templates/list_themes.jinja2")
def list_themes(request):

    themes = request.db_Videos.video.aggregate(
        [
            {"$addFields": {
                "score": {"$subtract": ["$thumbs_up", {"$divide": ["$thumbs_down", 2]}]}
            }},
            {
                "$group": {
                    "_id": "$theme",
                    "sum": {"$sum": "$score"}},

            },
            {"$sort": {"sum": -1}},

        ])


    return {
        "themes": themes
    }
