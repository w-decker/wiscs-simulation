from .constants import EMPTY_PARAMS
    
def _validate_params(params):
    if not isinstance(params, dict):
        raise ValueError("Params must be a dictionary")

    # Check that 'word' and 'image' keys are dictionaries
    if not isinstance(params.get("word"), dict) or not isinstance(params.get("image"), dict):
        raise ValueError("Params must be a dictionary of dictionaries")

    # Check that 'variance', 'n_participants', and 'n_trials' are present and are scalar values
    if not isinstance(params.get("variance"), (int, float)):
        raise ValueError("Params must contain 'variance' as a scalar value")
    if not isinstance(params.get("n_participants"), int):
        raise ValueError("Params must contain 'n_participants' as an integer")
    if not isinstance(params.get("n_trials"), int):
        raise ValueError("Params must contain 'n_trials' as an integer")

    return True
