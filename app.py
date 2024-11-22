from flask import Flask, render_template, request, redirect, flash, url_for
import boto3
from botocore.exceptions import NoCredentialsError

app = Flask(__name__)
app.secret_key = ''  # For flash messages

# AWS S3 Configuration
BUCKET_NAME = 'my-file-storage-bucket-vedant'
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
REGION_NAME = 'us-east-1'

# Initialize the S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME
)

@app.route('/')
def index():
    # List all files in the S3 bucket
    try:
        files = s3.list_objects_v2(Bucket=BUCKET_NAME).get('Contents', [])
    except NoCredentialsError:
        flash("Credentials not available", "error")
        return redirect(url_for('index'))
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        flash('No file part', 'error')
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(url_for('index'))
    try:
        s3.upload_fileobj(file, BUCKET_NAME, file.filename)
        flash('File uploaded successfully', 'success')
    except NoCredentialsError:
        flash("Credentials not available", "error")
    return redirect(url_for('index'))

@app.route('/download/<filename>')
def download(filename):
    try:
        # Generate the presigned URL for download
        file_url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': filename},
            ExpiresIn=3600
        )
    except NoCredentialsError:
        flash("Credentials not available", "error")
        return redirect(url_for('index'))
    return redirect(file_url)

@app.route('/delete/<filename>')
def delete(filename):
    try:
        s3.delete_object(Bucket=BUCKET_NAME, Key=filename)
        flash('File deleted successfully', 'success')
    except NoCredentialsError:
        flash("Credentials not available", "error")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
