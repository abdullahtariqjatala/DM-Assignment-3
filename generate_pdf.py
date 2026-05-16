"""Generate DS3002 Assignment 3 PDF report using ReportLab."""
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image,
    HRFlowable, PageBreak, ListFlowable, ListItem
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT

BASE = Path(__file__).parent
OUT  = BASE / "DS3002_Assignment3_Report.pdf"

doc = SimpleDocTemplate(
    str(OUT), pagesize=A4,
    leftMargin=2.5*cm, rightMargin=2.5*cm,
    topMargin=2.5*cm, bottomMargin=2.5*cm
)

styles = getSampleStyleSheet()
W = A4[0] - 5*cm  # usable width

# ── Custom styles ─────────────────────────────────────────────────────────────
title_style = ParagraphStyle('Title2', parent=styles['Title'],
    fontSize=18, spaceAfter=4, alignment=TA_CENTER)
subtitle_style = ParagraphStyle('Sub', parent=styles['Normal'],
    fontSize=13, spaceAfter=3, alignment=TA_CENTER, textColor=colors.HexColor('#333333'))
meta_style = ParagraphStyle('Meta', parent=styles['Normal'],
    fontSize=11, spaceAfter=16, alignment=TA_CENTER, textColor=colors.HexColor('#555555'))
h2_style = ParagraphStyle('H2', parent=styles['Heading1'],
    fontSize=14, spaceBefore=18, spaceAfter=6,
    textColor=colors.HexColor('#111111'), borderPadding=(0,0,3,0))
h3_style = ParagraphStyle('H3', parent=styles['Heading2'],
    fontSize=12, spaceBefore=12, spaceAfter=4,
    textColor=colors.HexColor('#222222'))
body_style = ParagraphStyle('Body', parent=styles['Normal'],
    fontSize=11, leading=16, spaceAfter=6, alignment=TA_JUSTIFY)
caption_style = ParagraphStyle('Caption', parent=styles['Normal'],
    fontSize=9, leading=13, spaceAfter=10, alignment=TA_CENTER,
    textColor=colors.HexColor('#444444'), fontName='Helvetica-Oblique')
bullet_style = ParagraphStyle('Bullet', parent=styles['Normal'],
    fontSize=11, leading=16, leftIndent=16, spaceAfter=3)

def h2(text):
    return [HRFlowable(width=W, thickness=1.5, color=colors.HexColor('#333333'),
                       spaceAfter=4),
            Paragraph(text, h2_style)]

def h3(text):
    return [Paragraph(text, h3_style)]

def body(text):
    return Paragraph(text, body_style)

def fig(filename, caption_text, width_frac=1.0):
    p = BASE / filename
    if not p.exists():
        return [Paragraph(f"[Image not found: {filename}]", caption_style)]
    img = Image(str(p), width=W*width_frac,
                height=W*width_frac * 0.55, kind='proportional')
    return [Spacer(1, 6), img,
            Paragraph(caption_text, caption_style), Spacer(1, 4)]

def bullets(items):
    return ListFlowable(
        [ListItem(Paragraph(i, bullet_style), leftIndent=20) for i in items],
        bulletType='bullet', start='•'
    )

def numbered(items):
    return ListFlowable(
        [ListItem(Paragraph(i, bullet_style), leftIndent=20) for i in items],
        bulletType='1'
    )

# ── Build story ───────────────────────────────────────────────────────────────
story = []

# Title
story += [
    Paragraph("DS-3002 Data Mining", title_style),
    Paragraph("Assignment #3 — Pulse to Prediction", subtitle_style),
    Paragraph("Mining Temporal Patterns and Building Classifiers on Patient Health Data", subtitle_style),
    Paragraph("Spring 2026 &nbsp;|&nbsp; BSDS &nbsp;|&nbsp; FAST-NUCES &nbsp;|&nbsp; 19th April 2026", meta_style),
    HRFlowable(width=W, thickness=2, color=colors.HexColor('#111111'), spaceAfter=12),
]

# ── 1. Dataset Overview ───────────────────────────────────────────────────────
story += h2("1. Dataset Overview")
story.append(body(
    "The dataset consists of simulated wearable and clinical readings from a "
    "regional hospital network. Each row represents one time-stamped vital sign "
    "reading for a patient, with readings spaced 6 hours apart, giving "
    "approximately 120 readings per patient over 30 days."
))
story.append(bullets([
    "<b>Size:</b> ~60,000 rows, 500 patients",
    "<b>Key columns:</b> PatientID, Timestamp, HeartRate, BloodPressureSystolic, "
    "BloodPressureDiastolic, BloodOxygenLevel, BodyTemperature, RespiratoryRate, "
    "SleepHours, StressLevel, Age, Gender, Diagnosis",
    "<b>Diagnosis classes:</b> Healthy, Hypertension, Diabetes, Arrhythmia, Sleep Disorder",
]))
story.append(Spacer(1, 8))

# ── 2. Preprocessing ──────────────────────────────────────────────────────────
story += h2("2. Preprocessing")
story.append(body(
    "The preprocessing pipeline ensures data quality and creates two clean data "
    "structures used throughout the rest of the pipeline."
))
story.append(numbered([
    "Loaded <i>patient_vitals.csv</i> and parsed Timestamp as a datetime column.",
    "Verified no null values in PatientID, Timestamp, or Diagnosis.",
    "Applied physiological range filters (e.g. HeartRate ∈ [40,180], "
    "BloodPressureSystolic ∈ [80,200]) and reported rows dropped per column.",
    "Sorted all records by PatientID then Timestamp.",
    "Built a per-patient time series dictionary for Part A.",
    "Constructed a patient-level feature matrix (mean, std, min, max, linear "
    "trend slope per vital sign) for Parts B and C.",
]))
story.append(Spacer(1, 8))

# ── 3. Part A ─────────────────────────────────────────────────────────────────
story += h2("3. Part A — Time Series Analysis & Trend Detection")

story += h3("A1 — Heart Rate Visualisation & Descriptive Statistics")
story.append(body(
    "Three patients were selected — one from each of the Healthy, Hypertension, "
    "and Arrhythmia classes. Their HeartRate time series were plotted on a single "
    "figure with three subplots, and descriptive statistics (mean, std, min, max, "
    "coefficient of variation) were computed for each."
))
story += fig("A1_heartrate_timeseries.png",
    "Figure 1: Heart rate time series for three selected patients. The Healthy "
    "patient shows a narrow, stable band around a normal mean. The Hypertension "
    "patient exhibits a moderately elevated mean with higher variability. The "
    "Arrhythmia patient displays pronounced irregular spikes and troughs, "
    "reflected in the highest coefficient of variation among the three.")

story += h3("A2 — Rolling Means & Additive Decomposition")
story.append(body(
    "BloodPressureSystolic was analysed using 7-reading and 14-reading rolling "
    "means overlaid on the raw signal for each of the three selected patients. "
    "Additive time series decomposition (trend + seasonality + residual) was "
    "applied to the patient with the most readings using a weekly period (28 readings)."
))
story += fig("A2_rolling_means.png",
    "Figure 2: BP Systolic with 7-reading and 14-reading rolling means. The "
    "7-reading window retains more local fluctuation, while the 14-reading window "
    "reveals broader trends. Both suppress noise but cannot separate trend from seasonality.")
story += fig("A2_decomposition.png",
    "Figure 3: Additive decomposition of BP Systolic. The four panels show the "
    "observed signal, isolated long-term trend, weekly seasonal component, and "
    "irregular residual. The trend panel reveals whether BP is systematically "
    "rising or falling independent of periodic rhythms.")

story += h3("A3 — Anomaly Detection via Personal μ ± 2σ")
story.append(body(
    "For every patient, a personal mean (μ) and standard deviation (σ) were "
    "computed for HeartRate. Readings exceeding μ ± 2σ were flagged as anomalies. "
    "The total anomaly count, percentage per diagnosis class, and top-5 anomaly "
    "patients were reported."
))
story += fig("A3_anomaly_plot.png",
    "Figure 4: HeartRate time series for the patient with the highest anomaly "
    "count. Red dots mark flagged readings exceeding the personal μ ± 2σ threshold. "
    "The dashed black line shows the patient's mean and orange dotted lines mark "
    "the ±2σ bounds. Arrhythmia patients show substantially higher anomaly rates "
    "than Healthy patients due to their inherently irregular heart rhythm.")

# ── 4. Part B ─────────────────────────────────────────────────────────────────
story += h2("4. Part B — Similarity Search & Patient Matching")

story += h3("B1 — Euclidean & Manhattan Nearest Neighbours")
story.append(body(
    "Ten random query patients (seed = 42) were selected. For each, the top-3 "
    "nearest neighbours were found using both Euclidean and Manhattan distance on "
    "the normalised patient-level feature matrix. Euclidean distance penalises "
    "large deviations quadratically, while Manhattan distance sums absolute "
    "differences linearly. In high-dimensional normalised spaces both metrics "
    "tend to agree on the closest neighbours."
))

story += h3("B2 — DTW-Based Similarity on Raw Time Series")
story.append(body(
    "Dynamic Time Warping (DTW) was applied to HeartRate sequences (first 20 "
    "readings, normalised to zero mean and unit variance) for all 500 patients. "
    "For three query patients (one per class), the top-3 DTW-nearest neighbours "
    "were reported and compared to Euclidean-based neighbours. DTW is more "
    "meaningful than Euclidean distance for time series that may be shifted or "
    "stretched in time, as it aligns sequences optimally before measuring distance."
))

story += h3("B3 — New Patient Diagnosis Prediction")
story.append(body(
    "A new patient with known vital statistics (HeartRate_mean = 98, "
    "BP_Systolic_mean = 155, BloodOxygenLevel_mean = 94, SleepHours_mean = 4.5) "
    "was normalised using the training scaler. The top-5 Euclidean nearest "
    "neighbours were identified and the predicted diagnosis was determined by "
    "majority vote. The elevated heart rate, high BP, reduced oxygen level, and "
    "low sleep strongly suggest Hypertension, consistent with the prediction."
))
story.append(Spacer(1, 8))

# ── 5. Part C ─────────────────────────────────────────────────────────────────
story += h2("5. Part C — Supervised Classification")
story.append(body(
    "All five classifiers were trained on the same patient-level feature matrix "
    "using a stratified 80/20 train-test split (random_state = 42). Each "
    "classifier reports accuracy, macro precision, recall, F1-score, and a "
    "confusion matrix."
))

story += h3("C1 — Decision Tree")
story.append(body(
    "A Decision Tree was trained with entropy criterion. max_depth was tuned "
    "over {2, 4, 6, 8, 10} by evaluating test accuracy. The tree was visualised "
    "to depth 3 and the top-5 feature importances were reported."
))
story += fig("C1_dt_depth.png",
    "Figure 5: Test accuracy vs. max_depth. Accuracy improves with depth up to "
    "a point, after which overfitting causes it to plateau or decline.", 0.7)
story += fig("C1_tree_viz.png",
    "Figure 6: Decision Tree visualised to depth 3. Each node shows the splitting "
    "feature, threshold, sample count, and majority class. Top splits involve BP "
    "and heart rate statistics, reflecting their clinical importance.")
story += fig("C1_feature_importance.png",
    "Figure 7: Top-5 feature importances by entropy gain. Blood pressure and "
    "heart rate features dominate, consistent with clinical knowledge.", 0.7)
story += fig("C1_Decision_Tree_cm.png",
    "Figure 8: Confusion matrix for the Decision Tree. Strong diagonal values "
    "indicate good per-class accuracy.", 0.6)

story += h3("C2 — Rule-Based Classification")
story.append(body(
    "An interpretable rule set of 12 clinically-grounded if-then rules was "
    "extracted. Each rule was evaluated for coverage and accuracy. The rule set "
    "provides full transparency at the cost of some accuracy compared to the "
    "Decision Tree."
))
story += fig("C2_rules_cm.png",
    "Figure 9: Confusion matrix for the rule-based classifier. Each prediction "
    "can be traced to a specific clinical condition, making this classifier "
    "highly auditable.", 0.6)

story += h3("C3 — k-Nearest Neighbour")
story.append(body(
    "A kNN classifier was trained on the normalised feature matrix. k was tuned "
    "over {1, 3, 5, 7, 9, 11, 15, 21} for both Euclidean and Manhattan metrics. "
    "kNN is a lazy learner; while effective here, its inference time grows "
    "linearly with dataset size, making it impractical for real-time hospital "
    "deployment at scale."
))
story += fig("C3_knn_accuracy.png",
    "Figure 10: Train and test accuracy vs. k for Euclidean (left) and Manhattan "
    "(right) metrics. Small k overfits; larger k smooths decision boundaries.")
story += fig("C3_kNN_cm.png",
    "Figure 11: Confusion matrix for the best kNN configuration.", 0.6)

story += h3("C4 — Gaussian Naïve Bayes")
story.append(body(
    "Gaussian NB was trained after verifying the Gaussian assumption via "
    "histograms and Q-Q plots. The Pearson correlation matrix was computed to "
    "assess the feature independence assumption. Strongly correlated pairs "
    "violate the Naïve Bayes independence assumption but NB often performs well "
    "due to its low variance."
))
story += fig("C4_gaussian_check.png",
    "Figure 12: Histograms and Q-Q plots for HeartRate_mean, BP_Systolic_mean, "
    "and SleepHours_mean. Points close to the diagonal in Q-Q plots confirm "
    "approximate normality.")
story += fig("C4_correlation.png",
    "Figure 13: Pearson correlation heatmap of mean vital sign features. "
    "Strongly correlated pairs violate the Naïve Bayes independence assumption.", 0.75)
story += fig("C4_Gaussian_NB_cm.png",
    "Figure 14: Confusion matrix for Gaussian Naïve Bayes.", 0.6)

story += h3("C5 — Support Vector Machine")
story.append(body(
    "An SVM with One-vs-Rest strategy was trained. RBF and Polynomial (degree=3) "
    "kernels were compared, with regularisation parameter C ∈ {0.1, 1, 10, 100} "
    "tuned via 5-fold cross-validation. SVM typically achieves high accuracy but "
    "provides no human-readable explanation for its predictions."
))
story += fig("C5_SVM_cm.png",
    "Figure 15: Confusion matrix for the best SVM configuration.", 0.6)
story += fig("C5_svm_boundary.png",
    "Figure 16: SVM decision boundary in 2D via PCA. Each coloured region "
    "represents the predicted class. Non-linear boundaries show how SVM "
    "separates the five diagnosis classes.", 0.75)

# ── 6. Final Comparison ───────────────────────────────────────────────────────
story += h2("6. Final Classifier Comparison & Deployment Recommendation")
story += fig("Final_comparison.png",
    "Figure 17: Test accuracy comparison across all five classifiers. SVM and "
    "Decision Tree typically lead, while Naïve Bayes and Rule-Based classifiers "
    "trade accuracy for interpretability.", 0.8)
story.append(body(
    "For clinical deployment, the <b>Decision Tree</b> is the recommended primary "
    "classifier. While SVM may achieve marginally higher accuracy, the Decision "
    "Tree provides full transparency: clinicians can trace every prediction "
    "through explicit feature thresholds, which is essential for regulatory "
    "compliance and clinician trust. The rule-based system serves as a valuable "
    "complement — its hand-crafted rules are directly auditable and can be "
    "updated by domain experts without retraining. kNN is suitable for "
    "exploratory patient matching but is too slow for real-time inference at "
    "scale. Gaussian NB is a fast baseline but its independence assumption is "
    "violated by correlated vital signs. A production system should combine the "
    "Decision Tree for primary classification with the rule-based system as a "
    "safety net, and should be retrained periodically as new patient data "
    "accumulates."
))

# ── Build PDF ─────────────────────────────────────────────────────────────────
doc.build(story)
print(f"PDF saved: {OUT}")
