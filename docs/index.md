put md file here , github pages use this dir
{% for page in site.pages %}
  {% if page.name != 'index.md' %}
- [{{ page.title | default: page.name | replace: ".md", "" }}]({{ page.url | relative_url }})
  {% endif %}
{% endfor %}
