# The following code to create a dataframe and remove duplicated rows is always executed and acts as a preamble for your script: 

# dataset <- data.frame(total_action_taken, year)
# dataset <- unique(dataset)

# Paste or type your script code here:
# The following code to create a dataframe and remove duplicated rows is always executed and acts as a preamble for your script: 

# dataset <- data.frame(total_action_taken, year)
# dataset <- unique(dataset)

# Paste or type your script code here:
# Check and install packages only if needed
# Check and install packages only if needed
if (!requireNamespace("forecast", quietly = TRUE)) {
  install.packages("forecast", lib = .libPaths()[1])
}
if (!requireNamespace("lubridate", quietly = TRUE)) {
  install.packages("lubridate", lib = .libPaths()[1])
}

library(forecast)
library(lubridate)

# Filter dataset to necessary records
ts_data <- ts(dataset$total_action_taken, start = min(dataset$year), frequency = 1)

# Split data into training and testing sets
train_size <- floor(0.8 * length(ts_data))
train_data <- head(ts_data, train_size)
test_data <- tail(ts_data, length(ts_data) - train_size)

# Fit a SARIMA model
sarima_model <- auto.arima(ts_data, seasonal = TRUE)

# Forecast with the SARIMA model
sarima_forecast <- forecast(sarima_model, h = length(ts_data))

# Plot the forecast
plot(sarima_forecast, main = "SARIMA Forecast of total actions taken for fly-tipping in London", xlab = "Year", ylab = "Total Actions Taken")

# Add actual values for the test set to the plot
lines(ts_data, col = "blue")


accuracy_metrics <- accuracy(sarima_forecast)
# Print the accuracy metrics to the console
print(accuracy_metrics)

# Add a legend with accuracy metrics to the plot
legend("topright", inset=.05, title="Accuracy Metrics",
    legend=c(paste("MAE:", round(accuracy_metrics[1, "MAE"], 2)),
        paste("RMSE:", round(accuracy_metrics[1, "RMSE"], 2)),
        paste("MAPE:", round(accuracy_metrics[1, "MAPE"], 2))),
    box.lty=1)
