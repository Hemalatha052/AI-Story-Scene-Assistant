import os
import json
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

st.set_page_config(
    page_title="AI Story & Scene Assistant",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 AI Story & Scene Assistant")
st.caption("Turn a simple story idea into a structured cinematic storyboard.")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY is not set.")
    st.stop()

client = genai.Client(api_key=api_key)

with st.sidebar:
    st.header("Storyboard Settings")

    genre = st.selectbox(
        "Genre",
        ["Drama", "Action", "Horror", "Romance", "Mystery", "Sci-Fi"]
    )

    style = st.selectbox(
        "Visual Style",
        ["Cinematic", "Realistic", "Dark", "Fantasy", "Documentary"]
    )

    scene_count = st.slider(
        "Number of scenes",
        2,
        6
        3
        
    )

story = st.text_area(
    "Enter your story idea",
    placeholder="Example: A girl enters an old railway station at midnight and hears a strange sound.",
    height=150
)

generate = st.button(
    "🎬 Generate Storyboard",
    type="primary"
)

if generate:

    if not story.strip():
        st.warning("Please enter a story idea first.")
        st.stop()

    prompt = f"""
You are an AI filmmaking assistant.

Convert the following story into a {scene_count}-scene storyboard.

Genre: {genre}
Visual style: {style}

For every scene provide:
- Scene number
- Title
- Location
- Time
- Characters
- Action
- Mood
- Camera shot
- Image generation prompt

Keep the scenes logically connected to the original story.

Return ONLY valid JSON in this structure:

{{
  "project_title": "short title",
  "scenes": [
    {{
      "scene_number": 1,
      "title": "scene title",
      "location": "location",
      "time": "time",
      "characters": ["character 1"],
      "action": "what happens",
      "mood": "mood",
      "camera_shot": "camera shot",
      "image_prompt": "cinematic image prompt"
    }}
  ]
}}

Story:
{story}
"""

    with st.spinner("AI is creating your storyboard..."):

        try:

            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )

            raw = response.text.strip()

            raw = raw.replace("```json", "")
            raw = raw.replace("```", "")
            raw = raw.strip()

            data = json.loads(raw)

            st.success("Storyboard generated successfully!")

            st.header(
                f"🎬 {data.get('project_title', 'Untitled Story')}"
            )

            for scene in data.get("scenes", []):

                with st.container(border=True):

                    st.subheader(
                        f"Scene {scene.get('scene_number')}: "
                        f"{scene.get('title')}"
                    )

                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown(
                            f"**📍 Location:** {scene.get('location')}"
                        )
                        st.markdown(
                            f"**🕒 Time:** {scene.get('time')}"
                        )
                        st.markdown(
                            f"**👥 Characters:** "
                            f"{', '.join(scene.get('characters', []))}"
                        )
                        st.markdown(
                            f"**🎭 Mood:** {scene.get('mood')}"
                        )

                    with col2:
                        st.markdown(
                            f"**🎥 Camera:** "
                            f"{scene.get('camera_shot')}"
                        )
                        st.markdown(
                            f"**🎬 Action:** "
                            f"{scene.get('action')}"
                        )

                    st.markdown(
                        "**🎨 Image Generation Prompt**"
                    )

                    st.info(
                        scene.get("image_prompt", "")
                    )

        except json.JSONDecodeError:
            st.error(
                "The AI returned an unexpected format. Please try again."
            )

        except Exception as e:
            st.error(
                f"Something went wrong: {e}"
            )

st.divider()

st.markdown("""
### 💡 Example

**Story:** A scientist discovers an unknown planet
and receives a mysterious signal.

The assistant converts the idea into connected scenes
with locations, actions, moods, camera directions,
and image-generation prompts.
""")