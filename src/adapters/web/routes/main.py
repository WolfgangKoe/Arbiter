from flask import Blueprint, current_app, render_template, request

from src.domain.models.phase import PHASES
from src.domain.ports.army_repository import ArmyRepository

bp = Blueprint("main", __name__)

DEFAULT_MAX_ROUNDS = 5


@bp.route("/")
def index() -> str:
    repo: ArmyRepository = current_app.army_repository  # type: ignore[attr-defined]
    army = repo.get_army()

    try:
        phase_index = int(request.args.get("phase", 0))
    except ValueError:
        phase_index = 0

    try:
        round_num = int(request.args.get("round", 1))
    except ValueError:
        round_num = 1

    try:
        max_rounds = int(request.args.get("max_rounds", DEFAULT_MAX_ROUNDS))
    except ValueError:
        max_rounds = DEFAULT_MAX_ROUNDS

    phase_index = max(0, min(phase_index, len(PHASES) - 1))
    max_rounds = max(1, max_rounds)
    game_over = round_num > max_rounds

    if game_over:
        try:
            from_round = int(request.args.get("from_round", max_rounds))
        except ValueError:
            from_round = max_rounds
        from_round = max(1, min(from_round, max_rounds))

        try:
            from_phase = int(request.args.get("from_phase", len(PHASES) - 1))
        except ValueError:
            from_phase = len(PHASES) - 1
        from_phase = max(0, min(from_phase, len(PHASES) - 1))

        return render_template(
            "index.html",
            game_over=True,
            restart_url=f"/?phase=0&round=1&max_rounds={max_rounds}",
            back_url=f"/?phase={from_phase}&round={from_round}&max_rounds={max_rounds}",
            from_round=from_round,
            from_phase_name=PHASES[from_phase].name,
            round=max_rounds,
            max_rounds=max_rounds,
            phase=PHASES[0],
            total=len(PHASES),
            prev_url=None,
            next_url=None,
            end_game_url=None,
            army1_vp=0,
            army1_cp=0,
            army2_vp=0,
            army2_cp=0,
            army=army,
        )

    phase = PHASES[phase_index]

    if phase_index > 0:
        prev_url = f"/?phase={phase_index - 1}&round={round_num}&max_rounds={max_rounds}"
    elif round_num > 1:
        prev_url = f"/?phase={len(PHASES) - 1}&round={round_num - 1}&max_rounds={max_rounds}"
    else:
        prev_url = None

    if phase_index < len(PHASES) - 1:
        next_url = f"/?phase={phase_index + 1}&round={round_num}&max_rounds={max_rounds}"
    elif round_num < max_rounds:
        next_url = f"/?phase=0&round={round_num + 1}&max_rounds={max_rounds}"
    else:
        next_url = (
            f"/?round={max_rounds + 1}&phase=0"
            f"&from_round={round_num}&from_phase={phase_index}&max_rounds={max_rounds}"
        )

    end_game_url = (
        f"/?round={max_rounds + 1}&phase=0"
        f"&from_round={round_num}&from_phase={phase_index}&max_rounds={max_rounds}"
    )

    return render_template(
        "index.html",
        phase=phase,
        total=len(PHASES),
        prev_url=prev_url,
        next_url=next_url,
        end_game_url=end_game_url,
        round=round_num,
        max_rounds=max_rounds,
        game_over=False,
        army1_vp=0,
        army1_cp=0,
        army2_vp=0,
        army2_cp=0,
        army=army,
    )
