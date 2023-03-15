# Introduction
This is the codes to use GPT-3 to generate ASP rules from logic puzzles.

## Installation
```
conda create --name gpt3-r -c conda-forge python=3.11
conda activate gpt3-r
conda install -c conda-forge openai clingo=5.6 tqdm xlsxwriter
```

## Preparation
Include your OpenAI API key in line 2 of `api_keys.py`.

## How to run
Execute the following codes to evaluate on 5 puzzles in the training data of 150-puzzle dataset.
```
python main.py --debug --dataset_name train --num 5
```
Here, the number `5` can be set to other numbers such as `10`, or `-1` which means to evaluate on all 50 training examples. The `dataset_name` can be one of `train`, `test`, and `test_HA`. The results of experiments will be recorded in `mistakes.xlsx`. If the option `--debug` is removed, then only the puzzles that we didn't get exactly 1 stable model will be recorded. (I will update the evaluation code to determine a correct prediction not by the number of stable models but by comparing the prediction and the solution.)

One can also use the following command to evaluate on the test dataset with ChatGPT model.
```
python main.py --debug --dataset_name test --num 5 --engine gpt-3.5-turbo
```

## How to read the results
- The results of every step are stored in the file `mistakes.xlsx` where each row denotes the provided information and different predictions (at different steps) for a puzzle.