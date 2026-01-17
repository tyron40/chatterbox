# Batch generation handler - CORRECT VERSION
def batch_generate_wrapper(use_same_voice, global_voice, *text_and_voice_inputs):
    """Wrapper to handle batch generation with proper input parsing."""
    # Split inputs into texts and voices
    num_fields = 50
    text_list = list(text_and_voice_inputs[:num_fields])
    voice_list = list(text_and_voice_inputs[num_fields:])
    
    # If using same voice, create a list with the global voice repeated
    if use_same_voice:
        voice_list = [global_voice] * num_fields
    
    # Generate batch
    for progress, audio_list, status in generate_batch_turbo_speech(text_list, voice_list, use_same_voice):
        # Prepare outputs: progress, status, and audio outputs
        outputs = [progress, status]
        
        # Add audio outputs - each audio component needs value and visible update
        for i in range(num_fields):
            if audio_list[i] is not None:
                # Audio was generated - set value and make visible
                outputs.append(audio_list[i])
                outputs.append(gr.update(visible=True))
            else:
                # No audio - keep hidden
                outputs.append(None)
                outputs.append(gr.update(visible=False))
        
        yield outputs
