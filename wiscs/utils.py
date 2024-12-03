from .constants import EMPTY_PARAMS

def _validate_params(params):
    if not isinstance(params, dict):
        raise ValueError("Params must be a dictionary")

    # Check that 'word' and 'image' keys are dictionaries
    if not isinstance(params.get("word"), dict) or not isinstance(params.get("image"), dict):
        raise ValueError("Params must contain 'word' and 'image' dictionaries")
    required_keys = ["perceptual", "conceptual", "task"]

    # Check 'word' dictionary
    for key in required_keys:
        if key not in params["word"]:
            raise ValueError(f"'word' dictionary must contain the key '{key}'")
        if not isinstance(params["word"][key], (int, float, tuple)):
            raise ValueError(f"'word[{key}]' must be a numeric value")

    # Check 'image' dictionary
    for key in required_keys:
        if key not in params["image"]:
            raise ValueError(f"'image' dictionary must contain the key '{key}'")
        if not isinstance(params["image"][key], (int, float, tuple)):
            raise ValueError(f"'image[{key}]' must be a numeric value")

    # Check that 'variance', 'n_participants', 'n_trials' and 'dist_type' are present and are correct types
    if not isinstance(params.get("variance"), (int, float)):
        raise ValueError("Params must contain 'variance' as a scalar value")
    if not isinstance(params.get("n_participants"), int):
        raise ValueError("Params must contain 'n_participants' as an integer")
    if not isinstance(params.get("n_trials"), int):
        raise ValueError("Params must contain 'n_trials' as an integer")
    if not isinstance(params.get("dist_type"), str):
        raise ValueError("Params must contain 'dist_type' as a string")

    return True