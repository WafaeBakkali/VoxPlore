import os

try:
    import certifi
    ca_bundle = certifi.where()
    if os.path.exists(ca_bundle):
        os.environ.setdefault("SSL_CERT_FILE", ca_bundle)
        os.environ.setdefault("REQUESTS_CA_BUNDLE", ca_bundle)
except ImportError:
    pass

from .agent import root_agent, get_agent_setup_config, AVATARS, VOICES, default_avatar, default_voice, preset, app_name, proactive_default
from .models import ClientMessage, ServerMessage, SetupMessage
from .tools import SessionState
from .toolrunner import run_function_call, handle_scene_event, load_paper, set_mode, add_upload, remove_upload
from . import genmedia
