# coding=utf-8

import os
import fire

content ='''---
layout: default
---
<div>
	<h2>{title}</h2>
	<hr>
		{{% for post in site.categories.{category} %}}
			<div class="post-preview">
				<span class="post-title">
					<a class="post-link" href="{{{{ post.url | prepend: site.baseurl }}}}">
						{{{{ post.title }}}}
					</a>
				</span>
				<span class="post-time">
					<p>{{{{ post.date | date: "%b %-d, %Y" }}}}</p>
				</span>
			</div>
		{{% endfor %}}
	</div>

<style>
	.block{{
		display: inline-block;
		margin:5px;
	}}
</style>'''

def passchange_category_name_into_english(posts_dir):
    files = os.listdir(posts_dir)
    for file in files:
        data = ''
        with open(posts_dir + '/' + file, 'r+') as f:
        	for line in f.readlines():
				if (line.find('categories: 面试') == 0):
					line = 'categories: Interview' + '\n'
				if (line.find('categories: 杂谈') == 0):
					line = 'categories: Others' + '\n'
				if (line.find('categories: 汇编') == 0):
					line = 'categories: Assembly' + '\n'

				data += line

		with open(posts_dir + '/' + file, 'r+') as f:
			f.writelines(data)


def create_category_pages(github_pages_dir):
	# find categories in blogs
	category_set = set()
	files = os.listdir(github_pages_dir + '/_posts')
	for file in files:
		with open(github_pages_dir + '/_posts/' + file, 'r') as f:
			category_str = ''
			for line in range(1, 7):
				category_str = f.readline()
	    	category_str_list = category_str.split(' ')
	    	if category_str_list[0] == 'categories:':
	    		category = category_str_list[1]
	    		category_set.add(category)

	# create category pages
	blog_dir = github_pages_dir + '/blog'
	for page_name in category_set:
		page_name = page_name.strip('\n')
		
		write_content = content.format(title=page_name, category=page_name)
		if not os.path.exists(blog_dir + '/' + page_name):
			page_dir = os.mkdir(blog_dir + '/' + page_name)
			
		with open(blog_dir + '/' + page_name + '/' + 'index.html', 'w') as f:		
			f.write(write_content)


if __name__ == '__main__':
    fire.Fire(create_category_pages)