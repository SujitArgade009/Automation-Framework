import os
from runwayml import RunwayML, TaskFailedError

def run(prompt_text, duration=5, prompt_image=None, ratio="1280:720", model="gen4_turbo"):
    client = RunwayML(api_key=os.getenv("RUNWAYML_API_SECRET"))  # Make sure API key is set
    task = client.image_to_video.create(
        model=model,
        prompt_image=prompt_image or "",      # Optional: pass image URI or data-URI
        prompt_text=prompt_text,
        ratio=ratio,
        duration=duration,
    )
    try:
        task_output = task.wait_for_task_output()
        print("Video ready:", task_output.output[0])
        return task_output.output[0]
    except TaskFailedError as e:
        print("Generation failed:", e.task_details)
        return None
