# csdn2md

## 简介
移植 csdn 博客移植到我的 [Github pages](https://0lddriv3r.github.io)上，并加上jekyll所需要的头部说明（layout、title、date、categories和`_post`文件基本格式）。若你的博客系统使用的是其他框架，请修改头部说明格式。

## 使用步骤
1. `uas.txt`文件存放**UA**。
2. 登录自己的 csdn 博客，把 cookies 复制到 `cookies.txt` 文件里。
3. 使用**Fire**命令行工具`python csdn2md.py username total_pages cookies_file start stop jekyll md_dir`（后四个有默认参数）。

*注：该导出程序对于markdown和非markdown格式博客文件均可。*