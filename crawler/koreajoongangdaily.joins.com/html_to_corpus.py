import os
from pyquery import PyQuery as pq

def get_eng_title(q):
	title = q('h3[id="sTitle_a"]').html()
	return remove_tag(title)

def get_eng_content(q):
	content = q('div[class="article_dvleft"] div[class="article_content"]').html()
	if content:
		return remove_tag(content)

	content = q('div[class="article_content"] tr td:first-child').html()
	if content:
		return remove_tag(content)

	return ''

def get_kor_title(q):
	title_selector = q('div[class="article_content"] font[color="014A77"]');
	title = title_selector.html()
	ret = remove_tag(title)
	if len(ret) > 0:
		title_selector.remove()
		return ret

	title = q('div[class="title"] h4').html()
	ret = remove_tag(title)
	if len(ret) > 0:
		return ret

	return '';

def get_kor_content(q):
	content = q('div[class="article_dvright"] div[class="article_content"]').html()
	if content:
		return remove_tag(content)

	content = q('div[class="article_content"] tr td:last-child').html()
	if content:
		return remove_tag(content)

	return ''

def remove_tag(s):
	if s is None:
		return ''
	s = s.encode('utf-8', 'replace')
	s = s.replace('<br>', '\n')
	ret = ''
	tag = 0
	for i in range(0, len(s)):
		if s[i] == '<':
			tag += 1
		if tag == 0:
			ret += s[i]
		if s[i] == '>':
			tag -= 1

	return ret.strip()



#######

proc_count = 0;
count = 0;

html_path = './html'
result_path = './parallel_corpus'
for filename in os.listdir(html_path):
	if not filename.endswith('.html'):
		continue
	count += 1;

	print 'process ' + filename

	filepath = html_path + '/' + filename
	q = pq(filename=filepath)
	eng_title = get_eng_title(q)
	eng_content = get_eng_content(q)
	kor_title = get_kor_title(q)
	kor_content = get_kor_content(q)

	aid = filename.split('.')[0]
	filename_eng = result_path + '/' + aid + '.eng.txt'
	filename_kor = result_path + '/' + aid + '.kor.txt'

	if len(eng_title) == 0 or len(eng_content) == 0 or len(kor_title) == 0 or len(kor_content) == 0:
		continue

	proc_count += 1;
	with open(filename_eng, 'w') as f:
		f.write(eng_title + "\n")
		f.write(eng_content)

	with open(filename_kor, 'w') as f:
		f.write(kor_title + "\n")
		f.write(kor_content)

print 'SUMMARY : %d / %d html success...' % (proc_count, count)