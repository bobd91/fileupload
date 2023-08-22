from flask import Flask, request, redirect, flash, render_template, Response
from io import TextIOWrapper

app = Flask(__name__)

app.secret_key = 'secret_key'

# Optional: limit size of uploaded file, example 1MB
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024

# Used in templates/fileupload.html to specify allowed file types
app.jinja_env.globals['ALLOW_FILETYPES'] = '.csv'

# The name of the downloaded file
# If this name should be computed based on uploaded filename
# then there is a bit more work to do
app.config['DOWNLOAD_FILENAME'] = 'transformed_data.csv'

# The HTML mime type of the downloaded data
app.config['DOWNLOAD_MIMETYPE'] = 'text/csv'

# Simple page just to link to file upload page
@app.route('/')
def index():
    return render_template('index.html')

# File upload processing
# HTML GET for the page where the user selects the file they want to upload
# HTML POST for the actual upload of the file data
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        # display the file upload page
        return render_template('fileupload.html')

    else:
        # Handle the uploaded file

        # Reject POST request without file
        if 'file' not in request.files:
            flash('No file')
            return redirect(request.url)

        # Transform the uploaded data
        data = transform(request.files['file'].stream)

        # None indicates failure to transform data
        if data is None:
            flash('Unable to transform file data')
            return redirect(request.url)

        # Return data to the user
        resp = Response(data, mimetype=app.config['DOWNLOAD_MIMETYPE'])
        resp.headers['Content-Disposition'] = \
                "attachment; filename=" + app.config['DOWNLOAD_FILENAME']
        return resp

def transform(stream):
    # Return the transformed data stream
    # Or None if the data is not what was expected

    # stream - a BytesIO stream

    # Example is CSV text data, we  append ',Bob' to each line 
    # To get the uploaded data as text we first wrap the BytesIO stream in a TextIOWrapper
    try:
        lines = TextIOWrapper(stream).read()
        data = ''
        for line in lines.splitlines():
            data += line + ",Bob\n"
        return data

    # If python throws any exceptions then return None
    except:
        return None

if __name__ == '__main__':
    app.run()

