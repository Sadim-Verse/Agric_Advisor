# 🌾 Agric Advisor

> A data-driven web app that predicts a crop's annual yield and gives farmers practical, tailored suggestions for improving it.

**🔗 Live demo:** [agric-advisor-1.streamlit.app](https://agric-advisor-1.streamlit.app/)

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B)
![scikit-learn](https://img.shields.io/badge/ML-scikit--learn-F7931E)

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Model & Data](#model--data)
- [Recommendation Logic](#recommendation-logic)
- [Supported Crops](#supported-crops)
- [Deployment](#deployment)
- [Known Limitations](#known-limitations)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Overview

Planning a harvest involves a lot of guesswork. **Agric Advisor** turns that guesswork into an estimate. A farmer selects a country and crop, enters basic environmental and input data, and the app predicts the expected annual yield using a trained machine learning model. Based on how high or low that prediction is, the app then offers actionable advice on rainfall management, temperature stress, and pesticide use.

## Features

- **Yield prediction**: estimates annual yield (in hectograms per hectare) from five inputs.
- **Guided inputs**: dropdowns for country and crop, and numeric fields bounded by the min/max values seen in the training data, which discourages unrealistic entries.
- **Crop classification**: tells the user what type of crop they selected (cereal, root, tuber, legume, or fruit).
- **Tiered recommendations**: four yield bands (low, average, good, excellent), each with advice on rainfall, temperature, and pesticide management.
- **Lightweight and deployable**: a single Streamlit app with a pre-trained model, so there is no backend or database to maintain.
- **Dev container support**: a `.devcontainer` configuration for a reproducible environment (e.g. GitHub Codespaces).

## How It Works

```
 User input                Preprocessing              Model                Output
┌──────────────┐        ┌────────────────┐        ┌──────────────┐     ┌────────────────────┐
│ Country      │        │ Label-encode   │        │ Pre-trained  │     │ Predicted yield    │
│ Crop         │ ─────► │ country & crop │ ─────► │ Random Forest│ ──► │ + crop type        │
│ Rainfall     │        │ (saved         │        │ (joblib)     │     │ + tiered advice    │
│ Pesticides   │        │  encoders)     │        │              │     │                    │
│ Temperature  │        └────────────────┘        └──────────────┘     └────────────────────┘
└──────────────┘
```

1. The app loads the trained model (`rfc_model_c.joblib`) and two fitted label encoders (`country_le`, `crop_le`).
2. The user's country and crop are converted to the numeric codes the model was trained on.
3. The five features are assembled into a single-row DataFrame and passed to the model.
4. The prediction is displayed, the crop is classified, and advice is chosen from the yield band.

## Project Structure

```
Agric_Advisor/
├── .devcontainer/        # Dev container configuration
├── app.py                # Streamlit UI and prediction flow (entry point)
├── yield_.py             # Helpers: dropdown options, input bounds, crop classification, advice
├── yield_pred.ipynb      # Notebook: data exploration, preprocessing, model training
├── rfc_model_c.joblib    # Trained model
├── country_le            # Fitted LabelEncoder for countries
├── crop_le               # Fitted LabelEncoder for crops
├── yield_df.csv          # Original dataset
├── new_yield_df.csv      # Cleaned dataset used by the app at runtime
├── requirements.txt      # Python dependencies
└── README.md
```

## Tech Stack

| Layer            | Technology                               |
| ---------------- | ---------------------------------------- |
| Language         | Python                                   |
| Web framework    | [Streamlit](https://streamlit.io/)       |
| Machine learning | [scikit-learn](https://scikit-learn.org/) |
| Data handling    | pandas, NumPy                            |
| Model storage    | joblib                                   |
| Experimentation  | Jupyter Notebook                         |

## Getting Started

### Prerequisites

- Python 3.9 or newer
- `pip` (and optionally `venv`)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Sadim-Verse/Agric_Advisor.git
cd Agric_Advisor

# 2. (Recommended) create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
# .venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

### Run the app

```bash
streamlit run app.py
```

Streamlit will print a local URL (usually `http://localhost:8501`). Open it in your browser.

> **Tip:** The saved model and encoders were created with a specific scikit-learn version. If you see unpickling warnings or errors, install the version used for training (check the notebook's output) or retrain the model with `yield_pred.ipynb`.

### Using the dev container

Open the repository in VS Code (Dev Containers extension) or GitHub Codespaces and the environment will be set up from `.devcontainer/`.

## Usage

1. **Select your country.**
2. **Select the crop** you plan to grow.
3. **Enter the average annual rainfall** (mm).
4. **Enter pesticide use** (tonnes).
5. **Enter the average temperature** (°C).
6. Click **Predict Annual Crop Yield**.

The app shows the predicted yield, the crop category, and a short list of suggestions matched to the yield level.

**Make sure all inputs are filled in before predicting.** The encoders and model require a value for every field.

## Model & Data

| Item              | Details                                                                                           |
| ----------------- | ------------------------------------------------------------------------------------------------- |
| **Task**          | Regression, predicting annual crop yield                                                          |
| **Model**         | `RandomForestRegressor` with default hyperparameters (saved as `rfc_model_c.joblib`)              |
| **Target**        | Yield in hectograms per hectare (hg/ha)                                                           |
| **Features**      | `Country`, `Crop`, `Average_annual_rainfall(mm)`, `Pesticides_used(tonnes)`, `Average_temperature(degree C)` |
| **Encoding**      | `LabelEncoder` for `Country` and `Crop`, persisted to `country_le` and `crop_le`                   |
| **Data files**    | `yield_df.csv` (raw), `new_yield_df.csv` (cleaned, used at runtime)                                |

> **Unit note:** 1 hg/ha = 0.1 kg/ha, so 20,000 hg/ha is 2,000 kg/ha (2 tonnes/ha).

The full training workflow (loading, cleaning, encoding, training, evaluation) is in [`yield_pred.ipynb`](./yield_pred.ipynb).

**Evaluation** (80/20 train/test split, `random_state=42`, 28,242 records):

| Model                                  | R² (test) | MAE (test, hg/ha) |
| -------------------------------------- | --------- | ----------------- |
| **Random Forest Regressor** (deployed) | **0.9729** | **5,654.61**      |
| XGBoost Regressor                      | 0.9660    | 8,730.21          |

Random Forest performed better on both metrics, so it was selected. The deployed model was then re-fit on the full dataset before being saved, so its score on that data (R² ≈ 0.9964) is a training score and not a measure of generalization.

## Recommendation Logic

The predicted yield (hg/ha) is mapped to one of four bands, and each band has its own advice on rainfall, temperature, and pesticide use:

| Band          | Predicted yield (hg/ha) | Focus of the advice                                                                 |
| ------------- | ----------------------- | ----------------------------------------------------------------------------------- |
| **Low**       | < 20,000                | Fix the basics: water retention (zai pits, contour ridges, mulch), shifting planting dates or using stress-tolerant varieties, weekly scouting, sprayer calibration |
| **Average**   | 20,000 to 39,999        | Optimize: plant after steady rains, foliar zinc/boron under heat stress, threshold-based spraying instead of fixed calendars, seed treatments |
| **Good**      | 40,000 to 59,999        | Fine-tune: field-level rain gauges, local weather alerts for timing sprays, targeted spraying of hotspots |
| **Excellent** | ≥ 60,000                | Sustain and innovate: soil moisture retention, on-farm trials of new varieties, local IPM groups |

The advice text lives in the `specs` dictionary in `yield_.py` and can be edited without touching the model.

## Supported Crops

| Category | Crops                |
| -------- | -------------------- |
| Cereal   | Maize, Rice (paddy), Sorghum, Wheat |
| Root     | Potatoes, Yams       |
| Tuber    | Cassava, Sweet potatoes |
| Legume   | Soybeans             |
| Fruit    | Plantains and others |

The countries available in the dropdown come directly from `new_yield_df.csv`.

## Deployment

The app is hosted on **Streamlit Community Cloud**: [agric-advisor-1.streamlit.app](https://agric-advisor-1.streamlit.app/).

To deploy your own copy:

1. Fork this repository.
2. Sign in at [share.streamlit.io](https://share.streamlit.io/) and click **New app**.
3. Select your fork, set the main file to `app.py`, and deploy.

## Known Limitations

- **Predictions are estimates, not guarantees.** Real yield also depends on soil, seed variety, irrigation, pests, and management practices, none of which are model inputs.
- **Coverage is limited** to the countries and crops present in the training data. Predictions outside the training range are unreliable, which is why numeric inputs are bounded.
- **Annual, aggregated inputs.** The model uses yearly averages and totals, so it cannot capture within-season effects.
- **Generic advice.** Recommendations are rule-based on yield bands and are not specific to local agronomic conditions. Consult a local extension officer before making major changes.
- **Version sensitivity.** The serialized model and encoders depend on the scikit-learn version used to create them.

## Roadmap

- [ ] Add RMSE and cross-validation to the evaluation
- [ ] Pin dependency versions in `requirements.txt`
- [ ] Add soil, fertilizer, and irrigation features
- [ ] Add charts comparing the prediction against regional averages
- [ ] Support multiple languages and units (kg/ha, tonnes/ha)
- [ ] Add unit tests for the helper functions
- [ ] Make the recommendations crop-specific

## Contributing

Contributions are welcome!

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push the branch: `git push origin feature/your-feature`
5. Open a pull request describing your changes.

For bugs or ideas, please [open an issue](https://github.com/Sadim-Verse/Agric_Advisor/issues).

## License

No license has been specified yet.

## Acknowledgements

- The Kaggle rainfall data made the training dataset possible
- [Streamlit](https://streamlit.io/) and [scikit-learn](https://scikit-learn.org/) for the tooling

---

Built by [Sadim-Verse](https://github.com/Sadim-Verse) to help farmers make better, data-informed decisions. 🌱
