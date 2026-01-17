# Read the base file
with open('modules/ui_components_fixed.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove show_download_button from the content
content = content.replace(', show_download_button=True', '')

# Append the batch and cinematic mixer functions
additional_functions = '''

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
'''

# Write the complete file
with open('modules/ui_components.py', 'w', encoding='utf-8') as f:
    f.write(content + additional_functions)

print("File created successfully with all functions!")
