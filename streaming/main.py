from flask import Flask, stream_with_context, request, Response, redirect,render_template
import time
app = Flask(__name__)

@app.route('/stream')
def streamed_response():
    def generate():
        for s in request.args['name']:
            time.sleep(0.5)
            yield s
    return Response(stream_with_context(generate()))

if __name__ == '__main__':
    app.debug = True
    app.run()
