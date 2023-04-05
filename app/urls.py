from . import app, db
from . import views

app.add_url_rule('/', view_func=views.index)
app.add_url_rule('/movie/<int:movie_id>', view_func=views.movie_detail)
app.add_url_rule('/search', view_func=views.movie_search)

app.add_url_rule('/admin/category/create', view_func=views.admin_category_create, methods=['POST', 'GET'])
app.add_url_rule('/admin/movie/create', view_func=views.admin_movie_create, methods=['POST', 'GET'])

app.add_url_rule('/admin/movie/list', view_func=views.admin_movie_list)
app.add_url_rule('/admin/category/list', view_func=views.admin_category_list)

app.add_url_rule('/admin/movie/<int:movie_id>/update', view_func=views.admin_movie_update, methods=['POST', 'GET'])
app.add_url_rule('/admin/category/<int:category_id>/update', view_func=views.admin_category_update, methods=['POST', 'GET'])

app.add_url_rule('/admin/movie/<int:movie_id>/delete', view_func=views.admin_movie_delete, methods=['POST', 'GET'])
app.add_url_rule('/admin/category/<int:category_id>/delete', view_func=views.admin_category_delete, methods=['POST', 'GET'])


app.add_url_rule('/account/register', view_func=views.user_register, methods=['POST', 'GET'])
app.add_url_rule('/account/login', view_func=views.user_login, methods=['POST', 'GET'])
app.add_url_rule('/account/logout', view_func=views.user_logout)
