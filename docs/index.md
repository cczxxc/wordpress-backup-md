put md file here , github pages use this dir
---
layout: default
title: 文档目录
---

# 📚 文档目录

{% for page in site.pages %}
  {% if page.path contains 'docs/' and page.path != 'docs/index.md' and page.url != '/' %}
- [{{ page.title | default: page.name | replace: ".md", "" }}]({{ page.url | relative_url }})
  {% endif %}
{% endfor %}

