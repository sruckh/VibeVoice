# 🛑 STOP — Run codemap before ANY task

```bash
codemap .                     # Project structure
codemap --deps                # How files connect
codemap --diff                # What changed vs main
codemap --diff --ref <branch> # Changes vs specific branch
```

## Required Usage

**BEFORE starting any task**, run `codemap .` first.

**ALWAYS run `codemap --deps` when:**
- User asks how something works
- Refactoring or moving code
- Tracing imports or dependencies

**ALWAYS run `codemap --diff` when:**
- Reviewing or summarizing changes
- Before committing code
- User asks what changed
- Use `--ref <branch>` when comparing against something other than main

# Project Analysis

## Structure (`codemap .`)
```
╭─────────────────────────────── VibeVoice ───────────────────────────────╮
│ Files: 55 | Size: 23.5MB                                                │
│ Top Extensions: .py (22), .md (10), .pt (7), .png (4), .gitignore (2)   │
╰─────────────────────────────────────────────────────────────────────────╯
VibeVoice
├──   .serena/ (7 files, 17.4KB)
│   ├──   memories/ (5 files, 12.0KB, all .md)
│   │   └── code_conventions   codebase_structure project_purpose    suggested_commands tech_stack         
│   └── .gitignore  project.yml 
├──   Figures/ (5 files, 2.2MB)
│   └── MOS-preference.png       VibeVoice.jpg            VibeVoice_Realtime.png   VibeVoice_logo.png       VibeVoice_logo_white.png 
├──   demo/ (14 files, 21.0MB)
│   ├──   text_examples/ (2 files, 1.9KB, all .txt)
│   │   └── 1p_abs       1p_vibevoice 
│   ├──   voices/streaming_model/ (7 files, 21.0MB, all .pt)
│   │   └── ⭐️ en-Carter_man  en-Davis_man      ⭐️ en-Emma_woman  ⭐️ en-Frank_man   ⭐️ en-Grace_woman en-Mike_man       ⭐️ in-Samuel_man  
│   ├──   web/ (2 files, 43.8KB)
│   │   └── app.py     index.html 
│   └── realtime_model_inference_from_file.py vibevoice_realtime_colab.ipynb        vibevoice_realtime_demo.py            
├──   docs/ (7.1KB)
│   └── vibevoice-realtime-0.5b.md 
├──   vibevoice/ (21 files, 243.3KB)
│   ├──   configs/ (2 files, 5.3KB, all .json)
│   │   └── qwen2.5_1.5b_64k qwen2.5_7b_32k   
│   ├──   modular/ (9 files, 117.5KB, all .py)
│   │   └── __init__                               configuration_vibevoice_streaming      modeling_vibevoice_streaming_inference modular_vibevoice_text_tokenizer       streamer                               
│   │       configuration_vibevoice                modeling_vibevoice_streaming           modular_vibevoice_diffusion_head       modular_vibevoice_tokenizer            
│   ├──   processor/ (4 files, 65.0KB, all .py)
│   │   └── __init__                      vibevoice_processor           vibevoice_streaming_processor vibevoice_tokenizer_processor 
│   ├──   schedule/ (3 files, 49.5KB, all .py)
│   │   └── __init__         dpm_solver       timestep_sampler 
│   ├──   scripts/ (2 files, 6.1KB, all .py)
│   │   └── __init__                                    convert_nnscaler_checkpoint_to_transformers 
│   └── __init__.py 
└── .gitignore     CLAUDE.md      GEMINI.md      LICENSE        README.md      SECURITY.md    pyproject.toml 
```

## Dependencies (`codemap --deps`)
```
╭───────────────────────────────╮
│  VibeVoice - Dependency Flow  │
╰───────────────────────────────╯

Demo ═══════════════════════════════════════════════════════
  app ───▶ modeling_vibevoice_streaming_inference, vibevoice_streaming_processor, streamer
  realtime_model_inference_from_file ───▶ modeling_vibevoice_streaming_inference, vibevoice_streaming_processor
  +1 standalone files

Vibevoice ══════════════════════════════════════════════════
  vibevoice_streaming_processor ───▶ modular_vibevoice_text_tokenizer
  modeling_vibevoice_streaming_inference ───▶ dpm_solver
  modeling_vibevoice_streaming ───▶ dpm_solver
  vibevoice_processor ───▶ modular_vibevoice_text_tokenizer
  convert_nnscaler_checkpoint_to_transformers ───▶ configuration_vibevoice
  +9 standalone files

─────────────────────────────────────────────────────────────
HUBS: dpm_solver (2←), modeling_vibevoice_streaming_inference (2←), vibevoice_streaming_processor (2←), modular_vibevoice_text_tokenizer (2←)
17 files · 156 functions · 10 deps
```