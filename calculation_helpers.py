from parameter_model import Formula, IVFData


def get_prior_pregnancy_value(data: IVFData, formula: Formula) -> float:
    return {
        0: formula.formula_prior_pregnancies_0_value,
        1: formula.formula_prior_pregnancies_1_value
    }.get(data.prior_pregnancies, formula.formula_prior_pregnancies_2_plus_value)


def get_prior_live_birth_value(data: IVFData, formula: Formula) -> float:
    return {
        0: formula.formula_prior_live_births_0_value,
        1: formula.formula_prior_live_births_1_value
    }.get(data.prior_live_births, formula.formula_prior_live_births_2_plus_value)


def get_age_value(data: IVFData, formula: Formula) -> float:
    return (formula.formula_age_linear_coefficient * data.age +
            formula.formula_age_power_coefficient * (data.age ** formula.formula_age_power_factor))


def get_bmi_value(data: IVFData, formula: Formula) -> float:
    return (formula.formula_bmi_linear_coefficient * data.bmi +
            formula.formula_bmi_power_coefficient * (data.bmi ** formula.formula_bmi_power_factor))


def get_boolean_value(data: IVFData, formula: Formula, factor_name: str) -> float:
    return getattr(formula, f'formula_{factor_name}_true_value') if getattr(data, factor_name) else getattr(formula, f'formula_{factor_name}_false_value')
