from controllers import ScriptController
from pathlib import Path
import json

# Controllers
script_controller = ScriptController()

# Create content directory
base_content_path = Path("content")
base_content_path.mkdir(exist_ok=True)  

system_input = "Based on the reddit story you are given, create a more fun and captivating version. Your output should be audio ready, meaning it should not use acronyms or any special characters. Don't include the title and try to make the stories 1 minute long"
user_input = "This happened yesterday. I was at the mall with two of my friends, both white and girls. We were shopping at Macy's when two Asian guys walked up to us and started flirting directly with my friends. One of friends who we can call Kate is in a relationship. My second friend who we'll call Emily and I are the only single ones. The guys proceeded to ask Kate and Emily to hangout sometimes and even asked to exchange numbers. Kate informed both guys that she was already taken and told them that I'm single and free to mingle. The guy who apparently called dibs on Kate gave me an awkward look and said Yeeeea I don't think that would work out. Curious I asked what he meant by that. What he said next didn't shock me. He told me that he's looking for someone who would fit the beauty standard and would be good enough to maybe be introduced to his parents. I chuckled and said Well that's okay. I'm sure your buddy down there isn't big enough for me anyway. I pointed at his private area. The two Asian guys and my friends were all stunned by my response. I told the girls to meet me in the footwear area when they were done with the guys and walked off. Later as we were driving home Kate told me that my response was sort of immature and stereotyping and not all Asian guys have small areas. I told her that I was going to just stand there and allow the prick to insult me. She said that I can't expect every guy to find me beautiful and attractive. I told her that they don't have to find me beautiful but to stand there and insult me and make rude comments like that is something I will never stand for. The rest of the ride home was quiet. Was I wrong?"
video_title = "AITA for telling an Asian man that his area is probably not big enough for me to enjoy anyway after he stated that I'm not a beauty standard"
script_model = "gpt-4o-mini"
audio_provider = "openai"

details = {
    "video_title": video_title,
    "system_input": system_input,
    "user_input": user_input,
    "script_model": script_model,
    "audio_provider": audio_provider
}

# Define project path and create if necessary
project_path = base_content_path / video_title.replace(' ', '_')

project_path.mkdir(parents=True, exist_ok=True)
print(f"Project created at: {project_path}")

details_path = project_path / "details.json"
script_path = project_path / "script.txt"
audio_path = project_path / "audio.mp3"

# Write details to JSON file
with open(details_path, 'w') as details_file:
    json.dump(details, details_file, indent=2, ensure_ascii=False)

# Generate script
script = script_controller.generate_script(system_input, user_input, script_model, script_path)
print(f"Script generated at: {script_path}")

# User confirmation loop
while True:
    res = input("Please confirm the script is correct before continuing (y/exit): ")
    if res.lower() == "y":
        break
    elif res.lower() == "exit":
        exit()
    else:
        print("Invalid input. Type 'y' to continue or 'exit' to exit the program.")

# Generate audio
script_controller.generate_audio(script, audio_provider, audio_path)
print(f"Audio generated at: {audio_path}")
