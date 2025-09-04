# Melody Generator (Genetic Algorithm Version)

A Python-based Melody Generator that creates MIDI melodies using a **genetic algorithm**. Users rate melodies interactively, and the system evolves new melodies based on your preferences. This version is **CLI-only**, no frontend required.

---

## Features

- Generate melodies with a genetic algorithm.
- User-driven fitness evaluation: rate each melody (1-5) to guide evolution.
- Customize:
  - Number of bars and notes per bar
  - Tempo (BPM)
  - Root note and scale (major/minor)
  - Population size, generations, and mutation rate
- Save the final accepted melody as a MIDI file.
- Play melodies temporarily during evaluation.

---

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/your-username/melody-generator.git
cd melody-generator
