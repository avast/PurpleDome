Attack
======

Boilerplate
-----------

PurpleDome, attack-log version: {{ boilerplate.log_format_major_version }}.{{ boilerplate.log_format_minor_version }}

Systems
-------

{% for s in systems %}
{{ s.role }}:{{ s.name }}
~~~~~~~~~~~~
IP: {{ s.ip }}

OS: {{ s.os }}

Paw: {{ s.paw }}

Group: {{ s.group }}

Sensors:

{% for sensor in s.sensors %}
* {{ sensor }}
{% endfor %}  {# sensors #}

Vulnerabilities:

{% for vulnerability in s.vulnerabilities %}
* {{ vulnerability }}
{% endfor %}  {# vulnerabilities #}

{% endfor %}  {# systems #}

Attack steps
------------
{% for e in events %}
{% if e.event is eq("start") %}
{% if e.type is eq("attack_step") %}


{{ e.text }}
~~~~~~~~~~~~
{% endif %}  {# end attack_step #}
{% if e.type is eq("dropping_file") %}

Dropping file to target
_______________________
At {{ e.timestamp }}
The file {{ e.file_name }} is dropped to the target {{ e.target }}.
{% endif %}
{% if e.type is eq("execute_payload") %}

Executing payload on target
___________________________
At {{ e.timestamp }}
The command {{ e.command }} is used to start a file on the target {{ e.target }}.
{% endif %}
{% if e.type is eq("narration") %}
{{ e.text }}
{% endif %}
{% if e.sub_type is eq("metasploit") %}

Metasploit attack {{ e.name }}
______________________________
+ Tactics: {{ e.tactics }}
+ Tactics ID: {{ e.tactics_id }}
+ Hunting Tag: {{ e.hunting_tag}}
+ At {{ e.timestamp }} a Metasploit command {{ e.name }} was used to attack {{ e.target }} from {{ e.source }}.
+ Description: {{ e.description }}
{% if e.metasploit_command is string() %}
+ Metasploit command: {{ e.metasploit_command }}
{% endif %}
{% if e.situation_description is string() %}
+ Situation: {{ e.situation_description }}
{% endif %}
{% if e.countermeasure is string() %}
+ Countermeasure: {{ e.countermeasure }}
{% endif %}
{% if e.result is string() %}
Attack result::

        {{ e.result }}
{% endif %}
{% if e.result is iterable() %}
Attack result::

{% for item in e.result %}
    {{ item|trim()|indent(4) }}
{% endfor %}
{% endif %}
{% endif %}
{% if e.sub_type is eq("kali") %}

Kali attack {{ e.name }}
________________________
+ Tactics: {{ e.tactics }}
+ Tactics ID: {{ e.tactics_id }}
+ Hunting Tag: {{ e.hunting_tag}}
+ At {{ e.timestamp }} a Kali command {{ e.kali_name }} was used to attack {{ e.target }} from {{ e.source }}.
+ Description: {{ e.description }}
{% if e.kali_command is string() %}
+ Kali command: {{ e.kali_command }}
{% endif %}
{% if e.situation_description is string() %}
+ Situation: {{ e.situation_description }}
{% endif %}
{% if e.countermeasure is string() %}
+ Countermeasure: {{ e.countermeasure }}
{% endif %}
{% if e.result is string() %}
Attack result::

    {{ e.result }}
{% endif %}
{% if e.result is iterable() %}
Attack result::

{% for item in e.result %}
    {{ item|trim()|indent(4) }}
{% endfor %}
{% endif %}
{% endif %}
{% if e.sub_type is eq("caldera") %}

Caldera attack {{ e.name }}
___________________________
+ Tactics: {{ e.tactics }}
+ Tactics ID: {{ e.tactics_id }}
+ Hunting Tag: {{ e.hunting_tag}}
+ At {{ e.timestamp }} a Caldera ability {{ e.ability_id }}/"{{ e.name }}" was used to attack the group {{ e.target_group }} from {{ e.source }}.
+ Description: {{ e.description }}
{% if e.situation_description is string() %}
+ Situation: {{ e.situation_description }}
{% endif %}
{% if e.countermeasure is string() %}
+ Countermeasure: {{ e.countermeasure }}
{% endif %}
{% if e.result is string() %}
Attack result::

    {{ e.result }}
{% endif %}
{% if e.result is iterable() %}
Attack result::

{% for item in e.result %}
    {{ item|trim()|indent(4) }}
{% endfor %}
{% endif %}
{% endif %}
{% endif %}  {# event equal start #}
{% endfor %}


Tools
-----
{% for e in events %}
{% if e.event is eq("start") %}
{% if e.type is eq("build") %}
Building tool {{ e.filename }}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The file {{ e.filename }} is built
{% if e.for_step %}
It will be used in Step {{ e.for_step }}
{% endif %}
Build time is between {{ e.timestamp }} and {{ e.timestamp_end }}
{% if e.dl_uri is string() %}
Built from source downloaded from {{ e.dl_uri }}
{% endif %}
{% if e.dl_uris %}
Built from sources downloaded from
{% for i in e.dl_uris %}
* {{ i }}
{% endfor %}
{% endif %}
{% if e.payload is string() %}
The attack tool uses a Meterpreter payload. The payload is {{ e.payload }}. The payload is built for the {{ e.platform }} platform and the {{ e.architecture }} architecture.
The settings for lhost and lport are {{ e.lhost }}/{{ e.lport }}.
{% endif %}
{% if e.encoding is string() %}
The file was encoded using {{ e.encoding }} after compilation.
{% endif %}
{% if e.encoded_filename is string() %}
The encoded version is named {{ e.encoded_filename }}.
{% endif %}
{% if e.SRDI_conversion %}
The attack tool was converted to position independent shellcode. See: https://github.com/monoxgas/sRDI
{% endif %}
{{ e.comment }}
{% endif %}
{% endif %}

{% endfor %}

