# Project Purpose

VibeVoice is an open-source research framework developed by Microsoft for advanced speech synthesis. Its primary goals are to generate expressive, long-form, and multi-speaker conversational audio (e.g., podcasts) from text.

Key capabilities include:
- **Long-form multi-speaker model:** Synthesizes speech up to 90 minutes with up to 4 distinct speakers.
- **Realtime streaming TTS model (VibeVoice-Realtime-0.5B):** Produces initial audible speech in ~300ms and supports streaming text input for single-speaker real-time speech generation, designed for low-latency.

The framework utilizes continuous speech tokenizers and a next-token diffusion framework, leveraging a Large Language Model (LLM) and a diffusion head for high-fidelity acoustic details.

**Note on Risks:** The project explicitly mentions risks and limitations related to potential misuse (deepfakes, disinformation), language limitations (English and Chinese only), and non-speech audio handling. It is intended for research and development purposes only.