from pyramid.view import view_config
from pyramid.response import Response
from pyramid.renderers import render_to_response
from sqlalchemy import func
from .. send_email import send_email


from sqlalchemy.exc import DBAPIError

from .. import models


@view_config(route_name='home', renderer='../templates/mytemplate.jinja2')
def my_view(request):
    try:
        query = request.dbsession.query(models.Height)
        one = query.filter(models.Height.email == 'one').first()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'one': one, 'project': 'collect_height'}

@view_config(route_name='success', renderer='../templates/success.jinja2')
def success(request):
    if request.method == 'POST':
        new_email = request.POST['email_name']
        new_height = request.POST['height_name']

        if request.dbsession.query(models.Height).filter(models.Height.email == new_email).count() == 0:
            new_model = models.Height(email = new_email, height = new_height)
            request.dbsession.add(new_model)
            average_height = request.dbsession.query(func.avg(models.Height.height)).scalar()
            average_height = round(average_height, 1)
            count = request.dbsession.query(models.Height).count()
            send_email(new_email, new_height, average_height, count)

        else:
            return render_to_response('../templates/duplicate.jinja2', {}, request=request)

    return {}

db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to initialize your database tables with `alembic`.
    Check your README.txt for descriptions and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
