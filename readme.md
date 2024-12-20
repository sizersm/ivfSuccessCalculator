# IVF Success Calculator

## Prerequisites

Make sure you have the following installed on your system:

- **Python 3.8+**
- **pip** (Python package manager)

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/sizersm/ivfSuccessCalculator.git
cd ivfSuccessCalculator
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate    # On Windows
```

### 3. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Running the Application Locally

### 1. Start the Flask Server

Run the following command to start the Flask server:

```bash
flask run
```

The application will start and be accessible at:

```
http://127.0.0.1:5000
```

### 2. Access the Frontend

Open your web browser and navigate to:

```
http://127.0.0.1:5000/
```

You should see the IVF Success Calculator form. Fill out the form fields and submit to calculate the IVF success percentage.

---

## Testing the API

If you want to test the API directly without the frontend, you can use tools like **Postman** or **cURL**.

### Endpoint

**POST** `/calculate`

### Example Request

```bash
curl -X POST http://127.0.0.1:5000/calculate \
    -H "Content-Type: application/json" \
    -d '{
        "using_own_eggs": true,
        "attempted_ivf_previously": false,
        "is_reason_for_infertility_known": true,
        "tubal_factor": false,
        "male_factor_infertility": true,
        "endometriosis": false,
        "ovulatory_disorder": true,
        "diminished_ovarian_reserve": false,
        "uterine_factor": true,
        "other_reason": false,
        "unexplained_infertility": true,
        "prior_pregnancies": 2,
        "prior_live_births": 1,
        "age": 30,
        "height_feet": 5,
        "height_inches": 6,
        "weight_lbs": 140
    }'
```

### Example Response

```json
{
    "success_chance_percentage": 70.19
}
```

### Unit Testing

The only tests are currently in 'test_calculate.py'. Use the following command to run it via the terminal:

```bash
pytest test_calculate.py
```

---

## TODO

### Improved Validation

The input data form currently limits data ranges in some respects, but not appropriately. For example, logic setting minimum height to 4'6'' has not been implemented. Ideally, there would be form validation on the front end, as well as validation via Pydantic in the backend. Informative messaging should also be implemented to inform the user of their mistakes.

Additional logic for unselecting options that conflict with a more recently selected option should also be implemented. Unit tests should also be added for this.

### More Testing

Unit test are limited right now to the main calculation. More unit tests should be added for fail-cases such as unsupported input data ranges. Unit tests should also be added for sub-score calculations and formula selection.

### More Features

Improvements such as transfer success calculations and improved visualizations should be implemented.


