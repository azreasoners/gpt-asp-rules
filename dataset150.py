"""
Data source:
    story: the problem description for each puzzle
    constraints: the hints for each puzzle
    constants: the constants manually extracted from the image for each puzzle
    solution: the solution of each puzzle
    domain_hint: the general hint for all puzzles (where the 2nd sentence is manually added)
"""

def data_gen(dataset_name='test', num_data=50):
    """
    Args:
        num_data (int): the maximum number of data to evaluate
        dataset_name (str): a string in {'train', 'test', 'test_HA'} denoting 3 datasets
    """
    if dataset_name == 'train': 
        data_path = 'LogicGridPuzzleData/Train_50/annoated/annotated_Train_[i].txt'
        solution_path = 'LogicGridPuzzleData/Train_50/Solution/sol_Train_[i].txt'
    elif dataset_name == 'test':
        data_path = 'LogicGridPuzzleData/Test_50/annotated/annotated_Test_[i].txt'
        solution_path = 'LogicGridPuzzleData/Test_50/Solution/sol_Test_[i].txt'
    else:
        data_path = 'LogicGridPuzzleData/Test_2_50_HA/HA_[i].txt'
        solution_path = 'LogicGridPuzzleData/Test_2_50_HA/sol_HA_[i].txt'

    puzzles = [] # a list of (story, constraints, constants, solution)
    domain_hint = 'Remember, as with all grid-based logic puzzles, no option in any category will ever be used more than once.'

    for i in range(1, num_data+1):
        i = str(i)
        with open(data_path.replace('[i]', i), 'r') as f:
            content = f.read().split('###')[0].replace('\t', '').replace('\n1. ', '\n::1. ').split('\n::')
            story, constraints, constants = content[0], content[-1], ''
            for s in content[1:-1]:
                category_constants = s.strip().split('\n')
                constants += category_constants[0] + ': ' + '; '.join(category_constants[1:]) + '.\n'
        with open(solution_path.replace('[i]', i), 'r') as f:
            solution = f.read()
        puzzles.append([story.strip() + ' ' + domain_hint, constraints.strip(), constants.strip(), solution.strip()])
        # puzzles.append([story.strip(), constraints.strip(), constants.strip(), solution.strip()])
    data_correction(dataset_name, puzzles)
    return puzzles

# remove the wrong category discussed in story
def data_correction(dataset_name, puzzles):
    if dataset_name == 'test':
        puzzles[11][0] = puzzles[11][0].replace('budget, ', '')
        puzzles[19][0] = puzzles[19][0]\
            .replace(', or featured people who played the same position', '')\
            .replace(''', and determine the player's position''', '')
        puzzles[48][0] = puzzles[48][0].replace('budget, ', '')
