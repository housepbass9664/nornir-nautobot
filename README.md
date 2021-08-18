# nornir-nautobot
This project aims to generate full device configurations using nornir as the orchestrator and nautobot as the data source. I want to use a few tools as humanly possible to build a complete automation system, only adding tools as they become absolutely necessary. 

Use this file to install the packages I'm using:
pip install -r requirements.txt 

The j2 templates are currently a work in progress but can be easily expanded upon. The main script is "apply_nautobot_cfg.py" and uses nornir and the pynautobot api client. 
