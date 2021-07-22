Attack
======

Target systems
--------------

Attack steps
------------

{% for e in events %}
    {% if e.event is eq("start") %}
        {% if e.type is eq("dropping_file") %}
            Dropping file to target
            ~~~~~~~~~~~~~~~~~~~~~~~
            At {{ e.timestamp }}

            The file {{ e.file_name }} is dropped to the target {{ e.target }}.
        {% endif %}
        {% if e.type is eq("execute_payload") %}
            Executing payload on target
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~
            At {{ e.timestamp }}

            The command {{ e.command }} is used to start a file on the target {{ e.target }}.
        {% endif %}
        {% if e.type is eq("narration") %}
            {{ e.text }}
        {% endif %}


        {% if e.sub_type is eq("metasploit") %}
            Metasploit attack {{ e.name }}
            ~~~~~~~~~~~~~~~~~~~~~~~~~~
            Tactics: {{ e.tactics }}
            Tactics ID: {{ e.tactics_id }}
            Hunting Tag: {{ e.hunting_tag}}

            At {{ e.timestamp }} a Metasploit command {{ e.name }} was used to attack {{ e.target }} from {{ e.source }}.

            {{ e.description }}

            {% if e.metasploit_command is string() %}
            Metasploit command: {{ e.metasploit_command }}
            {% endif %}

            {% if e.situation_description is string() %}
            Situation: {{ e.situation_description }}
            {% endif %}

            {% if e.countermeasure is string() %}
            Countermeasure: {{ e.countermeasure }}
            {% endif %}
        {% endif %}

        {% if e.sub_type is eq("kali") %}
            Kali attack {{ e.name }}
            ~~~~~~~~~~~~~~~~~~~~~~~~~~
            Tactics: {{ e.tactics }}
            Tactics ID: {{ e.tactics_id }}
            Hunting Tag: {{ e.hunting_tag}}

            At {{ e.timestamp }} a Kali command {{ e.kali_name }} was used to attack {{ e.target }} from {{ e.source }}.

            {{ e.description }}

            {% if e.kali_command is string() %}
            Kali command: {{ e.kali_command }}
            {% endif %}

            {% if e.situation_description is string() %}
            Situation: {{ e.situation_description }}
            {% endif %}

            {% if e.countermeasure is string() %}
            Countermeasure: {{ e.countermeasure }}
            {% endif %}
        {% endif %}

        {% if e.sub_type is eq("caldera") %}
            Caldera attack {{ e.name }}
            ~~~~~~~~~~~~~~~~~~~~~~~~~~
            Tactics: {{ e.tactics }}
            Tactics ID: {{ e.tactics_id }}
            Hunting Tag: {{ e.hunting_tag}}

            At {{ e.timestamp }} a Caldera ability {{ e.ability_id }}/"{{ e.name }}" was used to attack the group {{ e.target_group }} from {{ e.source }}.

            {{ e.description }}

            {% if e.situation_description is string() %}
            Situation: {{ e.situation_description }}
            {% endif %}

            {% if e.countermeasure is string() %}
            Countermeasure: {{ e.countermeasure }}
            {% endif %}
        {% endif %}





    {% endif %}  {# event equal start #}

{% endfor %}