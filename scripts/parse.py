from os import path, getenv
import requests
import re
from sys import argv, exit

from markdownify import markdownify
from bs4 import BeautifulSoup


YEAR = 2020
BASE_URL = 'https://adventofcode.com'
BASE_URL_DAY = BASE_URL + '/{}/day/'.format(YEAR)

LORE_MD_FORMAT = 'day-{}-{}.md'

REANY = r"(?:.|\n)*?"

BLOCK_PLACE = ('#__BLOCK_START__#', '#__BLOCK_END__#')
CODE_PLACE = ('#__CODE_START__#', '#__CODE_END__#')
BOLD_PLACE = ('#__BOLD_START__#', '#__BOLD_END__#')


if len(argv) <= 1:
  raise Exception('Require first argument to be day number')

if not getenv('SESSION'):
  raise Exception('No SESSION in environment')

day = argv[1]
cookies = {'session': getenv('SESSION')}

try:
  problem_url = BASE_URL_DAY + day
  response = requests.get(problem_url, cookies=cookies)
  html = response.content.decode('utf-8')
except request.URLError as e:
  raise


soup = BeautifulSoup(html, features='html.parser')
elements = soup.select('article.day-desc')

if not elements:
  raise Exception('No description')

article = ''.join(str(e) for e in elements)
# content = str(article)[len('<main>'):][:-len('</main>')]
content = str(article)[len('<article class="day-desc">'):][:-len('</article>')]

# Remove article tags
content = re.sub(r"<article[^<]*>", r"", content)
content = re.sub(r"</article>", r"---\n\n", content)

# Inline code
content = re.sub(r"(?<!<pre>)<code>([^<]*)</code>", r"`\1`", content)

def emphasis_inside(content, start_tag, end_tag, replace):
  emcode_pattern = rf"(?<!<pre>)({start_tag})((?:(?!{end_tag})(?:.|\n))*?<em>[^<]*</em>{REANY})({end_tag})"
  content = re.sub(emcode_pattern, rf"{replace[0]}\2{replace[1]}", content)

  while True:
    pattern = rf"({replace[0]}{REANY})<em>([^<]*)</em>({REANY}{replace[1]})"
    replacement = rf"\1{BOLD_PLACE[0]}\2{BOLD_PLACE[1]}\3"
    content, n = re.subn(pattern, replacement, content)
    if n == 0: break

  return content

# Emphasis inside code blocks
content = emphasis_inside(content, '<pre><code>', '</code></pre>', BLOCK_PLACE)

# Emphasis inside inline code
content = emphasis_inside(content, '<code>', '</code>', CODE_PLACE)

# Emphasis
content = re.sub(r"<em>([^<]*)</em>", r"**\1**", content)
content = re.sub(r"<em class=\"star\">([^<]*)</em>", r"_**\1**_", content)

# Links
link_pattern = r"<a href=\"([^\"]*)\">([^<]*)</a>"
content = re.sub(link_pattern, rf"[\2]({BASE_URL}\1)", content)

# Code blocks
content = re.sub(r"<pre><code>([^<]*)</code></pre>", r"```\n\1```\n", content)

# Useless elements
content = re.sub(r"<span[^>]*>([^<]*)</span>", r"\1", content)

# Header
content = re.sub(r"<h2>([^<]*)</h2>", r"## \1\n\n", content)
content = re.sub(r"<h2[^>]+>([^<]*)</h2>", r"### \1\n\n", content)

# Paragraphs
content = re.sub(r"<p>([^<]*)</p>", r"\1\n", content)

# List elements
content = re.sub(rf"<li>({REANY})</li>", r"- \1", content)
content = re.sub(r"\n?<ul>", r"", content)
content = re.sub(r"</?ul>", r"", content)

# Replace placeholders
block_place_pattern = rf"{BLOCK_PLACE[0]}({REANY}){BLOCK_PLACE[1]}\n"
content = re.sub(block_place_pattern, r"<pre>\1</pre>", content)

code_place_pattern = rf"{CODE_PLACE[0]}(.*?){CODE_PLACE[1]}"
content = re.sub(code_place_pattern, r"<code>\1</code>", content)

bold_place_pattern = rf"{BOLD_PLACE[0]}(.*?){BOLD_PLACE[1]}"
content = re.sub(bold_place_pattern, r"<b>\1</b>", content)

# Titles
content = re.sub(r"(##*\s)---\s(.*?)\s---", r"\1\2", content)

content = content.strip()
content += '\n\n'
content += '---\n\n'
content += '[View the original source here]({})'.format(problem_url, problem_url)

if len(argv) > 2:
  match = re.match(r"##*\sDay\s\d+:\s(.*?)\s*\n", content)
  title = match.groups()[0]
  title = re.sub(r"([^aA-zZ0-9 ])", r"", title)

  directory = argv[2]
  filename = LORE_MD_FORMAT.format(day, '-'.join(title.lower().split()))
  file = path.abspath(path.join(directory, filename))

  with open(file, "w") as fd:
    fd.write(content)

  exit()

print(content)
