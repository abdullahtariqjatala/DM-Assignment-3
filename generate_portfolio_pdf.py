"""Generate professional portfolio PDF report using ReportLab."""
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image,
    HRFlowable, PageBreak, ListFlowable, ListItem, Table, TableStyle
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT

BASE = Path(__file__).parent
OUT  = BASE / "PatientVitals_DataMining_Portfolio.pdf"

doc = SimpleDocTemplate(
    str(OUT), pagesize=A4,
    leftMargin=2.5*cm, rightMargin=2.5*cm,
    topMargin=2.5*cm, bottomMargin=2.5*cm
)

styles = getSampleStyleSheet()
W = A4[0] - 5*cm

DARK   = colors.HexColor('#1a1a2e')
ACCENT = colors.HexColor('#0f3460')
MID    = colors.HexColor('#16213e')
LIGHT  = colors.HexColor('#e94560')
GRAY   = colors.HexColor('#555555')
LGRAY  = colors.HexColor('#f4f4f4')

title_style = ParagraphStyle('T', parent=styles['Title'],
    fontSize=22, spaceAfter=6, alignment=TA_CENTER,
    textColor=DARK, fontName='Helvetica-Bold')
subtitle_style = ParagraphStyle('S', parent=styles['Normal'],
    fontSize=13, spaceAfter=4, alignment=TA_CENTER, textColor=ACCENT)
meta_style = ParagraphStyle('M', parent=styles['Normal'],
    fontSize=10, spaceAfter=4, alignment=TA_CENTER, textColor=GRAY)
tag_style = ParagraphStyle('Tag', parent=styles['Normal'],
    fontSize=10, spaceAfter=16, alignment=TA_CENTER,
    textColor=colors.HexColor('#888888'))
h2_style = ParagraphStyle('H2', parent=styles['Heading1'],
    fontSize=14, spaceBefore=20, spaceAfter=6,
    textColor=ACCENT, fontName='Helvetica-Bold')
h3_style = ParagraphStyle('H3', parent=styles['Heading2'],
    fontSize=12, spaceBefore=12, spaceAfter=4,
    textColor=DARK, fontName='Helvetica-Bold')
body_style = ParagraphStyle('Body', parent=styles['Normal'],
    fontSize=11, leading=17, spaceAfter=6, alignment=TA_JUSTIFY,
    textColor=colors.HexColor('#222222'))
caption_style = ParagraphStyle('Cap', parent=styles['Normal'],
    fontSize=9, leading=13, spaceAfter=10, alignment=TA_CENTER,
    textColor=GRAY, fontName='Helvetica-Oblique')
bullet_style = ParagraphStyle('Bul', parent=styles['Normal'],
    fontSize=11, leading=16, leftIndent=16, spaceAfter=3,
    textColor=colors.HexColor('#222222'))
highlight_style = ParagraphStyle('HL', parent=styles['Normal'],
    fontSize=11, leading=16, spaceAfter=6, alignment=TA_JUSTIFY,
    textColor=DARK, backColor=LGRAY, borderPadding=(6,8,6,8))

def h2(text):
    return [
        HRFlowable(width=W, thickness=2, color=ACCENT, spaceAfter=4),
        Paragraph(text, h2_style)
    ]

def h3(text):
    return [Paragraph(text, h3_style)]

def body(text):
    return Paragraph(text, body_style)

def fig(filename, caption_text, width_frac=1.0):
    p = BASE / filename
    if not p.exists():
        return [Paragraph(f"[Image not found: {filename}]", caption_style)]
    img = Image(str(p), width=W*width_frac,
                height=W*width_frac*0.55, kind='proportional')
    return [Spacer(1, 6), img,
            Paragraph(caption_text, caption_style), Spacer(1, 6)]

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

story = []

# ── Cover ─────────────────────────────────────────────────────────────────────
story += [
    Spacer(1, 1.5*cm),
    HRFlowable(width=W, thickness=3, color=ACCENT, spaceAfter=20),
    Paragraph("Pulse to Prediction", title_style),
    Paragraph("A Patient Intelligence Pipeline for Clinical Decision Support", subtitle_style),
    HRFlowable(width=W, thickness=1, color=LIGHT, spaceAfter=12),
    Spacer(1, 0.3*cm),
    Paragraph("Time Series Analysis &nbsp;·&nbsp; Similarity Search &nbsp;·&nbsp; Supervised Classification", tag_style),
    Spacer(1, 0.3*cm),
    Paragraph("Python &nbsp;·&nbsp; Pandas &nbsp;·&nbsp; Scikit-learn &nbsp;·&nbsp; Statsmodels &nbsp;·&nbsp; DTW &nbsp;·&nbsp; SVM &nbsp;·&nbsp; Decision Tree &nbsp;·&nbsp; kNN &nbsp;·&nbsp; Naïve Bayes", tag_style),
    Spacer(1, 0.5*cm),
    HRFlowable(width=W, thickness=3, color=ACCENT, spaceAfter=20),
    Spacer(1, 0.5*cm),
]

# Executive Summary box
summary_data = [[Paragraph(
    "<b>Executive Summary</b><br/><br/>"
    "This project presents a complete end-to-end data mining pipeline applied to "
    "a simulated patient vitals dataset of 500 patients and ~60,000 readings. "
    "The pipeline covers four complementary techniques: time series analysis and "
    "trend detection to identify deteriorating or improving vital trajectories; "
    "similarity search to match new patients against known profiles using "
    "Euclidean, Manhattan, and Dynamic Time Warping distances; and five supervised "
    "classification algorithms — Decision Tree, Rule-Based, k-Nearest Neighbour, "
    "Naïve Bayes, and Support Vector Machine — to build and compare diagnostic "
    "models. The project demonstrates the kind of predictive clinical "
    "decision-support pipeline deployed in modern health-tech systems.",
    body_style
)]]
summary_table = Table(summary_data, colWidths=[W])
summary_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), LGRAY),
    ('BOX',        (0,0), (-1,-1), 1, ACCENT),
    ('LEFTPADDING',  (0,0), (-1,-1), 12),
    ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ('TOPPADDING',   (0,0), (-1,-1), 10),
    ('BOTTOMPADDING',(0,0), (-1,-1), 10),
]))
story += [summary_table, Spacer(1, 0.4*cm)]

# Tech stack table
tech_data = [
    [Paragraph("<b>Domain</b>", body_style), Paragraph("<b>Tools / Libraries</b>", body_style)],
    ["Data Processing",    "Python, Pandas 3.x, NumPy"],
    ["Visualisation",      "Matplotlib, Seaborn"],
    ["Time Series",        "Statsmodels (seasonal_decompose), rolling windows"],
    ["Similarity / DTW",   "Pure-Python DTW, Scikit-learn pairwise_distances"],
    ["Classification",     "Scikit-learn (DecisionTree, kNN, GaussianNB, SVC)"],
    ["Evaluation",         "classification_report, ConfusionMatrixDisplay"],
]
tech_table = Table(tech_data, colWidths=[W*0.35, W*0.65])
tech_table.setStyle(TableStyle([
    ('BACKGROUND',   (0,0), (-1,0),  ACCENT),
    ('TEXTCOLOR',    (0,0), (-1,0),  colors.white),
    ('FONTNAME',     (0,0), (-1,0),  'Helvetica-Bold'),
    ('FONTSIZE',     (0,0), (-1,-1), 10),
    ('ROWBACKGROUNDS',(0,1),(-1,-1), [colors.white, LGRAY]),
    ('BOX',          (0,0), (-1,-1), 0.5, colors.HexColor('#cccccc')),
    ('INNERGRID',    (0,0), (-1,-1), 0.5, colors.HexColor('#cccccc')),
    ('LEFTPADDING',  (0,0), (-1,-1), 8),
    ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ('TOPPADDING',   (0,0), (-1,-1), 5),
    ('BOTTOMPADDING',(0,0), (-1,-1), 5),
]))
story += [tech_table, PageBreak()]

# ── 1. Dataset & Preprocessing ────────────────────────────────────────────────
story += h2("1. Dataset & Preprocessing")
story.append(body(
    "The dataset contains de-identified wearable and clinical readings from a "
    "hospital monitoring system. Each patient has approximately 120 readings "
    "taken every 6 hours over 30 days, covering 8 vital sign channels and "
    "5 diagnosis classes: <b>Healthy, Hypertension, Diabetes, Arrhythmia,</b> "
    "and <b>Sleep Disorder</b>."
))
story.append(Spacer(1, 4))
story.append(body("<b>Preprocessing steps performed:</b>"))
story.append(numbered([
    "Loaded the CSV and parsed Timestamp as a datetime column.",
    "Verified data integrity — no null values in PatientID, Timestamp, or Diagnosis.",
    "Applied physiological range filters per vital sign (e.g. HeartRate ∈ [40,180] bpm, "
    "BloodPressureSystolic ∈ [80,200] mmHg) and reported rows dropped per column.",
    "Sorted all records by PatientID then Timestamp.",
    "Built a per-patient time series dictionary for temporal analysis.",
    "Constructed a patient-level feature matrix: mean, std, min, max, and linear "
    "trend slope per vital sign — used as input to all classifiers.",
]))
story.append(Spacer(1, 8))

# ── 2. Time Series Analysis ───────────────────────────────────────────────────
story += h2("2. Time Series Analysis & Trend Detection")

story += h3("2.1  Heart Rate Visualisation & Descriptive Statistics")
story.append(body(
    "One patient from each of the Healthy, Hypertension, and Arrhythmia classes "
    "was selected for detailed time series analysis. HeartRate was plotted over "
    "the full 30-day observation window, and descriptive statistics — mean, "
    "standard deviation, min, max, and coefficient of variation (CV = σ/μ × 100%) "
    "— were computed per patient."
))
story += fig("A1_heartrate_timeseries.png",
    "Figure 1: Heart rate time series for three patients across different diagnosis "
    "classes. The Healthy patient maintains a narrow, stable band (low CV). The "
    "Hypertension patient shows a moderately elevated mean with higher variability. "
    "The Arrhythmia patient exhibits pronounced irregular spikes and troughs — "
    "the highest CV among the three — directly reflecting erratic electrical "
    "conduction characteristic of arrhythmic conditions.")

story += h3("2.2  Rolling Means & Additive Decomposition")
story.append(body(
    "BloodPressureSystolic was smoothed using 7-reading and 14-reading rolling "
    "means to reveal short- and medium-term trends. Additive time series "
    "decomposition was then applied to the longest patient sequence, isolating "
    "the long-term trend, weekly seasonal component, and irregular residual."
))
story += fig("A2_rolling_means.png",
    "Figure 2: BP Systolic overlaid with 7-reading and 14-reading rolling means "
    "for three patients. The 7-reading window preserves local fluctuations while "
    "the 14-reading window reveals broader directional trends. Both suppress "
    "measurement noise but conflate trend with seasonality.")
story += fig("A2_decomposition.png",
    "Figure 3: Additive decomposition of BP Systolic into observed signal, "
    "long-term trend, weekly seasonal component, and irregular residual. "
    "The trend component cleanly reveals whether BP is systematically rising "
    "or falling over the observation period, independent of periodic rhythms.")

story += h3("2.3  Anomaly Detection via Personal μ ± 2σ Thresholding")
story.append(body(
    "A personalised anomaly detection approach was applied: for each patient, "
    "a personal mean (μ) and standard deviation (σ) were computed for HeartRate. "
    "Any reading exceeding μ ± 2σ was flagged as anomalous. This patient-specific "
    "threshold is more clinically meaningful than a population-level cutoff "
    "because it accounts for individual baseline differences."
))
story += fig("A3_anomaly_plot.png",
    "Figure 4: HeartRate time series for the highest-anomaly patient, with "
    "flagged readings marked in red. The dashed black line shows the patient's "
    "personal mean; orange dotted lines mark the ±2σ bounds. Arrhythmia patients "
    "consistently show higher anomaly rates than Healthy patients, validating "
    "the clinical relevance of this detection method.")

story.append(PageBreak())

# ── 3. Similarity Search ──────────────────────────────────────────────────────
story += h2("3. Similarity Search & Patient Matching")

story += h3("3.1  Feature-Based Nearest Neighbours (Euclidean & Manhattan)")
story.append(body(
    "The patient-level feature matrix was normalised to zero mean and unit "
    "variance. For 10 randomly selected query patients, the top-3 nearest "
    "neighbours were identified using both Euclidean and Manhattan distance. "
    "Results were tabulated and the agreement rate between the two metrics "
    "was quantified. Both metrics tend to agree in high-dimensional normalised "
    "spaces; Manhattan is slightly more robust to outlier features."
))

story += h3("3.2  Dynamic Time Warping on Raw Heart Rate Sequences")
story.append(body(
    "DTW was applied to the first 20 HeartRate readings per patient (normalised "
    "to zero mean and unit variance). Unlike Euclidean distance, DTW aligns "
    "sequences optimally before measuring similarity, making it more appropriate "
    "for time series that may be shifted or stretched in time. The pairwise DTW "
    "distance matrix was computed for all 500 patients and the class-matching "
    "rate was compared against Euclidean-based neighbours."
))

story += h3("3.3  New Patient Diagnosis via Nearest-Neighbour Prediction")
story.append(body(
    "A new patient presenting with elevated heart rate (98 bpm), high systolic "
    "BP (155 mmHg), reduced blood oxygen (94%), and low sleep (4.5 hours) was "
    "normalised using the training scaler. The top-5 Euclidean nearest neighbours "
    "were identified and the diagnosis was predicted by majority vote. The "
    "confidence was reported as the fraction of neighbours matching the predicted "
    "class. The clinical profile strongly aligns with Hypertension."
))
story.append(Spacer(1, 8))

# ── 4. Supervised Classification ─────────────────────────────────────────────
story += h2("4. Supervised Classification")
story.append(body(
    "All five classifiers were trained on the patient-level feature matrix using "
    "a stratified 80/20 train-test split. Each model was evaluated on accuracy, "
    "macro-averaged precision, recall, F1-score, and a confusion matrix."
))

story += h3("4.1  Decision Tree")
story.append(body(
    "A Decision Tree with entropy criterion was trained and tuned over "
    "max_depth ∈ {2, 4, 6, 8, 10}. The optimal depth was selected by "
    "test accuracy. The tree was visualised to depth 3 and the top-5 "
    "feature importances were extracted."
))
story += fig("C1_dt_depth.png",
    "Figure 5: Test accuracy vs. max_depth. The optimal depth balances "
    "bias and variance — deeper trees overfit while shallow trees underfit.", 0.72)
story += fig("C1_tree_viz.png",
    "Figure 6: Decision Tree visualised to depth 3. Each node displays the "
    "splitting feature, threshold, sample count, and majority class. Top-level "
    "splits are dominated by blood pressure and heart rate statistics.")
story += fig("C1_feature_importance.png",
    "Figure 7: Top-5 feature importances. BP and heart rate features dominate, "
    "consistent with their clinical role in distinguishing the five classes.", 0.72)
story += fig("C1_Decision_Tree_cm.png",
    "Figure 8: Decision Tree confusion matrix. Strong diagonal values indicate "
    "good per-class accuracy across all five diagnosis classes.", 0.6)

story += h3("4.2  Rule-Based Classification")
story.append(body(
    "Twelve clinically-grounded if-then rules were derived from the training "
    "data. Each rule was evaluated for coverage (% of patients it applies to) "
    "and accuracy (% correctly classified under that rule). Example rules: "
    "<i>IF BP_Systolic_mean ≥ 140 THEN Hypertension</i>; "
    "<i>IF HeartRate_std ≥ 18 THEN Arrhythmia</i>. "
    "The rule set provides complete transparency — every prediction is fully "
    "explainable to a clinician."
))
story += fig("C2_rules_cm.png",
    "Figure 9: Rule-based classifier confusion matrix. The rule set trades "
    "some accuracy for full interpretability, making it ideal for clinical "
    "audit and regulatory review.", 0.6)

story += h3("4.3  k-Nearest Neighbour")
story.append(body(
    "kNN was trained on the normalised feature matrix with k tuned over "
    "{1, 3, 5, 7, 9, 11, 15, 21} for both Euclidean and Manhattan metrics. "
    "The train/test accuracy curves were plotted to identify the optimal k. "
    "While effective, kNN's O(n) inference time makes it impractical for "
    "real-time deployment in high-throughput hospital settings."
))
story += fig("C3_knn_accuracy.png",
    "Figure 10: Train and test accuracy vs. k for Euclidean (left) and "
    "Manhattan (right) metrics. Small k overfits; larger k smooths boundaries. "
    "Both metrics yield similar optimal accuracy on this dataset.")
story += fig("C3_kNN_cm.png",
    "Figure 11: kNN confusion matrix for the best k configuration.", 0.6)

story += h3("4.4  Gaussian Naïve Bayes")
story.append(body(
    "Gaussian NB was trained after verifying the Gaussian assumption via "
    "histograms and Q-Q plots for key features. The Pearson correlation matrix "
    "was computed to identify feature pairs that violate the independence "
    "assumption. Despite these violations, NB performs competitively due to "
    "its low variance and fast training."
))
story += fig("C4_gaussian_check.png",
    "Figure 12: Histograms and Q-Q plots for HeartRate_mean, BP_Systolic_mean, "
    "and SleepHours_mean. Mean-aggregated features tend toward normality "
    "(central limit theorem); Q-Q plots confirm approximate Gaussian behaviour.")
story += fig("C4_correlation.png",
    "Figure 13: Pearson correlation heatmap of mean vital sign features. "
    "Strongly correlated pairs (e.g. systolic/diastolic BP) violate the "
    "Naïve Bayes independence assumption.", 0.75)
story += fig("C4_Gaussian_NB_cm.png",
    "Figure 14: Gaussian Naïve Bayes confusion matrix.", 0.6)

story += h3("4.5  Support Vector Machine")
story.append(body(
    "An SVM with One-vs-Rest multi-class strategy was trained. RBF and "
    "Polynomial (degree=3) kernels were compared, with regularisation "
    "parameter C ∈ {0.1, 1, 10, 100} tuned via 5-fold cross-validation. "
    "The decision boundary was visualised in 2D using PCA projection. "
    "SVM achieves high accuracy but lacks interpretability — a significant "
    "trade-off in clinical settings where model reasoning must be auditable."
))
story += fig("C5_SVM_cm.png",
    "Figure 15: SVM confusion matrix for the best kernel and C configuration.", 0.6)
story += fig("C5_svm_boundary.png",
    "Figure 16: SVM decision boundary in 2D PCA space. Each coloured region "
    "represents the predicted diagnosis class. Non-linear boundaries (RBF "
    "kernel) demonstrate SVM's ability to separate complex class structures.", 0.75)

story.append(PageBreak())

# ── 5. Results & Recommendation ───────────────────────────────────────────────
story += h2("5. Results & Deployment Recommendation")
story += fig("Final_comparison.png",
    "Figure 17: Test accuracy comparison across all five classifiers. "
    "SVM and Decision Tree lead in accuracy; Rule-Based and Naïve Bayes "
    "trade accuracy for interpretability and speed.", 0.82)

# Results table
res_data = [
    [Paragraph("<b>Classifier</b>", body_style),
     Paragraph("<b>Accuracy</b>", body_style),
     Paragraph("<b>Interpretable</b>", body_style),
     Paragraph("<b>Inference Speed</b>", body_style),
     Paragraph("<b>Clinical Suitability</b>", body_style)],
    ["Decision Tree",  "High",   "✓ Full",    "Fast",    "★★★★★"],
    ["Rule-Based",     "Medium", "✓ Full",    "Fast",    "★★★★☆"],
    ["kNN",            "High",   "✗ None",    "Slow",    "★★★☆☆"],
    ["Naïve Bayes",    "Medium", "Partial",   "Fastest", "★★★☆☆"],
    ["SVM",            "Highest","✗ None",    "Medium",  "★★★★☆"],
]
res_table = Table(res_data, colWidths=[W*0.22, W*0.14, W*0.18, W*0.18, W*0.28])
res_table.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,0),  ACCENT),
    ('TEXTCOLOR',     (0,0), (-1,0),  colors.white),
    ('FONTNAME',      (0,0), (-1,0),  'Helvetica-Bold'),
    ('FONTSIZE',      (0,0), (-1,-1), 10),
    ('ROWBACKGROUNDS',(0,1), (-1,-1), [colors.white, LGRAY]),
    ('BOX',           (0,0), (-1,-1), 0.5, colors.HexColor('#cccccc')),
    ('INNERGRID',     (0,0), (-1,-1), 0.5, colors.HexColor('#cccccc')),
    ('LEFTPADDING',   (0,0), (-1,-1), 8),
    ('RIGHTPADDING',  (0,0), (-1,-1), 8),
    ('TOPPADDING',    (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('ALIGN',         (0,0), (-1,-1), 'CENTER'),
]))
story += [res_table, Spacer(1, 14)]

story.append(body(
    "For production clinical deployment, the <b>Decision Tree</b> is the "
    "recommended primary classifier. While SVM achieves marginally higher "
    "accuracy, the Decision Tree provides complete transparency — every "
    "prediction can be traced through explicit feature thresholds, which is "
    "essential for regulatory compliance (FDA, CE marking) and clinician trust. "
    "The rule-based system serves as a valuable safety net: its hand-crafted "
    "rules are directly auditable and can be updated by domain experts without "
    "retraining. kNN is well-suited for exploratory patient matching but is "
    "too slow for real-time inference at scale. Gaussian NB is an excellent "
    "fast baseline for resource-constrained environments. A production system "
    "should combine the Decision Tree for primary classification with the "
    "rule-based system for high-confidence edge cases, and should be retrained "
    "periodically as new patient data accumulates."
))

story.append(Spacer(1, 12))
story += [
    HRFlowable(width=W, thickness=1.5, color=ACCENT, spaceAfter=8),
    Paragraph(
        "Built with Python · Pandas · NumPy · Scikit-learn · Statsmodels · "
        "Matplotlib · Seaborn · ReportLab",
        ParagraphStyle('foot', parent=styles['Normal'],
            fontSize=9, alignment=TA_CENTER, textColor=GRAY)
    )
]

doc.build(story)
print(f"Portfolio PDF saved: {OUT}")
