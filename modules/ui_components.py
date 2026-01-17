"""
UI Components for Chatterbox TTS Enhanced
Contains function to create each tab's UI layout
"""
import gradio as gr
from .config import LANGUAGE_CONFIG, SUPPORTED_LANGUAGES
from .voice_manager import load_voices, get_voices_for_language, get_all_voices_with_gender


def create_header():
    """Create the application header."""
    gr.HTML("""
        <h1 style="font-size: 2.5em; margin-bottom: 0.5rem; text-align: center;">⚡ Chatterbox Turbo TTS (Supports 23 Languages) </h1>
        <p style='text-align: center; font-size: 1.2em; color: #666;'>High-Quality Voice Cloning, Text-to-Speech & Voice Conversion</p>
        
        <!-- Channel Section -->
        <div style="display: flex; justify-content: center; align-items: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); 
                    margin: 1.5rem auto; max-width: 700px;">
            <div style="display: flex; align-items: center; gap: 1.5rem; width: 100%;">
                <img src="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAkACQAAD..." alt="Channel Logo" style="width: 60px; height: 60px; border-radius: 50%; border: 2px solid #ccc; object-fit: cover;">
            <div style="text-align: left; flex-grow: 1; color: white;">
                <h3 style="margin: 0; font-size: 1.5rem; font-weight: 600;">Chatterbox by The Oracle Guy</h3>
                <p style="font-size: 1rem; margin-top: 0.5rem; opacity: 0.9;">Subscribe for more such future releases!</p>
            </div>
            <a href="https://www.youtube.com/@theoracleguy_AI?sub_confirmation=1" target="_blank"
                style="background-color: #E74C3C; color: white; padding: 10px 20px; font-size: 1.1rem;
                        text-decoration: none; border-radius: 4px; font-weight: 600; display: inline-flex;
                        align-items: center; gap: 12px; box-shadow: 0 4px 8px rgba(255, 0, 0, 0.2);
                        transition: background-color 0.3s, box-shadow 0.3s;">
                Subscribe
            </a>
        </div>
    </div>
    """)


def create_tts_tab():
    """Create the UI for Text-to-Speech tab."""
    with gr.Row():
        with gr.Column():
            text = gr.Textbox(
                value="Hey there! I'm The Oracle Guy, and I'm unlocking the secrets of AI!",
                label="Text to synthesize (unlimited length - smart chunking enabled)",
                max_lines=10,
                placeholder="Enter text to convert to speech..."
            )
            
            # Get available voices and set a valid default
            available_voices = get_voices_for_language("en")
            default_voice = available_voices[0] if available_voices else None
            
            voice_select_tts = gr.Dropdown(
                label="Select Voice",
                choices=available_voices,
                value=default_voice,
                info="Select a cloned voice or use default"
            )
            
            preview_audio_tts = gr.Audio(label="Voice Preview", interactive=False, visible=True)
            
            gr.Markdown("**Language:** English only for this tab. Use Multilingual TTS for other languages.")
            
            exaggeration = gr.Slider(0.25, 2, step=.05, label="Exaggeration (Neutral = 0.5)", value=.5)
            cfg_weight = gr.Slider(0.0, 1, step=.05, label="CFG/Pace", value=0.5)

            with gr.Accordion("⚙️ Advanced Options", open=False):
                seed_num = gr.Number(value=0, label="Random seed (0 for random)")
                temp = gr.Slider(0.05, 5, step=.05, label="Temperature", value=.8)
                min_p = gr.Slider(0.00, 1.00, step=0.01, label="min_p (0.00 disables)", value=0.05)
                top_p = gr.Slider(0.00, 1.00, step=0.01, label="top_p (1.0 disables)", value=1.00)
                repetition_penalty = gr.Slider(1.00, 2.00, step=0.1, label="Repetition Penalty", value=1.2)

            generate_btn = gr.Button("🎙️ Generate Speech", variant="primary", size="lg")

        with gr.Column():
            progress_bar_tts = gr.Slider(label="Progress", minimum=0, maximum=100, value=0, interactive=False)
            status_box_tts = gr.Textbox(label="Status", value="Ready to generate...", lines=3, interactive=False)
            audio_output_tts = gr.Audio(label="Generated Audio", autoplay=True)

    return {
        "text": text,
        "voice_select": voice_select_tts,
        "exaggeration": exaggeration,
        "cfg_weight": cfg_weight,
        "seed_num": seed_num,
        "temp": temp,
        "min_p": min_p,
        "top_p": top_p,
        "repetition_penalty": repetition_penalty,
        "generate_btn": generate_btn,
        "progress_bar": progress_bar_tts,
        "status_box": status_box_tts,
        "audio_output": audio_output_tts,
        "preview_audio": preview_audio_tts
    }


def create_multilingual_tab():
    """Create the UI for Multilingual TTS tab."""
    with gr.Row():
        with gr.Column():
            text_mtl = gr.Textbox(
                value=LANGUAGE_CONFIG["fr"]["text"],
                label="Text to synthesize (unlimited length - smart chunking enabled)",
                max_lines=5,
                placeholder="Enter text in any supported language..."
            )
            
            language_select_mtl = gr.Dropdown(
                label="Language",
                choices=[(f"{name} ({code})", code) for code, name in sorted(SUPPORTED_LANGUAGES.items())],
                value="fr",
                info="Select the language of your text"
            )
            
            voice_select_mtl = gr.Dropdown(
                label="Select Voice",
                choices=get_voices_for_language("fr"),
                value=f"Default ({SUPPORTED_LANGUAGES['fr']})",
                info="Select a voice for this language"
            )
            
            sample_audio_mtl = gr.Audio(
                label="Voice Preview",
                value=LANGUAGE_CONFIG["fr"]["audio"],
                interactive=False
            )
            
            exaggeration_mtl = gr.Slider(0.25, 2, step=.05, label="Exaggeration (Neutral = 0.5)", value=.5)
            cfg_weight_mtl = gr.Slider(0.0, 1, step=.05, label="CFG/Pace", value=0.5)

            with gr.Accordion("⚙️ Advanced Options", open=False):
                seed_num_mtl = gr.Number(value=0, label="Random seed (0 for random)")
                temp_mtl = gr.Slider(0.05, 5, step=.05, label="Temperature", value=.8)

            generate_btn_mtl = gr.Button("🎙️ Generate Speech", variant="primary", size="lg")

        with gr.Column():
            progress_bar_mtl = gr.Slider(label="Progress", minimum=0, maximum=100, value=0, interactive=False)
            status_box_mtl = gr.Textbox(label="Status", value="Ready to generate...", lines=3, interactive=False)
            audio_output_mtl = gr.Audio(label="Generated Audio", autoplay=True)
            
            gr.Markdown(f"""
            ### Supported Languages ({len(SUPPORTED_LANGUAGES)}):
            {', '.join([f"**{name}**" for name in sorted(SUPPORTED_LANGUAGES.values())])}
            """)

    return {
        "text": text_mtl,
        "language_select": language_select_mtl,
        "voice_select": voice_select_mtl,
        "sample_audio": sample_audio_mtl,
        "exaggeration": exaggeration_mtl,
        "cfg_weight": cfg_weight_mtl,
        "seed_num": seed_num_mtl,
        "temp": temp_mtl,
        "generate_btn": generate_btn_mtl,
        "progress_bar": progress_bar_mtl,
        "status_box": status_box_mtl,
        "audio_output": audio_output_mtl
    }


def create_voice_conversion_tab():
    """Create the UI for Voice Conversion tab."""
    with gr.Row():
        with gr.Column():
            gr.Markdown("""
            ### Convert any voice to another!
            Upload an audio file and select a target voice to convert it.
            """)
            
            input_audio_vc = gr.Audio(
                label="Input Audio",
                sources=["upload", "microphone"],
                type="filepath"
            )
            
            target_voice_select = gr.Dropdown(
                label="Target Voice",
                choices=["None"] + get_all_voices_with_gender(),
                value="None",
                info="Select target voice or use default"
            )
            
            preview_audio_vc = gr.Audio(label="Target Voice Preview", interactive=False, visible=True)
            
            convert_btn = gr.Button("🔄 Convert Voice", variant="primary", size="lg")

        with gr.Column():
            progress_bar_vc = gr.Slider(label="Progress", minimum=0, maximum=100, value=0, interactive=False)
            status_box_vc = gr.Textbox(label="Status", value="Ready to convert...", lines=3, interactive=False)
            audio_output_vc = gr.Audio(label="Converted Audio", autoplay=True)

    return {
        "input_audio": input_audio_vc,
        "target_voice_select": target_voice_select,
        "preview_audio": preview_audio_vc,
        "convert_btn": convert_btn,
        "progress_bar": progress_bar_vc,
        "status_box": status_box_vc,
        "audio_output": audio_output_vc
    }


def create_clone_voice_tab():
    """Create the UI for Clone Voice tab."""
    with gr.Row():
        with gr.Column():
            gr.Markdown("""
            ### Clone any voice instantly!
            
            **How to clone:**
            1. Upload or record a clear audio sample (5-30 seconds)
            2. Name your voice and select gender
            3. Select the language
            4. Click "Clone Voice"
            5. Use it in any tab!
            
            **Tips for best results:**
            - Use clear, high-quality audio
            - Avoid background noise
            - 10-20 seconds is ideal
            - Multiple sentences work better
            """)
            
            new_voice_name = gr.Textbox(
                label="Voice Name",
                placeholder="e.g., Amitabh, Priyanka, Morgan..."
            )
            
            voice_gender = gr.Radio(
                label="Gender",
                choices=[("Male ♂️", "male"), ("Female ♀️", "female")],
                value="male",
                info="Select the gender for display purposes"
            )
            
            voice_language = gr.Dropdown(
                label="Voice Language",
                choices=[(f"{name} ({code})", code) for code, name in sorted(SUPPORTED_LANGUAGES.items())],
                value="en",
                info="Select the language of the voice sample"
            )
            
            ref_audio_input = gr.Audio(
                label="Reference Audio Sample",
                sources=["upload", "microphone"],
                type="filepath"
            )
            clone_btn = gr.Button("🧬 Clone Voice", variant="primary", size="lg")
            
        with gr.Column():
            clone_status = gr.Textbox(label="Cloning Status", lines=3)
            gr.Markdown("""
            ### Your Cloned Voices:
            After cloning, your voice will appear in all tabs.
            
            **Voice Storage:**
            - Saved in `voice_samples` folder
            - Manage from this tab
            - Delete when no longer needed
            
            **Current Voices:**
            """)
            
            # Load current voices for initial display
            current_voices = load_voices()
            voices_display_text = "\n".join(current_voices) if current_voices else "No voices cloned yet"
            
            current_voices_display = gr.Textbox(
                value=voices_display_text,
                label="Cloned Voices",
                lines=5,
                interactive=False
            )
            
            with gr.Row():
                voice_to_delete = gr.Dropdown(
                    label="Select Voice to Delete",
                    choices=["None"] + current_voices,
                    value="None",
                    info="Select a cloned voice to delete"
                )
                delete_btn_clone = gr.Button("🗑️ Delete Voice", variant="secondary", size="sm")
            
            delete_status_clone = gr.Textbox(label="Delete Status", lines=2)

    return {
        "new_voice_name": new_voice_name,
        "voice_gender": voice_gender,
        "voice_language": voice_language,
        "ref_audio_input": ref_audio_input,
        "clone_btn": clone_btn,
        "clone_status": clone_status,
        "current_voices_display": current_voices_display,
        "voice_to_delete": voice_to_delete,
        "delete_btn": delete_btn_clone,
        "delete_status": delete_status_clone
    }


def create_turbo_tab():
    """Create the UI for Turbo TTS tab."""
    with gr.Row():
        with gr.Column():
            gr.Markdown("""
            ### ⚡ Chatterbox-Turbo - Ultra-Fast TTS
            
            **What's New:**
            - **350M parameters** - Streamlined architecture
            - **10x faster** - One-step decoder (vs 10 steps)
            - **Native paralinguistic tags** - Add realistic emotions!
            - **Low-latency** - Perfect for voice agents
            
            **Available Paralinguistic Tags:**
            `[clear throat]` `[sigh]` `[shush]` `[cough]` `[groan]` 
            `[sniff]` `[gasp]` `[chuckle]` `[laugh]`
            
            **Example:**
            *"Hi there, Sarah here from MochaFone calling you back [chuckle], have you got one minute to chat about the billing issue?"*
            """)
            
            text_turbo = gr.Textbox(
                value="Hi there! [chuckle] I'm The Oracle Guy, and I'm unlocking the secrets of AI with Chatterbox-Turbo!",
                label="Text to synthesize (unlimited length - smart chunking enabled)",
                max_lines=5,
                placeholder="Enter text with optional paralinguistic tags like [chuckle], [laugh], [sigh]...",
                elem_id="turbo_textbox"
            )
            
            # Paralinguistic tag buttons with custom styling
            gr.Markdown("**Quick Insert Tags:**")
            with gr.Row(elem_classes="tag-container"):
                btn_clear_throat = gr.Button("[clear throat]", size="sm", elem_classes="tag-btn")
                btn_sigh = gr.Button("[sigh]", size="sm", elem_classes="tag-btn")
                btn_shush = gr.Button("[shush]", size="sm", elem_classes="tag-btn")
                btn_cough = gr.Button("[cough]", size="sm", elem_classes="tag-btn")
                btn_groan = gr.Button("[groan]", size="sm", elem_classes="tag-btn")
            
            with gr.Row(elem_classes="tag-container"):
                btn_sniff = gr.Button("[sniff]", size="sm", elem_classes="tag-btn")
                btn_gasp = gr.Button("[gasp]", size="sm", elem_classes="tag-btn")
                btn_chuckle = gr.Button("[chuckle]", size="sm", elem_classes="tag-btn")
                btn_laugh = gr.Button("[laugh]", size="sm", elem_classes="tag-btn")
            
            # Get available voices and set a valid default
            available_voices = get_voices_for_language("en")
            default_voice = available_voices[0] if available_voices else None
            
            voice_select_turbo = gr.Dropdown(
                label="Select Voice (Required for Turbo)",
                choices=available_voices,
                value=default_voice,
                info="Turbo requires a reference voice clip for cloning"
            )
            
            preview_audio_turbo = gr.Audio(label="Voice Preview", interactive=False, visible=True)
            
            gr.Markdown("**Language:** English only. **Note:** Turbo model requires a voice reference.")

            
            generate_btn_turbo = gr.Button("⚡ Generate Speech (Turbo)", variant="primary", size="lg")

        with gr.Column():
            progress_bar_turbo = gr.Slider(label="Progress", minimum=0, maximum=100, value=0, interactive=False)
            status_box_turbo = gr.Textbox(label="Status", value="Ready to generate...", lines=3, interactive=False)
            audio_output_turbo = gr.Audio(label="Generated Audio", autoplay=True)
            
            gr.Markdown("""
            ### 💡 Tips for Best Results:
            - Use paralinguistic tags naturally in your text
            - Tags work best mid-sentence or at natural pauses
            - Combine multiple tags for complex emotions
            - Perfect for narration, voice agents, and creative workflows
            - Generation is ~3x faster than standard model
            """)

    return {
        "text": text_turbo,
        "voice_select": voice_select_turbo,
        "preview_audio": preview_audio_turbo,
        "generate_btn": generate_btn_turbo,
        "progress_bar": progress_bar_turbo,
        "status_box": status_box_turbo,
        "audio_output": audio_output_turbo,
        "btn_clear_throat": btn_clear_throat,
        "btn_sigh": btn_sigh,
        "btn_shush": btn_shush,
        "btn_cough": btn_cough,
        "btn_groan": btn_groan,
        "btn_sniff": btn_sniff,
        "btn_gasp": btn_gasp,
        "btn_chuckle": btn_chuckle,
        "btn_laugh": btn_laugh
    }


def create_batch_tab():
    """Create the UI for Batch TTS tab with up to 50 text inputs."""
    
    # Create text input fields and voice dropdowns
    text_inputs = []
    voice_inputs = []
    audio_outputs = []
    bgmusic_inputs = []
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("""
            ### 📦 Batch TTS - Generate Up to 50 Audio Files
            
            **Features:**
            - Generate up to 50 different texts at once
            - Use same voice for all or select individually
            - Optional background music for each audio
            - Progress tracking for batch
            - Download all as ZIP file
            - Powered by Turbo TTS for fast processing
            
            **How to use:**
            1. Enter texts in the fields (leave empty to skip)
            2. Choose voice mode below
            3. Optionally add background music files
            4. Click "Generate All"
            5. Download each audio individually or all as ZIP
            """)
            
            # Voice mode selection
            use_same_voice = gr.Checkbox(
                label="Use same voice for all texts",
                value=True,
                info="Uncheck to select voice for each text individually"
            )
            
            # Get available voices and set a valid default
            available_voices = get_voices_for_language("en")
            default_voice = available_voices[0] if available_voices else None
            
            # Global voice selector
            global_voice = gr.Dropdown(
                label="Voice for All Texts",
                choices=available_voices,
                value=default_voice,
                info="This voice will be used when 'Use same voice' is checked"
            )
            
            generate_batch_btn = gr.Button("🎬 Generate All Audio Files", variant="primary", size="lg")
            
            progress_bar = gr.Slider(label="Overall Progress", minimum=0, maximum=100, value=0, interactive=False)
            status_box = gr.Textbox(label="Status", value="Ready to generate...", lines=2, interactive=False)
            
            download_all_btn = gr.Button("📦 Download All as ZIP", visible=False, size="lg")
            download_all_file = gr.File(label="Download ZIP", visible=False)
        
        with gr.Column(scale=2):
            gr.Markdown("### Text Inputs & Outputs")
            
            # Create 50 text input fields with corresponding voice dropdowns, bgmusic, and audio outputs
            for i in range(50):
                with gr.Row():
                    with gr.Column(scale=3):
                        text_input = gr.Textbox(
                            label=f"Text {i+1}",
                            placeholder=f"Enter text {i+1} to synthesize (leave empty to skip)...",
                            lines=2
                        )
                        text_inputs.append(text_input)
                    
                    with gr.Column(scale=2):
                        voice_input = gr.Dropdown(
                            label=f"Voice {i+1}",
                            choices=available_voices,
                            value=default_voice,
                            visible=False
                        )
                        voice_inputs.append(voice_input)
                        
                        bgmusic_input = gr.Audio(
                            label=f"Background Music {i+1} (Optional)",
                            type="filepath",
                            visible=False
                        )
                        bgmusic_inputs.append(bgmusic_input)
                
                # Audio output for this text
                audio_output = gr.Audio(
                    label=f"Generated Audio {i+1}",
                    visible=False
                )
                audio_outputs.append(audio_output)
    
    return {
        "text_inputs": text_inputs,
        "voice_inputs": voice_inputs,
        "bgmusic_inputs": bgmusic_inputs,
        "audio_outputs": audio_outputs,
        "use_same_voice": use_same_voice,
        "global_voice": global_voice,
        "generate_batch_btn": generate_batch_btn,
        "progress_bar": progress_bar,
        "status_box": status_box,
        "download_all_btn": download_all_btn,
        "download_all_file": download_all_file
    }


def create_cinematic_mixer_tab():
    """Create the UI for Cinematic Audio Mixer tab."""
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("""
            ### 🎬 Cinematic Audio Mixer
            
            **Features:**
            - Mix your generated voice with cinematic background music
            - Choose from different moods (Epic, Dramatic, Suspenseful, etc.)
            - Automatic audio ducking (music lowers when voice speaks)
            - Adjustable music volume
            - Professional audio mixing
            
            **How to use:**
            1. Upload or select a voice audio file
            2. Choose a mood/genre for background music
            3. Adjust music volume
            4. Enable/disable audio ducking
            5. Click "Mix Audio"
            """)
            
            voice_file = gr.Audio(
                label="Voice Audio File",
                type="filepath"
            )
            
            mood_select = gr.Dropdown(
                label="Music Mood/Genre",
                choices=["Epic", "Dramatic", "Suspenseful", "Emotional", "Action", "Ambient"],
                value="Epic"
            )
            
            volume_slider = gr.Slider(
                label="Music Volume",
                minimum=0.1,
                maximum=1.0,
                value=0.3,
                step=0.05
            )
            
            ducking_checkbox = gr.Checkbox(
                label="Enable Audio Ducking",
                value=True
            )
            
            mix_btn = gr.Button("🎵 Mix Audio", variant="primary", size="lg")
        
        with gr.Column():
            status_box = gr.Textbox(
                label="Status",
                value="Ready to mix audio...",
                lines=3,
                interactive=False
            )
            
            output_audio = gr.Audio(
                label="Mixed Audio Output",
                type="filepath"
            )
            
            gr.Markdown("""
            ### 💡 Tips:
            - Use lower music volume (0.2-0.4) for voice-heavy content
            - Enable ducking for better voice clarity
            - Epic/Dramatic moods work well for trailers and promos
            - Ambient/Emotional moods suit storytelling and narration
            """)
    
    return {
        "voice_file": voice_file,
        "mood_select": mood_select,
        "volume_slider": volume_slider,
        "ducking_checkbox": ducking_checkbox,
        "mix_btn": mix_btn,
        "output_audio": output_audio,
        "status_box": status_box
    }
