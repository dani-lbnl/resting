#!/bin/sh
python3 process_metadata_ieee8023.py
python3 process_actual_metadata.py
python3 process_COVID-19_metadata.py
python3 process_figure_metadata.py
python3 generate_Source_description.py
