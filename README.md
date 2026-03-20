# 🏃 Sub-30 Minute 5km Predictor (100-Day Project)

A data-driven approach to tracking physiological progression. This project utilizes personal running data to model fitness improvement and predict the timeline to achieving a sub-30 minute 5km run.

## 🔬 The Research Mission
As a self-taught AI/ML engineer, I am treating my daily running habit as a longitudinal study. By logging pace, heart rate, and recovery metrics over 100 days, I am building a dataset to perform predictive inference.

## 📈 The Mathematics of Progress
We model the pace improvement using **Linear Regression** to determine the rate of change in velocity ($v$) over time ($t$):

$$y = mx + b$$

Where:
* **$y$**: Predicted Pace (min/km)
* **$m$**: Rate of improvement (slope)
* **$x$**: Days of training
* **$b$**: Initial fitness baseline (intercept)

## 🛠️ Project Structure
- `log_run.py`: Python interface for daily data entry.
- `running_logs.csv`: The primary dataset tracking 100 days of runs.
- `predict.py`: (In Development) The inference engine to calculate the goal date.