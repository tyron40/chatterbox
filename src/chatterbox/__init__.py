# Set version directly instead of trying to get from package metadata
__version__ = "1.0.0"

from .tts import ChatterboxTTS
from .vc import ChatterboxVC
from .mtl_tts import ChatterboxMultilingualTTS, SUPPORTED_LANGUAGES
