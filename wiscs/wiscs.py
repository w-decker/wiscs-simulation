import numpy as np
import numpy.typing as npt
import pandas as pd
from typing import Dict, Any

vs = lambda x: np.sum(list(x.pop('task', None).values()))

def print_deltas(df, return_array=False):
    """Calculate deltas for each question collapsing across items and participants."""
    unique_q = sorted(df['question_idx'].unique())
    deltas = []
    for q in unique_q:
        sub = df[df['question_idx'] == q]
        m_w = sub.loc[sub['item_type'] == 'word', 'RT'].mean()
        m_i = sub.loc[sub['item_type'] == 'image', 'RT'].mean()
        diff = m_w - m_i
        deltas.append(diff)
        print(f"Q{q}: | word - image | = {np.abs(diff):.2f}")
    if return_array:
        return np.array(deltas)

def make_tasks(low, high, n) -> npt.ArrayLike:
    """Generate task parameters"""
    return np.random.permutation(np.linspace(low, high, n).round(0))

def _simulate_basic(
    word: Dict[str, float],
    image: Dict[str, float],
    noise: Dict[str, float],
    n_participants: int,
    n_items: int,
    n_questions: int,
    task: Dict[str, list]
) -> dict:
    """
    Your original _simulate_basic() function. 
    For convenience, the code is repeated here. 
    """
    vs = lambda x: np.sum(list(x.values()))
    
    # Cognitive components
    c_word = vs(word)
    c_image = vs(image)

    # Noise components
    image_noise = np.random.normal(0, noise['image'], (n_participants, n_questions, n_items))
    word_noise = np.random.normal(0, noise['word'], (n_participants, n_questions, n_items))
    participant_noise = np.random.normal(0, noise['participant'], (n_participants, n_questions, n_items))
    question_noise = np.random.normal(0, noise['question'], (n_participants, n_questions, n_items))

    # Task effects (separate for words and images)
    task_word = np.array(task.get('word', [0] * n_questions))[None, :, None]
    task_image = np.array(task.get('image', [0] * n_questions))[None, :, None]

    if len(task_word[0]) != n_questions or len(task_image[0]) != n_questions:
        raise ValueError("Task values must match the number of questions for both word and image conditions.")

    # Reaction times
    RT_word = c_word + task_word + word_noise + participant_noise + question_noise
    RT_image = c_image + task_image + image_noise + participant_noise + question_noise

    return dict(
        RT=dict(word=RT_word, image=RT_image),
        word_noise=word_noise,
        image_noise=image_noise,
        participant_noise=participant_noise,
        question_noise=question_noise,
        task_effects={'word': task_word, 'image': task_image},
        c=dict(word=c_word, image=c_image)
    )
def simulate(
    design: Dict[str, bool],
    word: Dict[str, float],
    image: Dict[str, float],
    noise: Dict[str, float],
    n_participants: int,
    n_items: int,
    n_questions: int,
    task: Dict[str, list] = None
) -> pd.DataFrame:
    """
    Simulate data with a mix of within-subjects and between-subjects factors.
    
    Parameters
    ----------
    design : dict
        A dictionary indicating whether each factor is within-subject (True) or between-subjects (False).
        Example: dict(questions=True, items=False)
    word : dict
        Cognitive components for word stimuli.
    image : dict
        Cognitive components for image stimuli.
    noise : dict
        Noise parameter dictionary, e.g. {'word': 10, 'image': 10, 'participant': 5, 'question': 3}
    n_participants : int
        Total number of participants.
    n_items : int
        Total number of items.
    n_questions : int
        Total number of questions.
    task : dict
        Dictionary with "word" and/or "image" keys to represent task-based manipulations across questions.

    Returns
    -------
    pd.DataFrame
        A long-form DataFrame containing columns such as:
        ['participant', 'item_type', 'question_idx', 'item_idx', 'RT']
        and possibly columns for 'group' or 'condition' if between-subject splits exist.
    """

    if task is None:
        # Default: no extra task effects
        task = {'word': [0]*n_questions, 'image': [0]*n_questions}

    items_within = design.get('items', True)
    if items_within:
        item_subgroups = [dict(label='both', n_participants=n_participants, sees_word=True, sees_image=True)]
    else:
        # Split participants into two subgroups
        half = n_participants // 2
        # If n_participants is odd, one group will just get an extra participant
        remainder = n_participants % 2
        item_subgroups = [
            dict(label='word_only',   n_participants=half + remainder, sees_word=True,  sees_image=False),
            dict(label='image_only',  n_participants=half,             sees_word=False, sees_image=True)
        ]

    questions_within = design.get('questions', True)
    if questions_within:
        # Single question set (1..n_questions)
        question_subgroups = [dict(label='allQ', n_questions=n_questions, question_offset=0)]
    else:
        # Split Q's in half
        half_q = n_questions // 2
        remainder_q = n_questions % 2
        question_subgroups = [
            dict(label='Q1', n_questions=half_q + remainder_q, question_offset=0),
            dict(label='Q2', n_questions=half_q,               question_offset=half_q + remainder_q)
        ]

    all_dfs = []
    participant_counter = 0

    for item_grp in item_subgroups:
        for q_grp in question_subgroups:
            # Build new "word" and "image" dictionaries as needed
            # If this subgroup doesn't see words at all, zero them out:
            this_word = word if item_grp['sees_word'] else {}
            this_image = image if item_grp['sees_image'] else {}

            # Build a custom "task" dict (so if they see no words, word-task is zero, etc.)
            # Also reduce the length of task lists if we're splitting questions.
            n_q_sub = q_grp['n_questions']
            q_off = q_grp['question_offset']
            
            sub_task = {}
            if 'word' in task:
                if item_grp['sees_word']:
                    sub_task['word'] = task['word'][q_off:q_off + n_q_sub]
                else:
                    sub_task['word'] = [0]*n_q_sub  # not seeing words => 0 effect
            if 'image' in task:
                if item_grp['sees_image']:
                    sub_task['image'] = task['image'][q_off:q_off + n_q_sub]
                else:
                    sub_task['image'] = [0]*n_q_sub  # not seeing images => 0 effect

            # Simulate for this subgroup
            sim_dict = _simulate_basic(
                word=this_word,
                image=this_image,
                noise=noise,
                n_participants=item_grp['n_participants'],
                n_items=n_items,
                n_questions=n_q_sub,
                task=sub_task
            )

            # Convert to DataFrame
            df_long = _dict_to_long_df(
                sim_dict=sim_dict,
                participant_offset=participant_counter,
                group_label=f"{item_grp['label']}__{q_grp['label']}"
            )

            # Update counters
            participant_counter += item_grp['n_participants']

            all_dfs.append(df_long)

    # Concatenate all subgroups
    final_df = pd.concat(all_dfs, ignore_index=True)

    return final_df

def dataframe(RT: np.ndarray, design: dict) -> pd.DataFrame:
    """
    Convert the output of the simulate() function into a tidy pandas DataFrame.
    
    Parameters
    ----------
    RT : np.ndarray
        A 3D array of simulated reaction times with shape (n_participants, n_questions, n_items).
    design : dict
        A dictionary indicating whether items and questions are between-subjects.
    
    Returns
    -------
    pd.DataFrame
        A tidy DataFrame with columns for Participant, Question, Item, RT, and factors.
    """
    n_participants, n_questions, n_items = RT.shape
    
    # Create participant IDs
    participant_ids = np.repeat(np.arange(1, n_participants + 1), n_questions * n_items)
    
    # Handle question IDs
    if design.get("questions", False):  # Questions are between-subjects
        question_ids = np.repeat(
            np.random.choice(np.arange(1, n_questions + 1), size=n_participants), n_items
        )
        question_ids = np.tile(question_ids, n_participants)
    else:  # Questions are within-subjects
        question_ids = np.tile(np.repeat(np.arange(1, n_questions + 1), n_items), n_participants)
    
    # Handle item IDs
    if design.get("items", False):  # Items are between-subjects
        item_ids = np.tile(
            np.random.choice(np.arange(1, n_items + 1), size=n_participants), n_questions
        )
        item_ids = np.repeat(item_ids, n_items)
    else:  # Items are within-subjects
        item_ids = np.tile(np.arange(1, n_items + 1), n_participants * n_questions)
    
    # Flatten reaction times
    RT_flat = RT.flatten()
    
    # Validate lengths
    assert len(participant_ids) == len(RT_flat), "Mismatch in participant IDs and RT_flat"
    assert len(question_ids) == len(RT_flat), "Mismatch in question IDs and RT_flat"
    assert len(item_ids) == len(RT_flat), "Mismatch in item IDs and RT_flat"
    
    # Build the DataFrame
    df = pd.DataFrame({
        "Participant": participant_ids,
        "Question": question_ids,
        "Item": item_ids,
        "RT": RT_flat
    })
    
    return df

def _dict_to_long_df(
        sim_dict: Dict[str, Any],
        participant_offset: int,
        group_label: str = ''
    ) -> pd.DataFrame:
        """
        Convert the _simulate_basic() output to a long DataFrame.
        We add an offset so participant indices don't collide across groups.
        """
        rt_word = sim_dict['RT']['word']  # shape: (n_participants, n_questions, n_items)
        rt_image = sim_dict['RT']['image']

        rows = []
        n_part = rt_word.shape[0]
        n_q = rt_word.shape[1]
        n_it = rt_word.shape[2]

        for p in range(n_part):
            for q in range(n_q):
                for i in range(n_it):
                    # Word condition row
                    rows.append({
                        'participant': participant_offset + p,
                        'group': group_label,
                        'item_type': 'word',
                        'question_idx': q,
                        'item_idx': i,
                        'RT': rt_word[p, q, i]
                    })
                    # Image condition row
                    rows.append({
                        'participant': participant_offset + p,
                        'group': group_label,
                        'item_type': 'image',
                        'question_idx': q,
                        'item_idx': i,
                        'RT': rt_image[p, q, i]
                    })

        return pd.DataFrame(rows)