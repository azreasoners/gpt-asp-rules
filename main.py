import argparse

from dataset150 import data_gen
from pipeline import Pipeline

def main(args):
    puzzle_pipeline = Pipeline(vars(args))
    puzzle_pipeline.path_prompt = {
        'constants': 'prompts/2_constant_formatting.txt',
        'predicates': 'prompts/3_gen_predicates.txt',
        'search_space': 'prompts/4_gen_search_space.txt',
        'paraphrasing': 'prompts/5_paraphrasing.txt',
        'constraints': 'prompts/6_gen_constraints.txt',
    }
    prefix = 'gpt_split_' + args.engine + '_'
    puzzle_pipeline.path_cache = {k: f'caches/{prefix}{k}.json' for k in puzzle_pipeline.path_prompt}
    puzzle_pipeline.load_prompt()
    puzzle_pipeline.load_cache()

    num = 50 if args.num == -1 else min(args.num, 50)
    puzzles = data_gen(args.dataset_name, num)
    incorrect_indices = []
    for i in range(1, num+1):
        print(f'Solving puzzle {i}')
        story, constraints, constants, solution = puzzles[i-1]
        replace = {
            '<STORY>': story,
            '<CONSTRAINTS>': constraints,
            '<CONSTANTS>': constants,
            '<PREDICATES>': '',
        }

        # [optional: only used when skipping some steps] initialize placeholders
        constraints_paraphrased = rules_search_space = rules_constraints = rules_all = answer_sets = ''

        # Step 1: extract constants and their categories
        # this step is not needed for the logic puzzles

        # Step 2: format constants and their categories
        constants_formatted = puzzle_pipeline.gen_response('constants', replace)
        replace['<CONSTANTS>'] = constants_formatted

        # Step 3: generate predicates of interest
        predicates = puzzle_pipeline.gen_response('predicates', replace)
        replace['<PREDICATES>'] = predicates

        # Step 4: generate the search space (i.e., facts and choice rules)
        rules_search_space = puzzle_pipeline.gen_response('search_space', replace)

        # Step 5: paraphrase the constraints in sentence format
        constraints_paraphrased = puzzle_pipeline.gen_response('paraphrasing', replace)
        replace['<CONSTRAINTS>'] = constraints_paraphrased

        # Step 6: generate the constraints in rule format
        # rules_constraints = puzzle_pipeline.gen_response('constraints', replace)
        rules_constraints = puzzle_pipeline.gen_response_constraints('constraints', replace)

        # Step 7: compute answer sets
        rules_all = rules_search_space + '\n\n' + rules_constraints
        answer_sets = puzzle_pipeline.gen_answer_set(rules_all)

        # Step 8: evaluate final prediction
        if len(answer_sets) != 1:
            incorrect_indices.append(i)

        if len(answer_sets) == 1:
            filtered_set = [fact for fact in answer_sets[0] if ',' in fact]
            prediction = '\n'.join(filtered_set)
        else:
            prediction = ''
        # record all information/mistakes
        if len(answer_sets) != 1 or args.debug:
            puzzle_pipeline.mistakes.append((
                story, constraints, constraints_paraphrased, constants, constants_formatted,
                predicates, rules_search_space, rules_constraints, rules_all, len(answer_sets), prediction,
                solution
            ))

    print(f'Number of correct predictions: {num - len(incorrect_indices)}/{num}')
    print('Incorrect indices: ', incorrect_indices)
    cols = [
        'story', 'constraints', 'constraints_paraphrased', 'constants', 'constants_formatted',
        'predicates', 'rules_search_space', 'rules_constraints', 'rules_all', '#answer_sets', 'prediction',
        'solution'
    ]
    puzzle_pipeline.save_mistakes(cols)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset_name', default='test', type=str,
        help='the engine name in \{train, test, test_HA\}')
    parser.add_argument('--num', default=-1, type=int,
        help='the maximum number of puzzles to evaluate; -1 means all')
    parser.add_argument('--step', default=7, type=int,
        help='the program will run step 1, 2, ... until this specified number')
    parser.add_argument('--engine', default='text-davinci-003', type=str,
        help='the engine name in \{gpt-4, text-davinci-003, text-davinci-002, text-curie-001\}')
    parser.add_argument('--temperature', default=0., type=float,
        help='the temperature for the GPT-3 model')
    parser.add_argument('--max_tokens', default=1500, type=int,
        help='the max number of tokens to generate')
    parser.add_argument('--debug', default=False, action='store_true', help='debug mode')
    args = parser.parse_args()
    main(args)