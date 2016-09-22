from jinja2 import Template

template_str = """\aRun ID:\b {{ unique_id }}
\aCreated by\b {{ author }} on {{ date }} UTC
\aRan\b {{ script }} using {{ command }}
{% if command_args|length > 0 %}
Using command-line arguments: {{ command_args }}
{% endif %}
{% if gitcommit is defined %}
\aGit:\b commit {{ gitcommit }}, in repo {{ gitrepo }}, with origin {{ gitorigin }}
{% endif %}
{% if svnrepo is defined %}
\aSvn:\b commit {{ svncommit }}, in repo {{ svnrepo }}.
{% endif %}
\aEnvironment:\b {{ environment|join(", ") }}
{% if libraries is defined %}
\aLibraries:\b {{ libraries|join(", ") }}
{% endif %}
{% if exception is defined %}
\aException:\b ({{ exception.type }}) {{ exception.message }}
{% endif %}
{% if inputs|length == 0 %}
\aInputs:\b none
{% else %}
\aInputs:\b
{% for input in inputs %}
{% if input is string %}
{{ input }}
{% else %}
{{ input[0] }} ({{ input[1] }})
{% endif %}
{% endfor %}
{% endif %}
{% if outputs | length == 0 %}
\aOutputs:\b none
{% else %}
\aOutputs:\b
{% for output in outputs %}
{% if output is string %}
{{ output }}
{% else %}
{{ output[0] }} ({{ output[1] }})
{% endif %}
{% endfor %}
{% endif %}
{% if notes is defined %}
\aNotes:\b
{{ notes }}
{% endif %}
"""

BOLD = '\033[1m'
RESET = '\033[0m'

template_str_withcolor = template_str.replace('\a', BOLD).replace('\b', RESET)
template_str_nocolor = template_str.replace('\a', '').replace('\b', '')


def template_result(r, nocolor=False):
    # Print a single result from the search
    if nocolor:
        template_str = template_str_nocolor
    else:
        template_str = template_str_withcolor

    template = Template(template_str, trim_blocks=True)
    return template.render(**r)

