"""
Chatterbox TTS Enhanced - Main Application
A high-quality voice cloning, text-to-speech & voice conversion application
"""
import sys
import os

# Add src directory and project root to sys.path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

src_path = os.path.join(project_root, "src")
if src_path not in sys.path:
    sys.path.append(src_path)

import gradio as gr
from modules.config import LANGUAGE_CONFIG, SUPPORTED_LANGUAGES
from modules.voice_manager import (
    load_voices, 
    get_voices_for_language, 
    get_all_voices_with_gender,
    resolve_voice_path,
    clone_voice,
    delete_voice
)
from modules.generation_functions import (
    generate_speech,
    generate_multilingual_speech,
    convert_voice,
    generate_turbo_speech,
    generate_batch_turbo_speech,
    create_batch_zip
)
from modules.audio_mixer import mix_audio_with_music

# Import UI components
from modules.ui_components import (
    create_header,
    create_tts_tab,
    create_multilingual_tab,
    create_voice_conversion_tab,
    create_clone_voice_tab,
    create_turbo_tab,
    create_batch_tab,
    create_cinematic_mixer_tab
)

# Load voices at startup
available_voices = load_voices()

# Custom CSS for Turbo tag buttons
CUSTOM_CSS = """
.tag-container {
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 8px !important;
    margin-top: 5px !important;
    margin-bottom: 10px !important;
    border: none !important;
    background: transparent !important;
}
.tag-btn {
    min-width: fit-content !important;
    width: auto !important;
    height: 32px !important;
    font-size: 13px !important;
    background: #eef2ff !important;
    border: 1px solid #c7d2fe !important;
    color: #3730a3 !important;
    border-radius: 6px !important;
    padding: 0 10px !important;
    margin: 0 !important;
    box-shadow: none !important;
}
.tag-btn:hover {
    background: #c7d2fe !important;
    transform: translateY(-1px);
}
"""

# ---------------------------
# Main Application
# ---------------------------
with gr.Blocks(title="Chatterbox TTS Enhanced", theme=gr.themes.Soft(), css=CUSTOM_CSS) as demo:
    # State variables
    tts_model_state = gr.State(None)
    vc_model_state = gr.State(None)
    mtl_model_state = gr.State(None)
    
    # Header
    create_header()
    
    # Create tabs
    with gr.Tab("⚡ Turbo TTS"):
        turbo_components = create_turbo_tab()
    
    with gr.Tab("📦 Batch TTS"):
        batch_components = create_batch_tab()

    with gr.Tab("🎤 TTS Main (English)"):
        tts_components = create_tts_tab()
    
    with gr.Tab("🌍 Multilingual TTS"):
        mtl_components = create_multilingual_tab()
    
    with gr.Tab("🔄 Voice Conversion"):
        vc_components = create_voice_conversion_tab()
    
    with gr.Tab("🧬 Clone Voice"):
        clone_components = create_clone_voice_tab()
    
    with gr.Tab("🎬 Cinematic Mixer"):
        mixer_components = create_cinematic_mixer_tab()
    
    # ---------------------------
    # Event Handlers - TTS Tab
    # ---------------------------
    tts_components['generate_btn'].click(
        fn=generate_speech,
        inputs=[
            tts_components['text'],
            tts_components['voice_select'],
            tts_components['exaggeration'],
            tts_components['temp'],
            tts_components['seed_num'],
            tts_components['cfg_weight'],
            tts_components['min_p'],
            tts_components['top_p'],
            tts_components['repetition_penalty']
        ],
        outputs=[
            tts_components['progress_bar'],
            tts_components['audio_output'],
            tts_components['status_box']
        ]
    )
    
    # Update preview when voice changes
    def update_tts_preview(voice_name):
        path = resolve_voice_path(voice_name, "en")
        return path

    tts_components['voice_select'].change(
        fn=update_tts_preview,
        inputs=[tts_components['voice_select']],
        outputs=[tts_components['preview_audio']]
    )
    
    # ---------------------------
    # Event Handlers - Turbo Tab
    # ---------------------------
    turbo_components['generate_btn'].click(
        fn=generate_turbo_speech,
        inputs=[
            turbo_components['text'],
            turbo_components['voice_select']
        ],
        outputs=[
            turbo_components['progress_bar'],
            turbo_components['audio_output'],
            turbo_components['status_box']
        ]
    )
    
    # Update preview when voice changes (Turbo)
    def update_turbo_preview(voice_name):
        path = resolve_voice_path(voice_name, "en")
        return path

    turbo_components['voice_select'].change(
        fn=update_turbo_preview,
        inputs=[turbo_components['voice_select']],
        outputs=[turbo_components['preview_audio']]
    )
    
    # Tag insertion buttons (Turbo) - JavaScript for cursor position
    INSERT_TAG_JS = """
    (tag_val, current_text) => {
        const textarea = document.querySelector('#turbo_textbox textarea');
        if (!textarea) return current_text + " " + tag_val;
        const start = textarea.selectionStart;
        const end = textarea.selectionEnd;
        let prefix = " ";
        let suffix = " ";
        if (start === 0) prefix = "";
        else if (current_text[start - 1] === ' ') prefix = "";
        if (end < current_text.length && current_text[end] === ' ') suffix = "";
        return current_text.slice(0, start) + prefix + tag_val + suffix + current_text.slice(end);
    }
    """
    
    # Create tag button handlers
    for btn_name in ['btn_clear_throat', 'btn_sigh', 'btn_shush', 'btn_cough', 'btn_groan', 
                     'btn_sniff', 'btn_gasp', 'btn_chuckle', 'btn_laugh']:
        turbo_components[btn_name].click(
            fn=None,
            inputs=[turbo_components[btn_name], turbo_components['text']],
            outputs=turbo_components['text'],
            js=INSERT_TAG_JS
        )
    
    # ---------------------------
    # Event Handlers - Multilingual Tab
    # ---------------------------
    mtl_components['generate_btn'].click(
        fn=generate_multilingual_speech,
        inputs=[
            mtl_components['text'],
            mtl_components['voice_select'],
            mtl_components['language_select'],
            mtl_components['exaggeration'],
            mtl_components['temp'],
            mtl_components['seed_num'],
            mtl_components['cfg_weight']
        ],
        outputs=[
            mtl_components['progress_bar'],
            mtl_components['audio_output'],
            mtl_components['status_box']
        ]
    )
    
    # Update language change
    mtl_components['language_select'].change(
        fn=lambda lang: (
            LANGUAGE_CONFIG.get(lang, {}).get("text", ""),
            gr.update(choices=get_voices_for_language(lang), value=f"Default ({SUPPORTED_LANGUAGES.get(lang, lang)})")
        ),
        inputs=[mtl_components['language_select']],
        outputs=[mtl_components['text'], mtl_components['voice_select']]
    )
    
    # Update preview when voice changes (Multilingual)
    def update_mtl_preview(voice_name, language_code):
        path = resolve_voice_path(voice_name, language_code)
        return path

    mtl_components['voice_select'].change(
        fn=update_mtl_preview,
        inputs=[mtl_components['voice_select'], mtl_components['language_select']],
        outputs=[mtl_components['sample_audio']]
    )
    
    # ---------------------------
    # Event Handlers - Voice Conversion Tab
    # ---------------------------
    vc_components['convert_btn'].click(
        fn=convert_voice,
        inputs=[vc_components['input_audio'], vc_components['target_voice_select']],
        outputs=[vc_components['progress_bar'], vc_components['audio_output'], vc_components['status_box']]
    )
    
    # Update preview when voice changes (VC)
    def update_vc_preview(voice_name):
        if voice_name == "None": 
            return None
        
        clean_name = voice_name.replace(" ♂️", "").replace(" ♀️", "")
        
        if clean_name.startswith("Default ("):
            lang_name = clean_name.split("(")[1].split(")")[0]
            for code, name in SUPPORTED_LANGUAGES.items():
                if name == lang_name:
                    return LANGUAGE_CONFIG.get(code, {}).get("audio")
        
        from modules.voice_manager import VOICES
        possible_names = [clean_name, f"{clean_name}_male", f"{clean_name}_female"]
        
        for name in possible_names:
            if name in VOICES["samples"]:
                return VOICES["samples"][name]
        
        for code in SUPPORTED_LANGUAGES:
            for name in possible_names:
                full_name = f"{name}_{code}"
                if full_name in VOICES["samples"]:
                    return VOICES["samples"][full_name]
        
        return None

    vc_components['target_voice_select'].change(
        fn=update_vc_preview,
        inputs=[vc_components['target_voice_select']],
        outputs=[vc_components['preview_audio']]
    )
    
    # ---------------------------
    # Event Handlers - Clone Voice Tab
    # ---------------------------
    clone_components['clone_btn'].click(
        fn=clone_voice,
        inputs=[
            clone_components['ref_audio_input'],
            clone_components['new_voice_name'],
            clone_components['voice_language'],
            clone_components['voice_gender']
        ],
        outputs=[clone_components['clone_status'], tts_components['voice_select']]
    ).then(
        fn=lambda: gr.update(choices=get_voices_for_language("en")),
        outputs=[tts_components['voice_select']]
    ).then(
        fn=lambda: gr.update(choices=get_voices_for_language("en")),
        outputs=[turbo_components['voice_select']]
    ).then(
        fn=lambda: gr.update(choices=get_voices_for_language("en")),
        outputs=[batch_components['global_voice']]
    ).then(
        fn=lambda lang: gr.update(choices=get_voices_for_language(lang)),
        inputs=[mtl_components['language_select']],
        outputs=[mtl_components['voice_select']]
    ).then(
        fn=lambda: gr.update(choices=["None"] + get_all_voices_with_gender()),
        outputs=[vc_components['target_voice_select']]
    ).then(
        fn=lambda: "\n".join(load_voices()) if load_voices() else "No voices cloned yet",
        outputs=[clone_components['current_voices_display']]
    ).then(
        fn=lambda: gr.update(choices=["None"] + get_all_voices_with_gender(), value="None"),
        outputs=[clone_components['voice_to_delete']]
    )
    
    clone_components['delete_btn'].click(
        fn=delete_voice,
        inputs=[clone_components['voice_to_delete']],
        outputs=[clone_components['delete_status'], clone_components['voice_to_delete']]
    ).then(
        fn=lambda: gr.update(choices=get_voices_for_language("en")),
        outputs=[tts_components['voice_select']]
    ).then(
        fn=lambda: gr.update(choices=get_voices_for_language("en")),
        outputs=[turbo_components['voice_select']]
    ).then(
        fn=lambda: gr.update(choices=get_voices_for_language("en")),
        outputs=[batch_components['global_voice']]
    ).then(
        fn=lambda lang: gr.update(choices=get_voices_for_language(lang)),
        inputs=[mtl_components['language_select']],
        outputs=[mtl_components['voice_select']]
    ).then(
        fn=lambda: gr.update(choices=["None"] + get_all_voices_with_gender()),
        outputs=[vc_components['target_voice_select']]
    ).then(
        fn=lambda: "\n".join(load_voices()) if load_voices() else "No voices cloned yet",
        outputs=[clone_components['current_voices_display']]
    )
    
    # ---------------------------
    # Event Handlers - Batch Tab
    # ---------------------------
    def toggle_voice_dropdowns(use_same):
        updates = []
        for voice_input in batch_components['voice_inputs']:
            updates.append(gr.update(visible=not use_same))
        return updates
    
    batch_components['use_same_voice'].change(
        fn=toggle_voice_dropdowns,
        inputs=[batch_components['use_same_voice']],
        outputs=batch_components['voice_inputs']
    )
    
    # State to store generated audios
    batch_audio_state = gr.State([None] * 50)
    
    # Batch generation handler with background music support
    def batch_generate_wrapper(use_same_voice, global_voice, *all_inputs):
        """Wrapper to handle batch generation with background music."""
        num_fields = 50
        text_list = list(all_inputs[:num_fields])
        voice_list = list(all_inputs[num_fields:num_fields*2])
        bgmusic_list = list(all_inputs[num_fields*2:num_fields*3])
        
        if use_same_voice:
            voice_list = [global_voice] * num_fields
        
        for progress, audio_list, status in generate_batch_turbo_speech(text_list, voice_list, use_same_voice, bgmusic_list):
            outputs = [progress, status, audio_list]
            
            has_audio = any(audio is not None for audio in audio_list)
            outputs.append(gr.update(visible=has_audio))
            
            for i in range(num_fields):
                outputs.append(audio_list[i])
                outputs.append(gr.update(visible=audio_list[i] is not None))
            
            yield outputs
    
    def download_all_handler(audio_list):
        """Create ZIP file with all generated audios."""
        if not audio_list or all(audio is None for audio in audio_list):
            return None
        zip_path = create_batch_zip(audio_list)
        return zip_path if zip_path else None
    
    batch_inputs = [batch_components['use_same_voice'], batch_components['global_voice']] + \
                   batch_components['text_inputs'] + batch_components['voice_inputs'] + \
                   batch_components['bgmusic_inputs']
    
    batch_outputs_flat = [
        batch_components['progress_bar'], 
        batch_components['status_box'],
        batch_audio_state,
        batch_components['download_all_btn']
    ]
    for audio in batch_components['audio_outputs']:
        batch_outputs_flat.extend([audio, audio])
    
    batch_components['generate_batch_btn'].click(
        fn=batch_generate_wrapper,
        inputs=batch_inputs,
        outputs=batch_outputs_flat
    )
    
    batch_components['download_all_btn'].click(
        fn=download_all_handler,
        inputs=[batch_audio_state],
        outputs=[batch_components['download_all_file']]
    ).then(
        fn=lambda: gr.update(visible=True),
        outputs=[batch_components['download_all_file']]
    )
    
    # ---------------------------
    # Event Handlers - Cinematic Mixer Tab
    # ---------------------------
    def mix_audio_handler(voice_file, mood, music_volume, enable_ducking):
        """Handle audio mixing with progress updates."""
        if voice_file is None:
            return None, "❌ Please upload a voice file first"
        
        try:
            yield None, "🎵 Mixing audio with cinematic music..."
            
            output_path = mix_audio_with_music(
                voice_path=voice_file,
                mood=mood,
                music_volume=music_volume,
                enable_ducking=enable_ducking
            )
            
            if output_path:
                yield output_path, f"✅ Success! Mixed audio saved to: {output_path}"
            else:
                yield None, "❌ Failed to mix audio. Check that FFmpeg is installed and music files are available."
                
        except Exception as e:
            yield None, f"❌ Error: {str(e)}"
    
    mixer_components['mix_btn'].click(
        fn=mix_audio_handler,
        inputs=[
            mixer_components['voice_file'],
            mixer_components['mood_select'],
            mixer_components['volume_slider'],
            mixer_components['ducking_checkbox']
        ],
        outputs=[
            mixer_components['output_audio'],
            mixer_components['status_box']
        ]
    )


if __name__ == "__main__":
    demo.queue(
        max_size=50,
        default_concurrency_limit=1,
    ).launch(inbrowser=True, show_error=True)
