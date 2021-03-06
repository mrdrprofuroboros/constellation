from flask import Flask, jsonify
from flask_cors import CORS
from flask_graphql import GraphQLView

from source import settings, schemas


app = Flask(__name__)
CORS(app)

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schemas.schema, graphiql=True))

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'message': 'The requested URL was not found on the server.'}), 404


if __name__ == '__main__':
    app.run(
        host=settings.BIND_HOST,
        port=settings.BIND_PORT,
        debug=settings.DEBUG,
    )
