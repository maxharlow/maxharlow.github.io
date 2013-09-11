#!/usr/bin/env python

import sys
import os
import shutil
import re
import glob
import datetime

def publish(source, templates):
	for article in articles(source):
		print('Publishing ' + article)
		modified = datestamp(article)
		template(article, templates)
		if modified: organise(article)
	print('Done!')

def articles(path):
        articles = glob.glob(path + '/*.article') if os.path.isdir(path) else glob.glob(path)
	return [filename.replace('.article', '') for filename in articles]

def datestamp(article):
	content = open(article + '.article', 'r+')
        body = content.readlines()
        modified = False
        if '</time>' not in body[0]:
                now = datetime.datetime.now()
		content.seek(0)
		content.write('<time datetime="{0}">{1}</time>\n'.format(now.isoformat(), now.strftime('%A %d %B %Y')))
		content.writelines(body)
                modified = True
	content.close()
        return modified

def template(article, templates):
	content = open(article + '.article', 'r')
	body = content.read()
        title = re.search('<h1>(.*)</h1>', body).group(1)
	for templatefilename in glob.glob(templates + '/*') if os.path.isdir(templates) else glob.glob(templates):
		templatefile = open(templatefilename, 'r')
		template = templatefile.read()
		templatefile.close()
		formatted = template.format(TITLE=title, BODY=body)
		output = open(article + '.html', 'w')
		output.write(formatted)
		output.close()
        content.close()

def organise(article):
	year = str(datetime.datetime.now().year)
	if not os.path.exists(year): os.makedirs(year)
        for file in glob.glob(article + '.*'): shutil.move(file, year)

source = sys.argv[1] if len(sys.argv) > 1 else 'drafts/*'
templates = sys.argv[2] if len(sys.argv) > 2 else 'templates/*'

publish(source, templates)
