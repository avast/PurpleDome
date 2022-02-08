*********
Structure
*********

Structure of an experiment flow. Plugin calls have boxes with extra squares at the left.

.. graphviz::
    :name: Experiment flow
    :caption: Experiment flow
    :alt: The way an experiment is conducted
    :align: center

     digraph "sphinx-ext-graphviz" {
         size="6, 30";

         graph [fontname="Verdana", fontsize="12"];
         node [fontname="Verdana", fontsize="12"];
         edge [fontname="Sans", fontsize="9"];

        start_attacker [label="start attacker", shape="box", fillcolor=green, style=filled]
        start_targets [label="start targets", shape="box", fillcolor=green, style=filled]
        start_caldera [label="start caldera", shape="box", fillcolor=green, style=filled]
        prime_vulnerabilities [label="prime vulnerabilities", shape="component", fillcolor=green, style=filled]
        prime_sensors [label="prime sensors", shape="component", fillcolor=green, style=filled]
        install_vulnerabilities [label="install vulnerabilities", shape="component", fillcolor=green, style=filled]
        install_sensors [label="install sensors", shape="component", fillcolor=green, style=filled]
        start_caldera_implants [label="start caldera implants", shape="box", fillcolor=green, style=filled]
        run_caldera_attacks [label="run caldera attacks", shape="box", fillcolor=red, style=filled]
        run_plugin_attacks [label="run plugin attacks", shape="component", fillcolor=red, style=filled]
        stop_sensors [label="stop sensors", shape="component", fillcolor=lightblue, style=filled]
        collect_sensors [label="collect sensors", shape="component", fillcolor=yellow, style=filled]
        stop_vulnerabilities [label="stop vulnerabilities", shape="component", fillcolor=lightblue, style=filled]
        stop_targets [label="stop targets", shape="component", fillcolor=lightblue, style=filled]
        stop_attacker [label="stop attacker", shape="component", fillcolor=lightblue, style=filled]
        generate_documents [label="generate documents", shape="box", fillcolor=yellow, style=filled]
        collect_loot [label="collect loot", shape="box", fillcolor=yellow, style=filled]


        start_attacker -> start_targets
        start_targets -> start_caldera
        start_caldera->prime_vulnerabilities
        prime_vulnerabilities->prime_sensors
        prime_sensors->install_vulnerabilities
        install_vulnerabilities->install_sensors
        install_sensors->start_caldera_implants
        start_caldera_implants->run_caldera_attacks
        run_caldera_attacks->run_plugin_attacks
        run_plugin_attacks->stop_sensors
        stop_sensors->collect_sensors
        collect_sensors->stop_vulnerabilities
        stop_vulnerabilities->stop_targets
        stop_targets->stop_attacker
        stop_attacker->generate_documents
        generate_documents->collect_loot

    }