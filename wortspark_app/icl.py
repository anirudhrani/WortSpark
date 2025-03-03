import os
import json
import random

class SampleGenerator:
    """Mainly serves two functionalitites.
        1. Generates demonstrations (first thirty demonstrations from the basic samples).
        2. Generates unseen demonstrations picked randomly either from basic samples or complex samples."""

    def __init__(self, dataset_path="wortspark_app/data/dataset.jsonl"):
        self.data = []
        with open(dataset_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        self.data.append(json.loads(line))
                    except json.JSONDecodeError as e:
                        print(f"Error decoding line: {line}\n{e}")

        output_chunks = []
        for entry in self.data[:30]:
            chunk = (
                f"\nExample Number: {entry['task_id']}\n"
                f"Input: {entry['task_description']}\n"
                f"Output: \n{entry['code']}\n"
            )
            output_chunks.append(chunk)
        
        self.formatted_samples = "\n".join(output_chunks)
    
    def demonstrations(self):
        """Return demonstrations to be embedded within the prompt as a string."""
        return self.formatted_samples
    
    def get_unseen_sample_at_random(self, within_30=True):
        """Samples one task at random from the unseen set."""
        filtered_data = [entry for entry in self.data if entry['task_id'] > 30]
        if not filtered_data:
            return None
        chosen = random.choice(filtered_data)
        
        return chosen['task_id'], chosen['task_description'], chosen['code']

# generator = SampleGenerator()
# print(generator.get_unseen_sample_at_random())
