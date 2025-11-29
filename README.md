## Build family trees from books with local LLMs

An experiment to see how far we can go with local resources on tackling an interesting problem. Extract a relationship graph from literature.
Using local LLMs extract family trees and relationships from texts.

## Installation

Download and setup [ollama](https://ollama.com/download) and pull a few models:

```
ollama pull gemma3
ollama pull mistral
```
it might take a while depending on your connection speed.

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), clone and install the repo

```bash
uv venv
source .venv/bin/activate
uv pip install .
```

## Usage

Get some literature from [project gutenberg](https://www.gutenberg.org/) and run the main script:

```bash
python src/main.py file model_name
```

Cleaning up the original text file greatly improves the results. 
Running on both complicated ([Middlemarch](https://www.gutenberg.org/ebooks/145)) and simpler books ([The Tale of Peter Rabbit](https://www.gutenberg.org/ebooks/14838)) yields mediocre results. 

