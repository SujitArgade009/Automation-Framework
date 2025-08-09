from stages import script_gen, voice_gen, animation_gen, video_edit, upload_youtube

def main():
    script_file = script_gen.run(theme="motivation")   # Step 1
    audio_file = voice_gen.run(script_file)            # Step 2
    video_file = animation_gen.run(script_file)        # Step 3
    final_video = video_edit.run(video_file, audio_file)  # Step 4
    upload_youtube.run(final_video)                    # Step 5

if __name__ == "__main__":
    main()
