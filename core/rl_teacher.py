# core/rl_teacher.py


def rl_teacher_optimize(prepared: dict, signals: dict, econ: dict, mc: dict) -> dict:
    try:
        score = (
            0.4 * signals["Overall Score"]
            + 0.3 * max(0, econ["econometric_prediction"])
            + 0.2 * (1 - abs(mc["mc_std"]))
            + 0.1 * (1 - abs(mc["mc_mean"]))
        )
        action = (
            "Increase policy stability"
            if score < 40
            else "Boost adoption mechanisms"
            if score < 70
            else "Optimise for resilience cluster"
        )
        return {"rl_reward": float(score), "rl_action": action}
    except Exception:
        return {"rl_reward": 0.0, "rl_action": "No optimisation"}
