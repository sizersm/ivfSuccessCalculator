from pydantic import BaseModel, Field


class IVFData(BaseModel):
    using_own_eggs: bool
    attempted_ivf_previously: bool
    is_reason_for_infertility_known: bool
    age: int
    height_feet: int
    height_inches: int
    weight_lbs: int
    tubal_factor: bool | None = Field(default=False)
    male_factor_infertility: bool | None = Field(default=False)
    endometriosis: bool | None = Field(default=False)
    ovulatory_disorder: bool | None = Field(default=False)
    diminished_ovarian_reserve: bool | None = Field(default=False)
    uterine_factor: bool | None = Field(default=False)
    other_reason: bool | None = Field(default=False)
    unexplained_infertility: bool | None = Field(default=False)
    prior_pregnancies: int = Field(default=0)
    prior_live_births: int = Field(default=0)

    @property
    def bmi(self) -> float:
        total_inches = self.height_feet * 12 + self.height_inches
        return (self.weight_lbs / (total_inches ** 2)) * 703


class Formula(BaseModel):
    param_using_own_eggs: str
    param_attempted_ivf_previously: str
    param_is_reason_for_infertility_known: str
    formula_intercept: float
    formula_age_linear_coefficient: float
    formula_age_power_factor: float
    formula_age_power_coefficient: float
    formula_bmi_linear_coefficient: float
    formula_bmi_power_factor: float
    formula_bmi_power_coefficient: float
    formula_prior_pregnancies_0_value: float
    formula_prior_pregnancies_1_value: float
    formula_prior_pregnancies_2_plus_value: float = Field(alias='formula_prior_pregnancies_2+_value')
    formula_prior_live_births_0_value: float
    formula_prior_live_births_1_value: float
    formula_prior_live_births_2_plus_value: float = Field(alias='formula_prior_pregnancies_2+_value')
    formula_tubal_factor_true_value: float
    formula_tubal_factor_false_value: float
    formula_male_factor_infertility_true_value: float
    formula_male_factor_infertility_false_value: float
    formula_endometriosis_true_value: float
    formula_endometriosis_false_value: float
    formula_ovulatory_disorder_true_value: float
    formula_ovulatory_disorder_false_value: float
    formula_diminished_ovarian_reserve_true_value: float
    formula_diminished_ovarian_reserve_false_value: float
    formula_uterine_factor_true_value: float
    formula_uterine_factor_false_value: float
    formula_other_reason_true_value: float
    formula_other_reason_false_value: float
    formula_unexplained_infertility_true_value: float
    formula_unexplained_infertility_false_value: float
