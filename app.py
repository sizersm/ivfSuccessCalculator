import logging
import os
from enum import Enum

from flask import Flask, request, jsonify, Response, send_from_directory
import csv
import math

from pydantic import ValidationError

from calculation_helpers import (get_age_value, get_bmi_value, get_boolean_value, get_prior_live_birth_value,
                                 get_prior_pregnancy_value)
from parameter_model import Formula, IVFData

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

FORMULAS = []
BOOLEAN_VALUE_FACTOR_NAMES = ['tubal_factor',
                              'male_factor_infertility',
                              'endometriosis',
                              'ovulatory_disorder',
                              'diminished_ovarian_reserve',
                              'uterine_factor',
                              'other_reason',
                              'unexplained_infertility']
CSV_FILE_PATH = os.getenv('CSV_FILE_PATH', 'ivf_success_formulas.csv')


class ParamOption(str, Enum):
    TRUE = "TRUE"
    FALSE = "FALSE"
    NA = "N/A"


if not os.path.exists(CSV_FILE_PATH):
    logger.error(f"CSV file not found: {CSV_FILE_PATH}")
    exit()

with open('ivf_success_formulas.csv', mode='r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        try:
            FORMULAS.append(Formula(**row))
        except ValidationError as e:
            logger.error(f"Error validating row {row}: {e}")


def string_to_bool(value: str) -> bool:
    if value.upper() == ParamOption.TRUE:
        return True
    return False


def match_param(param: bool, formula_param: str) -> bool:
    return param == string_to_bool(formula_param) or formula_param == ParamOption.NA


def select_formula(formulas: list[Formula], data: IVFData) -> Formula | None:
    for formula in formulas:
        if match_param(data.using_own_eggs, formula.param_using_own_eggs) \
                and match_param(data.attempted_ivf_previously, formula.param_attempted_ivf_previously) \
                and match_param(data.is_reason_for_infertility_known, formula.param_is_reason_for_infertility_known):
            return formula
    return None


def calculate(data: IVFData) -> tuple[Response, int]:
    formula: Formula | None = select_formula(FORMULAS, data)

    if formula is None:
        return jsonify({"error": "No usable formula found"}), 400

    score: float = (formula.formula_intercept +
                    get_age_value(data, formula) +
                    get_bmi_value(data, formula) +
                    sum(get_boolean_value(data, formula, factor_name) for factor_name in BOOLEAN_VALUE_FACTOR_NAMES) +
                    get_prior_pregnancy_value(data, formula) +
                    get_prior_live_birth_value(data, formula))

    exp_score = math.exp(score)
    success_chance_percentage: float = exp_score / (1 + exp_score)

    return jsonify({"success_chance_percentage": success_chance_percentage * 100}), 200


@app.route('/calculate', methods=['POST'])
def calculate_success():
    data = request.get_json()

    try:
        ivf_data = IVFData(**data)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    return calculate(ivf_data)


@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
