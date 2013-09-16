import sys
import optparse
import ConfigParser
import os
import cooperhewitt.api.client
import json
import urllib
import csv
import zipfile
import datetime
import boto
from boto.s3.key import Key
import sendgrid


s3_key = os.environ['S3_KEY']
s3_secret = os.environ['S3_SECRET']
s3_bucket = os.environ['S3_BUCKET']
access_token = os.environ['CH_API_KEY']
hostname = os.environ['CH_API_HOST']

sendgrid_username = os.environ['SENDGRID_USERNAME']
sendgrid_password = os.environ['SENDGRID_PASSWORD']

if __name__ == '__main__':
	
	parser = optparse.OptionParser()
	parser.add_option('-q', '--query', dest='query', action='store', help='enter some search terms', default='cats')
	parser.add_option('-t', '--to', dest='to', action='store', help='enter an email address')
	
	(opts, args) = parser.parse_args()
    
	api = cooperhewitt.api.client.OAuth2(access_token, hostname=hostname)
	method = 'cooperhewitt.search.objects'
	args = { 'query': opts.query, 'has_images': 'yes' }

	rsp = api.call(method, **args)
	
	now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')	
	os.makedirs("tmp/" + now)

	ofile  = open("tmp/" + now + "/" + "query.csv", "wb")
	writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
	
	writer.writerow(['object_id','filename', 'image_url', 'object_url'])
	
	# download images and create csv data
	
	for obj in rsp['objects']:
		for img in obj['images']:
			url = img['b']['url']
			file_name = url.split('/')[-1]
			print "Downloading " + url + "..."
			urllib.urlretrieve (img['b']['url'], "tmp/" + now + "/" + file_name)
			row = [obj['id'], file_name, url, 'http://collection.cooperhewitt.org/objects/'+obj['id']]
			writer.writerow(row)
	
	ofile.close()
	
	# write zip file to disk
	
	zf = zipfile.ZipFile("tmp/" + now + ".zip", "w")
	for dirname, subdirs, files in os.walk("tmp/" + now ):
	    zf.write(dirname)
	    for filename in files:
	        zf.write(os.path.join(dirname, filename))
	zf.close()
	
	# uplaod zip to s3
	
	conn = boto.connect_s3(s3_key, s3_secret)
	bucket = conn.get_bucket(s3_bucket)
	k = Key(bucket)
	k.key = now + ".zip"
	k.set_contents_from_filename("tmp/" + now + ".zip")
	k.make_public()
	
	# send an email with sendgrid
	if opts.to:
		s = sendgrid.Sendgrid(sendgrid_username, sendgrid_password, secure=True)

		body = """
		Hey ya,\n Thanks for your patience. Please us the URL below to download your zip file...\n
		"""
		body = body + "https://s3.amazonaws.com/download_tool/" + now + ".zip"

		message = sendgrid.Message("cooperhewitt@si.edu", "Your stuff is ready", body, body)
		message.add_to(opts.to)
		s.web.send(message)	
	
	
	
	
	
	