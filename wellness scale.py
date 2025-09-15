import pandas as pd
import os

# === Load dataset ===
file_path = "Scale for MentalHealthWelness - Student Wellness Dataset (Schoolwise) (1).csv"
df = pd.read_csv(file_path)

# Ensure numeric scores
df['score_ew'] = pd.to_numeric(df['score_ew'], errors='coerce')
df['score_cw'] = pd.to_numeric(df['score_cw'], errors='coerce')
df['score_aw'] = pd.to_numeric(df['score_aw'], errors='coerce')

def calculate_wellness_scale(data, org_ids):
    """Calculate the wellness thresholds for each class group and score type."""
    if org_ids != "all":
        data = data[data['org_id'].isin(org_ids)]

    results = []
    for class_group in sorted(data['class_group'].dropna().unique()):
        class_data = data[data['class_group'] == class_group]
        for score_col, score_label in [
            ('score_ew', 'Emotional (EW)'),
            ('score_cw', 'Cognitive (CW)'),
            ('score_aw', 'Academic (AW)')
        ]:
            mean_val = class_data[score_col].mean()
            std_val = class_data[score_col].std()

            thresholds = {
                'Class Group': class_group,
                'Score Type': score_label,
                'Needs Attention (< μ−2σ)': f"<{mean_val - 2 * std_val:.2f}",
                'Poor (μ−2σ to < μ−σ)': f"{mean_val - 2 * std_val:.2f}–{mean_val - std_val:.2f}",
                'Moderate (μ±σ)': f"{mean_val - std_val:.2f}–{mean_val + std_val:.2f}",
                'Good (> μ+σ to ≤ μ+2σ)': f"{mean_val + std_val:.2f}–{mean_val + 2 * std_val:.2f}",
                'Excellent (> μ+2σ)': f">{mean_val + 2 * std_val:.2f}",
                'Mean': round(mean_val, 2),
                'Std Dev': round(std_val, 2)
            }
            results.append(thresholds)
    return pd.DataFrame(results)

# === Main Program ===
user_input = input("Enter org_id(s) separated by commas, or type 'all' for all organizations: ").strip()

if user_input.lower() == "all":
    org_ids_to_check = "all"
else:
    try:
        org_ids_to_check = [int(x.strip()) for x in user_input.split(",") if x.strip() != ""]
    except ValueError:
        print("Please enter only numbers separated by commas or 'all'.")
        exit()

# Calculate
scale_df = calculate_wellness_scale(df, org_ids_to_check)

# Save results in the same directory as the script
output_path = os.path.join(os.path.dirname(os.path.abspath(file_path)), "wellness_scale_results.csv")
scale_df.to_csv(output_path, index=False)

print(f"\n Wellness scale calculated and saved to: {output_path}")
