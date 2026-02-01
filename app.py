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
    delete_voice,
    bulk_clone_voices
)
from modules.generation_functions import (
    generate_speech,
    generate_multilingual_speech,
    convert_voice,
    generate_turbo_speech,
    generate_batch_speech
)
from modules.ai_text_generator import (
    generate_single_text,
    generate_all_texts
)

# Import UI components
from modules.ui_components import (
    create_header,
    create_tts_tab,
    create_multilingual_tab,
    create_voice_conversion_tab,
    create_clone_voice_tab,
    create_batch_generation_tab,
    create_turbo_tab
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
with gr.Blocks(title="Chatterbox TTS Enhanced") as demo:
    # State variables
    tts_model_state = gr.State(None)
    vc_model_state = gr.State(None)
    mtl_model_state = gr.State(None)
    
    # Header
    create_header()
    
    # Create tabs
    with gr.Tab("⚡ Turbo TTS"):
        turbo_components = create_turbo_tab()

    with gr.Tab("🎤 TTS Main (English)"):
        tts_components = create_tts_tab()
    
    with gr.Tab("🌍 Multilingual TTS"):
        mtl_components = create_multilingual_tab()
    
    with gr.Tab("🔄 Voice Conversion"):
        vc_components = create_voice_conversion_tab()
    
    with gr.Tab("🧬 Clone Voice"):
        clone_components = create_clone_voice_tab()

    with gr.Tab("📦 Batch Generation"):
        batch_components = create_batch_generation_tab()
    
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
    # Using the same pattern as HuggingFace demo
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
    turbo_components['btn_clear_throat'].click(
        fn=None,
        inputs=[turbo_components['btn_clear_throat'], turbo_components['text']],
        outputs=turbo_components['text'],
        js=INSERT_TAG_JS
    )
    
    turbo_components['btn_sigh'].click(
        fn=None,
        inputs=[turbo_components['btn_sigh'], turbo_components['text']],
        outputs=turbo_components['text'],
        js=INSERT_TAG_JS
    )
    
    turbo_components['btn_shush'].click(
        fn=None,
        inputs=[turbo_components['btn_shush'], turbo_components['text']],
        outputs=turbo_components['text'],
        js=INSERT_TAG_JS
    )
    
    turbo_components['btn_cough'].click(
        fn=None,
        inputs=[turbo_components['btn_cough'], turbo_components['text']],
        outputs=turbo_components['text'],
        js=INSERT_TAG_JS
    )
    
    turbo_components['btn_groan'].click(
        fn=None,
        inputs=[turbo_components['btn_groan'], turbo_components['text']],
        outputs=turbo_components['text'],
        js=INSERT_TAG_JS
    )
    
    turbo_components['btn_sniff'].click(
        fn=None,
        inputs=[turbo_components['btn_sniff'], turbo_components['text']],
        outputs=turbo_components['text'],
        js=INSERT_TAG_JS
    )
    
    turbo_components['btn_gasp'].click(
        fn=None,
        inputs=[turbo_components['btn_gasp'], turbo_components['text']],
        outputs=turbo_components['text'],
        js=INSERT_TAG_JS
    )
    
    turbo_components['btn_chuckle'].click(
        fn=None,
        inputs=[turbo_components['btn_chuckle'], turbo_components['text']],
        outputs=turbo_components['text'],
        js=INSERT_TAG_JS
    )
    
    turbo_components['btn_laugh'].click(
        fn=None,
        inputs=[turbo_components['btn_laugh'], turbo_components['text']],
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
        
        # Remove gender symbols if present
        clean_name = voice_name.replace(" ♂️", "").replace(" ♀️", "")
        
        # Check if it's a default voice string like "Default (English)"
        if clean_name.startswith("Default ("):
            # Extract language name
            lang_name = clean_name.split("(")[1].split(")")[0]
            # Find code
            for code, name in SUPPORTED_LANGUAGES.items():
                if name == lang_name:
                    return LANGUAGE_CONFIG.get(code, {}).get("audio")
        
        # Try different possible names with gender suffixes
        from modules.voice_manager import VOICES
        possible_names = [
            clean_name,
            f"{clean_name}_male",
            f"{clean_name}_female"
        ]
        
        # Check cloned voices
        for name in possible_names:
            if name in VOICES["samples"]:
                return VOICES["samples"][name]
        
        # Try finding it with language suffixes if not found directly
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
    # Update all voice dropdowns when cloning
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
    ).then(
        fn=lambda: gr.update(choices=get_voices_for_language("en")),
        outputs=[batch_components['voice_for_all']]
    ).then(
        fn=lambda: [gr.update(choices=get_voices_for_language("en"))] * 100,
        outputs=batch_components['batch_voice_selects']
    )
    
    # Delete voice functionality in Clone Voice tab
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
    
    # Bulk clone voices functionality
    clone_components['bulk_clone_btn'].click(
        fn=bulk_clone_voices,
        inputs=[
            clone_components['bulk_audio_files'],
            clone_components['bulk_voice_names'],
            clone_components['bulk_voice_gender'],
            clone_components['bulk_voice_language']
        ],
        outputs=[clone_components['bulk_clone_status']]
    ).then(
        fn=lambda: gr.update(choices=get_voices_for_language("en")),
        outputs=[tts_components['voice_select']]
    ).then(
        fn=lambda: gr.update(choices=get_voices_for_language("en")),
        outputs=[turbo_components['voice_select']]
    ).then(
        fn=lambda lang: gr.update(choices=get_voices_for_language(lang)),
        inputs=[mtl_components['language_select']],
        outputs=[mtl_components['voice_select']]
    ).then(
        fn=lambda: gr.update(choices=["None"] + get_all_voices_with_gender()),
        outputs=[vc_components['target_voice_select']]
    ).then(
        fn=lambda: gr.update(choices=get_voices_for_language("en")),
        outputs=[batch_components['voice_for_all']]
    ).then(
        fn=lambda: [gr.update(choices=get_voices_for_language("en"))] * 100,
        outputs=batch_components['batch_voice_selects']
    ).then(
        fn=lambda: "\n".join(load_voices()) if load_voices() else "No voices cloned yet",
        outputs=[clone_components['current_voices_display']]
    ).then(
        fn=lambda: gr.update(choices=["None"] + get_all_voices_with_gender(), value="None"),
        outputs=[clone_components['voice_to_delete']]
    )

    # ---------------------------
    # Event Handlers - Batch Generation Tab
    # ---------------------------
    # Function to handle batch generation with individual text fields
    def process_batch_generation(use_same_voice, voice_for_all, model_type, language_select, *inputs):
        # Split inputs: first 100 are text inputs, next 100 are voice selections
        text_inputs = inputs[:100]
        voice_inputs = inputs[100:200] if len(inputs) >= 200 else []
        
        # Filter out empty text inputs and get their indices
        valid_texts = []
        valid_indices = []
        for i, text in enumerate(text_inputs):
            if text and text.strip():
                valid_texts.append(text)
                valid_indices.append(i)
        
        if not valid_texts:
            return [0] + [None] * 100 + ["No valid text inputs found. Please enter at least one text."]
        
        # Collect voice selections for each valid text
        voices = []
        if use_same_voice:
            # Use the same voice for all texts
            voices = [voice_for_all] * len(valid_texts)
        else:
            # Use individual voice selections from the voice dropdowns
            for idx in valid_indices:
                if voice_inputs and idx < len(voice_inputs):
                    voice = voice_inputs[idx]
                else:
                    # Fallback to first available voice if voice input is missing
                    available_voices = get_voices_for_language("en")
                    voice = available_voices[0] if available_voices else None
                voices.append(voice)
        
        # Call the batch generation function with the collected texts and voices
        # The generate_batch_speech function is a generator that yields progress updates
        progress = 0
        status = "Starting batch generation..."
        audio_outputs = [None] * 100
        
        # Pass individual texts and voices to generate_batch_speech
        for progress_update, audio_data, status_update, audio_index in generate_batch_speech(valid_texts, voices, model_type, language_select):
            progress = progress_update
            status = status_update
            
            # If audio data is returned, update the corresponding audio output
            if audio_data is not None and audio_index is not None:
                # Map back to the original index
                if audio_index < len(valid_indices):
                    original_index = valid_indices[audio_index]
                    audio_outputs[original_index] = audio_data
        
        # Return progress, audio outputs for all slots, and status
        return [progress] + audio_outputs + [status]
                    
    # Connect the generate button to the processing function
    # Include both text inputs and voice selections
    batch_components['generate_all_btn'].click(
        fn=process_batch_generation,
        inputs=[
            batch_components['use_same_voice'],
            batch_components['voice_for_all'],
            batch_components['batch_model_type'],
            batch_components['batch_language_select'],
            *batch_components['batch_inputs'],
            *batch_components['batch_voice_selects']
        ],
        outputs=[
            batch_components['progress_bar'],
            *batch_components['batch_audio_outputs'],
            batch_components['status_box']
        ]
    )
                    
    # ---------------------------
    # Event Handlers - AI Text Generation (Batch Tab)
    # ---------------------------
    # Function to generate all texts using AI
    def process_generate_all_texts(topic, duration_minutes, num_texts):
        """Generate multiple texts using AI and update all text fields."""
        try:
            if not topic or not topic.strip():
                return [gr.update()] * 100 + ["❌ Error: Please enter a topic for AI generation."]
            
            # Initialize all outputs as no-update
            text_updates = [gr.update()] * 100
            
            # Generate texts using AI (duration is always in minutes)
            for index, generated_text, status in generate_all_texts(topic, duration_minutes, "minutes", int(num_texts)):
                # Update the specific text field
                text_updates[index] = gr.update(value=generated_text)
                
            final_status = f"✅ Successfully generated {int(num_texts)} unique texts about: {topic}"
            return text_updates + [final_status]
            
        except Exception as e:
            error_status = f"❌ Error: {str(e)}\n\nMake sure OPENAI_API_KEY environment variable is set."
            return [gr.update()] * 100 + [error_status]
    
    # Connect "Generate All Texts" button
    batch_components['generate_all_texts_btn'].click(
        fn=process_generate_all_texts,
        inputs=[
            batch_components['ai_topic'],
            batch_components['ai_duration_minutes'],
            batch_components['ai_num_texts']
        ],
        outputs=batch_components['batch_inputs'] + [batch_components['ai_status']]
    )
    
    # Function to generate single text for individual button
    def process_generate_single_text(topic, duration_minutes, field_index):
        """Generate a single text using AI for a specific field."""
        try:
            if not topic or not topic.strip():
                return gr.update(), "❌ Error: Please enter a topic for AI generation."
            
            # Generate unique text for this field (duration is always in minutes)
            generated_text = generate_single_text(topic, duration_minutes, "minutes", variation_number=field_index+1)
            
            status = f"✅ Generated text for field {field_index+1}"
            return gr.update(value=generated_text), status
            
        except Exception as e:
            error_status = f"❌ Error: {str(e)}\n\nMake sure OPENAI_API_KEY environment variable is set."
            return gr.update(), error_status
    
    # Connect individual generate buttons (one for each of the 100 fields)
    for i, gen_btn in enumerate(batch_components['batch_generate_btns']):
        gen_btn.click(
            fn=lambda topic, dur_min, idx=i: process_generate_single_text(topic, dur_min, idx),
            inputs=[
                batch_components['ai_topic'],
                batch_components['ai_duration_minutes']
            ],
            outputs=[batch_components['batch_inputs'][i], batch_components['ai_status']]
        )
                
    # Add a function to create a zip file with all generated audio files
    def create_download_all_button():
        import os
        import zipfile
        from datetime import datetime
        
        # Create a button to download all generated audio files
        download_all_btn = gr.Button("📦 Download All Audio Files", variant="secondary")
        
        def download_all_audio():
            # Create a zip file with all generated audio files
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            zip_filename = f"batch_output/all_audio_{timestamp}.zip"
            
            # Ensure the directory exists
            os.makedirs("batch_output", exist_ok=True)
            
            # Find the most recent batch output directory
            batch_dirs = [d for d in os.listdir("batch_output") if d.startswith("batch_")]
            if not batch_dirs:
                return None, "No generated audio files found."
            
            # Sort by creation time (newest first)
            batch_dirs.sort(reverse=True)
            latest_batch_dir = os.path.join("batch_output", batch_dirs[0])
            
            # Create a zip file with all audio files
            with zipfile.ZipFile(zip_filename, "w") as zipf:
                for file in os.listdir(latest_batch_dir):
                    if file.endswith(".wav"):
                        zipf.write(os.path.join(latest_batch_dir, file), file)
            
            return zip_filename, f"All audio files downloaded as {zip_filename}"
        
        # Add the download button to the UI
        download_all_btn.click(
            fn=download_all_audio,
            inputs=[],
            outputs=[gr.File(label="Download"), gr.Textbox(label="Status")]
        )
        
        return download_all_btn
    
    # Add the download all button to the batch generation tab
    with gr.Row():
        create_download_all_button()
                        

if __name__ == "__main__":
    demo.queue(
        max_size=50,
        default_concurrency_limit=1,
    ).launch(
        inbrowser=True, 
        show_error=True,
        theme=gr.themes.Soft(),
        css=CUSTOM_CSS
    )
