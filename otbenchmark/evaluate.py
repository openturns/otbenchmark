def evaluate(username, password, set_id, problem_id, x):
    """Evaluate a performance function

    Parameters
    ----------
        username : str
            Registered username for authentication.
            For testing without registration use 'testuser'.
        password : str
            Registered password for authentication.
            For testing without registration use 'testpass'.
        set_id : int
            Identification number of the problem set.
        problem_id : int
            Identification number of the problem.
        x : list, numpy.array
            Values of independent variables/random variables
            where the performance function is evaluated.
            Columns are the values of random variables (x1, x2,...xn).
            Bundle (vectorized) call is possible by providing multiple rows,
            each corresponds to one set of values of the random variables.

    Returns
    -------
        g_val_sys : list (numpy.array)
            Performance function value on system level.
        g_val_comp : list (numpy.array)
            Performance function value for each component.
        msg : str
            Diagnostic message.

    Examples
    --------
        >>> g_val_sys, g_val_comp, msg = evaluate(username='testuser',
                                                  password='testpass',
                                                  set_id=-1, problem_id=2,
                                                  x=[0.545, 1.23])
        >>> print(g_val_sys)
        1.2918
    """
    # -----------------------------------------------
    # Pre-processing
    # -----------------------------------------------
    import json
    import requests
    import numpy as np

    if isinstance(x, np.ndarray):
        x = x.tolist()

    main_url = "https://tno-black-box-challenge-api.herokuapp.com/"

    body = {
        "username": username,
        "password": password,
        "set_ID": set_id,
        "problem_ID": problem_id,
        "input_list": x,
    }

    # -----------------------------------------------
    # HTTP request
    # -----------------------------------------------
    r = requests.post(main_url + "evaluate", json=body, timeout=30)

    # -----------------------------------------------
    # Post-processing
    # -----------------------------------------------
    json_data = json.loads(r.text)

    msg = json_data["msg"]
    g_val_sys = json_data["g_val_sys"]
    g_val_comp = json_data["g_val_comp"]

    return g_val_sys, g_val_comp, msg
