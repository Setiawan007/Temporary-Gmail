from flask import Flask, jsonify, redirect, url_for
from flask_limiter.util import get_remote_address
from flask_limiter import Limiter
from dotenv import dotenv_values
from Helpers import Email as EmailHelper

config = dotenv_values(".env")

app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["5000 per day", "50 per minute"],
    storage_uri="memory://",
)

mailbox = EmailHelper.Email()
mailbox.Login()


def index_error_responder(request_limit):
    return jsonify(
        {
            "status": "error",
            "message": "You have reached the request limit of {} requests per day".format(
                request_limit.limit
            ),
        }
    )


@app.route('/read/<email>', methods=['GET'])
@limiter.limit("20/minute", on_breach=index_error_responder)
def get_message(email):
    return jsonify(mailbox.GetMessages(email))


@app.route('/delete/<uid>', methods=['GET'])
def delete_message(uid):
    return jsonify(mailbox.delete_message(uid))


@app.route('/readby/<email>/<string_data>', methods=['GET'])
@limiter.limit("20/minute", on_breach=index_error_responder)
def read_by(email, string_data):
    if string_data is None:
        return jsonify(
            {
                'status': False,
                'message': 'Data Search is empty'
            }
        )
    else:
        return jsonify(mailbox.read_by(string_data, email))


@app.route('/', methods=['GET'])
def index():
    return jsonify(
        {
            'status': True,
            'message': 'Welcome to API'
        }
    )


@app.route('/generate/<type>', methods=['GET'])
def generate_email(type):
    # Gmail Dot Trick Refrence
    #
    # https://codegolf.stackexchange.com/questions/204473/generate-gmail-dot-aliases

    return jsonify(
        {
            'status': True,
            'message': 'Success',
            'data': mailbox.generate_email(type)
        }
    )


@app.errorhandler(404)
def not_found(error):
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        threaded=True,
    )
