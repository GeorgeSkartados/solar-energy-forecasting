import pandas as pd
import numpy as np
import random
from prophet import Prophet
import matplotlib.pyplot as plt

# Set seed for reproducibility
random.seed(42)
np.random.seed(42)

# Load the dataset
df = pd.read_csv("Book(Sheet1).csv")

# Clean: Remove rows with non-positive solar generation
df = df[df['total_solar'] > 0]

# Rename for Prophet
df = df.rename(columns={"datetime": "ds", "total_solar": "y"})

# Parse datetime (mixed formats handled by pandas)
df['ds'] = pd.to_datetime(df['ds'], dayfirst=True, errors='coerce')
df = df.dropna(subset=['ds'])

# Optional: Clip outliers (top 5%)
q95 = df['y'].quantile(0.95)
df['y'] = df['y'].clip(upper=q95)

# Fit the model
model = Prophet(daily_seasonality=True)
model.fit(df)

# Forecast next 7 days (hourly)
future = model.make_future_dataframe(periods=168, freq='H')
forecast = model.predict(future)

# Plot forecast
fig = model.plot(forecast)
plt.title("Solar Generation Forecast")
plt.xlabel("Date")
plt.ylabel("Solar Generation")
plt.tight_layout()
plt.show()

# Prepare forecast for export
forecast_trimmed = forecast[['ds', 'yhat']].rename(columns={'yhat': 'y'})
forecast_trimmed["type"] = "forecast"

# Prepare actuals
actual_trimmed = df[['ds', 'y']].copy()
actual_trimmed["type"] = "actual"

# Combine both
combined = pd.concat([actual_trimmed, forecast_trimmed], ignore_index=True)

# Export to CSV for Power BI
combined.to_csv("solar_combined_forecast.csv", index=False)

print("Forecast completed and exported as 'solar_combined_forecast.csv'")

