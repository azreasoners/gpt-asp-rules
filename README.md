# GPT + ASP
This is the implementation of [Leveraging Large Language Models to Generate Answer Set Programs](https://proceedings.kr.org/2023/37/kr2023-0037-ishay-et-al.pdf).  
[Lab page](https://azreasoners.github.io/ARG-webpage/)

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

One can also use the following command to evaluate on the test dataset with the GPT-4 model.
```
python main.py --debug --dataset_name test --num 5 --engine gpt-4
```
To do the Sudoku and the Jobs Puzzle, one can run:
```
python sudoku.py --engine text-davinci-003
python jobs_puzzle.py --engine gpt-4
```
## How to read the results
- The results of every step are stored in the file `mistakes.xlsx` where each row denotes the provided information and different predictions (at different steps) for a puzzle.
- In `error_analysis`, you can view Excel files which track the errors and fixes for GPT-3 and GPT-4 on the logic puzzles test set. The errors are highlighted in red, and the fixes in blue. We categorize the errors and their subtypes as follows:

Paraphrase:
-	Either/or: about conversion of the either/or sentence being paraphrased incorrectly.
-	All different: about conversion of the “a,b,c, and d are different” sentence types being paraphrased incorrectly.

Constrant Generation (semantic):
-	Comparison between times: to do with a comparison of time being incorrect.
-	Operator: A wrong operator such as “<” in place of “>” or “+” in place of “-“.
-	Incorrect disjunction in the head: Associated with rules that have a disjunction in the head, where at least one of the elements of the disjunction should be in the body of the rule instead.
-	Other: A generic semantic error which does not fit into any prior pattern.

Constraint Generation (syntax): A variable name is wrong or two variables are out of order.  
Constant Formatting: A constant has double quotes around it when it should not.

## Citation
Please cite our paper as:
```
@inproceedings{KR2023-37,
    title     = {{Leveraging Large Language Models to Generate Answer Set Programs}},
    author    = {Ishay, Adam and Yang, Zhun and Lee, Joohyung},
    booktitle = {{Proceedings of the 20th International Conference on Principles of Knowledge Representation and Reasoning}},
    pages     = {374--383},
    year      = {2023},
    month     = {8},
    doi       = {10.24963/kr.2023/37},
    url       = {https://doi.org/10.24963/kr.2023/37},
  }
```
