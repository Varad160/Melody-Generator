import streamlit as st
import random
import os
from midiutil import MIDIFile
from typing import List, Tuple
from midi2audio import FluidSynth

BITS_PER_NOTE = 4
NOTES = ["C", "D", "E", "F", "G", "A", "B"]
SCALES = {"major": [0, 2, 4, 5, 7, 9, 11], "minor": [0, 2, 3, 5, 7, 8, 10]}


def generate_genome(length: int) -> List[int]:
    """Generate a random genome."""
    return [random.randint(0, 1) for _ in range(length)]


def int_from_bits(bits: List[int]) -> int:
    """Convert binary bits to an integer."""
    return int("".join(map(str, bits)), 2)


def genome_to_notes(genome: List[int], scale: str, root_note: int) -> List[int]:
    """Convert genome to a sequence of notes based on the scale."""
    notes = [genome[i:i + BITS_PER_NOTE] for i in range(0, len(genome), BITS_PER_NOTE)]
    scale_intervals = SCALES[scale]
    return [root_note + scale_intervals[int_from_bits(note) % len(scale_intervals)] for note in notes]


def play_melody(melody: List[int], bpm: int):
    """Play a melody as a temporary MIDI file (without saving)."""
    midi = MIDIFile(1)
    track = 0
    time = 0
    channel = 0
    duration = 1
    volume = 100

    midi.addTempo(track, time, bpm)
    for note in melody:
        midi.addNote(track, channel, note + 60, time, duration, volume)
        time += duration

    # Save as a temporary file for playback
    temp_filename = "temp_melody.mid"
    with open(temp_filename, "wb") as temp_file:
        midi.writeFile(temp_file)
    
    # Play the temporary MIDI file using a default player
    import os
    if os.name == 'nt':  # Windows
        os.system(f"start {temp_filename}")
    else:  # MacOS/Linux
        os.system(f"open {temp_filename}")


def mutate_genome(genome: List[int], mutation_rate: float) -> List[int]:
    """Mutate the genome."""
    return [bit if random.random() > mutation_rate else 1 - bit for bit in genome]


def crossover(parent1: List[int], parent2: List[int]) -> Tuple[List[int], List[int]]:
    """Perform single-point crossover between two genomes."""
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2


def main():
    num_bars = 4
    num_notes_per_bar = 4
    genome_length = num_bars * num_notes_per_bar * BITS_PER_NOTE
    population_size = 5
    mutation_rate = 0.1
    generations = 10
    bpm = 120
    root_note = 0  # C
    scale = "major"

    # Initialize the population
    population = [generate_genome(genome_length) for _ in range(population_size)]

    for generation in range(generations):
        print(f"\n--- Generation {generation + 1} ---")

        # Evaluate fitness (user ratings)
        fitness_scores = []
        for i, genome in enumerate(population):
            melody = genome_to_notes(genome, scale, root_note)
            print(f"Playing melody {i + 1} of generation {generation + 1}. Please rate it (1-5):")
            play_melody(melody, bpm)
            rating = int(input(f"Rate melody {i + 1}: "))
            fitness_scores.append((genome, rating))

            # If user rates it 5, accept and save as the final output
            if rating == 5:
                print("Accepted melody with a rating of 5. Saving the final output...")
                save_final_melody(melody, bpm, "final_melody.mid")
                return

        # Sort by fitness
        fitness_scores.sort(key=lambda x: x[1], reverse=True)

        # Selection and reproduction
        next_population = []
        for _ in range(population_size // 2):
            parent1, parent2 = random.choices([x[0] for x in fitness_scores[:2]], k=2)
            child1, child2 = crossover(parent1, parent2)
            next_population.extend([mutate_genome(child1, mutation_rate), mutate_genome(child2, mutation_rate)])

        population = next_population

    print("Music generation complete but no melody was accepted. Exiting...")


def save_final_melody(melody: List[int], bpm: int, filename: str):
    """Save the final accepted melody to a MIDI file."""
    midi = MIDIFile(1)
    track = 0
    time = 0
    channel = 0
    duration = 1
    volume = 100

    midi.addTempo(track, time, bpm)
    for note in melody:
        midi.addNote(track, channel, note + 60, time, duration, volume)
        time += duration

    with open(filename, "wb") as file:
        midi.writeFile(file)
    print(f"Final melody saved as {filename}.")


if __name__ == "__main__":
    main()
