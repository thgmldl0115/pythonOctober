import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel('./test_sec.xlsx')

print(df.head())

# Convert the 'DETAILTIME' column to datetime type for plotting
df['SEC'] = pd.to_datetime(df['SEC'])

# Plotting the line graph
plt.figure(figsize=(12, 6))
plt.plot(df['SEC'], df['SLEEP'], label=' Weight (g)', linestyle='-', marker='')

# Setting labels and title
plt.xlabel('Time')
plt.ylabel('Grams')
plt.title('Sleep G vs Time')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Display the plot
plt.show()