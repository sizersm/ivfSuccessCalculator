import pytest
from app import app, calculate
from parameter_model import IVFData


@pytest.fixture
def app_context():
    app_context = app.app_context()
    app_context.push()
    yield app_context
    app_context.pop()


@pytest.mark.parametrize("ivf_data, expected_status, expected_success_chance", [
    (
        IVFData(
            using_own_eggs=True,
            attempted_ivf_previously=False,
            is_reason_for_infertility_known=True,
            age=32,
            height_feet=5,
            height_inches=8,
            weight_lbs=150,
            tubal_factor=False,
            male_factor_infertility=False,
            endometriosis=True,
            ovulatory_disorder=True,
            diminished_ovarian_reserve=False,
            uterine_factor=False,
            other_reason=False,
            unexplained_infertility=False,
            prior_pregnancies=1,
            prior_live_births=1
        ),
        200,
        62
    ),
    (
        IVFData(
            using_own_eggs=False,
            attempted_ivf_previously=True,
            is_reason_for_infertility_known=False,
            age=50,
            height_feet=5,
            height_inches=4,
            weight_lbs=200,
            tubal_factor=False,
            male_factor_infertility=False,
            endometriosis=False,
            ovulatory_disorder=False,
            diminished_ovarian_reserve=False,
            uterine_factor=False,
            other_reason=False,
            unexplained_infertility=False,
            prior_pregnancies=0,
            prior_live_births=0
        ),
        200,
        47
    ),
    (
        IVFData(
            using_own_eggs=True,
            attempted_ivf_previously=False,
            is_reason_for_infertility_known=False,
            age=21,
            height_feet=5,
            height_inches=3,
            weight_lbs=115,
            tubal_factor=False,
            male_factor_infertility=False,
            endometriosis=False,
            ovulatory_disorder=False,
            diminished_ovarian_reserve=False,
            uterine_factor=False,
            other_reason=False,
            unexplained_infertility=False,
            prior_pregnancies=0,
            prior_live_births=0
        ),
        200,
        43
    ),
    (
        IVFData(
            using_own_eggs=True,
            attempted_ivf_previously=False,
            is_reason_for_infertility_known=True,
            age=36,
            height_feet=5,
            height_inches=3,
            weight_lbs=120,
            tubal_factor=False,
            male_factor_infertility=False,
            endometriosis=False,
            ovulatory_disorder=True,
            diminished_ovarian_reserve=False,
            uterine_factor=False,
            other_reason=False,
            unexplained_infertility=False,
            prior_pregnancies=1,
            prior_live_births=0
        ),
        200,
        46
    ),
    (
        IVFData(
            using_own_eggs=True,
            attempted_ivf_previously=True,
            is_reason_for_infertility_known=True,
            age=32,
            height_feet=5,
            height_inches=8,
            weight_lbs=150,
            tubal_factor=True,
            male_factor_infertility=False,
            endometriosis=False,
            ovulatory_disorder=False,
            diminished_ovarian_reserve=True,
            uterine_factor=False,
            other_reason=False,
            unexplained_infertility=False,
            prior_pregnancies=1,
            prior_live_births=1
        ),
        200,
        41
    )
])
def test_calculate(ivf_data, expected_status, expected_success_chance, app_context):
    response = calculate(ivf_data)

    assert response.status_code == expected_status

    json_response = response.get_json()

    assert isinstance(json_response["success_chance_percentage"], float)
    assert round(json_response["success_chance_percentage"]) == expected_success_chance


if __name__ == '__main__':
    pytest.main()
