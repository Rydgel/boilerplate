from flask import jsonify


def global_handlers(app):
    @app.errorhandler(404)
    def page_not_found(_):
        return jsonify({'error': True, 'msg': '404'}), 404
    # todo other kinds of errors
