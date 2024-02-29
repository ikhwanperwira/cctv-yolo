"""
This module provides functions to generate Cloudflare configuration files.

The functions in this module generate the 'cf-credentials.json' and 'cf-config.yaml' files
based on the provided configuration and environment variables.
"""

#pylint: disable=import-error
import os
import json
import yaml
from dotenv import load_dotenv
load_dotenv()

def load_cf_config():
  """
  Generate Cloudflare configuration files.

  This function generates the 'cf-credentials.json' and 'cf-config.yaml' files
  based on the provided configuration and environment variables.

  Args:
    None

  Returns:
    None
  """

  config = {
    'url': f'http://{os.getenv("HOST", "127.0.0.1")}:{os.getenv("PORT", "5000")}',
    'tunnel': os.getenv('TUNNEL_ID'),
    'credentials-file': './.cloudflared/cf-credentials.json'
  }

  creds = {
    'AccountTag': os.getenv('ACCOUNT_TAG'),
    'TunnelSecret': os.getenv('TUNNEL_SECRET'),
    'TunnelID': os.getenv('TUNNEL_ID')
  }

  with open(os.path.join(os.path.dirname(__file__), '../../.cloudflared/cf-credentials.json'), 'w', encoding='utf8') as file:
    json.dump(creds, file)

  with open(os.path.join(os.path.dirname(__file__), '../../.cloudflared/cf-config.yaml'), 'w', encoding='utf8') as file:
    yaml.dump(config, file)
