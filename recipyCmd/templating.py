from jinja2 import Template

run_template = """\aRun ID:\b {{ unique_id }}
\aCreated by\b {{ author }} on {{ date }} UTC
\aRan\b {{ script }} using {{ command }}
{% if command_args %}
Using command-line arguments: {{ command_args }}
{% endif %}

{%- if gitcommit %}
\aGit:\b commit {{ gitcommit }}, in repo {{ gitrepo }}, with origin {{ gitorigin }}
{% endif %}
{% if svnrepo %}
\aSvn:\b commit {{ svncommit }}, in repo {{ svnrepo }}
{% endif %}
\aEnvironment:\b {{ environment|join(", ") }}
{% if libraries %}
\aLibraries:\b {{ libraries|join(", ") }}
{% endif %}
{% if exception %}
\aException:\b ({{ exception.type }}) {{ exception.message }}
{% endif -%}

\aInputs:\b
{% if not inputs %}
none
{% else %}
{% for input in inputs %}
{% if input is string %}
{{ input }}
{% else %}
{{ input[0] }} ({{ input[1] }})
{% endif %}
{% endfor %}
{% endif -%}

\aOutputs:\b
{% if not outputs %}
none
{% else %}
{% for output in outputs %}
{% if output is string %}
{{ output }}
{% else %}
{{ output[0] }} ({{ output[1] }})
{% endif %}
{% endfor %}
{% endif %}

{%- if notes %}
\aNotes:\b
{{ notes }}
{% endif %}
"""

debug_template = """DB path: {{ db_path }}
Full config file (as interpreted):
----------------------------------
{{ config }}
----------------------------------
"""

BOLD = '\033[1m'
RESET = '\033[0m'

template_str_withcolor = run_template.replace('\a', BOLD).replace('\b', RESET)
template_str_nocolor = run_template.replace('\a', '').replace('\b', '')


def render_run_template(run, nocolor=False):
    """Renders the template for single run / result """
    if nocolor:
        template_str = template_str_nocolor
    else:
        template_str = template_str_withcolor
    template = Template(template_str, trim_blocks=True)
    return template.render(**run)


def render_debug_template(db_path, config):
    template = Template(debug_template)
    return template.render(db_path=db_path, config=config)
