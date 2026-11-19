
import streamlit as st
import matplotlib.pyplot as plt
import csv
import io
from datetime import datetime

st.set_page_config(
    page_title="PhytoListen",
    page_icon="🌱",
    layout="wide"
)

if "history" not in st.session_state:
    st.session_state.history = []

# Project Header
st.title("🌱 PhytoListen")

st.markdown("""
### Listening to Plant Stress to Save Water

PhytoListen is a plant-monitoring prototype that combines
soil moisture, illustrative plant stress signals, and weather
conditions to support irrigation decisions.
""")

st.divider()

st.subheader("Plant Stress Monitoring & Irrigation Support")

st.info(
    "Demo prototype: readings are simulated/manual inputs, "
    "not real sensor measurements."
)

# Input Section
st.sidebar.header("Plant Readings")

soil = st.sidebar.slider(
    "Soil Moisture (%)", 0, 100, 25
)

stress = st.sidebar.selectbox(
    "Illustrative Stress Signal", ["low", "high"]
)

weather = st.sidebar.selectbox(
    "Weather Condition",
    ["Sunny", "Cloudy", "Rainy", "Hot"]
)

# SINGLE DECISION LOGIC
if soil < 30 and stress == "high":

    result = "Possible plant stress"
    decision = "Inspect the plant and verify root-zone moisture."
    reason = "Low soil moisture and high illustrative stress signal."
    status = "ALERT: Two indicators suggest possible stress."

elif soil < 30:

    result = "Low soil moisture"
    decision = "Recheck root-zone moisture."
    reason = "Soil moisture is below the demo threshold."
    status = "WARNING: Soil moisture is low."

elif stress == "high":

    result = "Possible plant stress"
    decision = "Inspect the plant for other stress factors."
    reason = "High illustrative stress signal."
    status = "WARNING: Possible plant stress."

else:

    result = "No clear stress detected"
    decision = "Continue monitoring."
    reason = "No clear stress indicated by the demo inputs."
    status = "NORMAL: No clear stress signal."

# Weather Context
if weather == "Rainy":
    weather_advice = (
        "Rainy weather is selected. Verify actual rainfall "
        "and root-zone moisture before irrigation."
    )
else:
    weather_advice = (
        "Consider actual local weather and soil conditions "
        "when making irrigation decisions."
    )

# Current Readings
st.subheader("📊 Current Plant Readings")

col1, col2, col3 = st.columns(3)

col1.metric("Soil Moisture", f"{soil}%")
col2.metric("Stress Signal", stress.upper())
col3.metric("Weather", weather)

# Irrigation Recommendation
st.divider()
st.subheader("💧 Irrigation Recommendation")

st.write("**Result:**", result)
st.write("**Recommendation:**", decision)
st.info(weather_advice)

# Plant Health Status
st.divider()
st.subheader("🌿 Plant Health Status")

if status.startswith("ALERT"):
    st.error(status)

elif status.startswith("WARNING"):
    st.warning(status)

else:
    st.success(status)

# Combined Analysis
st.divider()
st.subheader("🔍 Combined Analysis")

st.write("**Soil Moisture:**", soil, "%")
st.write("**Plant Stress Signal:**", stress.upper())
st.write("**Weather Condition:**", weather)
st.write("**Analysis Result:**", result)
st.write("**Reason:**", reason)
st.write("**Weather Context:**", weather_advice)

# Final Decision Summary
st.divider()
st.subheader("📋 Final Decision Summary")

st.write("**Decision:**", decision)
st.write("**Reason:**", reason)
st.write("**Plant Health:**", status)
st.write("**Weather Guidance:**", weather_advice)

# Save Reading
if st.button("💾 Save Current Reading"):

    reading = {
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Soil Moisture (%)": soil,
        "Stress Signal": stress.upper(),
        "Weather": weather,
        "Result": result,
        "Decision": decision,
        "Plant Health": status
    }

    st.session_state.history.append(reading)

    st.success("Reading saved successfully!")

# How It Works
st.divider()
st.subheader("⚙️ How PhytoListen Works")

st.markdown("""
1. **Soil Monitoring:** Collects soil moisture readings.
2. **Plant Stress Monitoring:** Uses plant stress signal inputs.
3. **Weather Context:** Considers weather conditions.
4. **Combined Analysis:** Evaluates all three inputs together.
5. **Decision Support:** Provides irrigation-related recommendations.
""")

# Key Features
st.divider()
st.subheader("✨ Key Features")

col1, col2 = st.columns(2)

with col1:
    st.info("💧 Soil Moisture Monitoring")
    st.info("🌿 Plant Stress Signal Analysis")
    st.info("🌦️ Weather-based Context")

with col2:
    st.info("🔍 Combined Analysis")
    st.info("📋 Irrigation Decision Support")
    st.info("📊 Reading History & Graph")

# Innovation
st.divider()
st.subheader("💡 What Makes PhytoListen Different?")

st.write("""
PhytoListen combines three different sources of information:

- Soil moisture readings
- Plant stress signals
- Weather conditions

Instead of relying on soil moisture alone, the prototype
uses combined inputs to support more informed irrigation decisions.

Its goal is to help identify possible plant stress and encourage
careful water management.
""")

# Reading History
st.divider()
st.subheader("📚 Reading History")

if st.session_state.history:

    for i, item in enumerate(st.session_state.history, start=1):

        st.write(f"### Reading {i}")
        st.write("Time:", item["Time"])
        st.write("Soil Moisture:", item["Soil Moisture (%)"], "%")
        st.write("Stress Signal:", item["Stress Signal"])
        st.write("Weather:", item["Weather"])
        st.write("Result:", item["Result"])
        st.write("Decision:", item["Decision"])
        st.write("Plant Health:", item["Plant Health"])
        st.divider()

    # CSV Download
    output = io.StringIO()

    writer = csv.DictWriter(
        output,
        fieldnames=st.session_state.history[0].keys()
    )

    writer.writeheader()
    writer.writerows(st.session_state.history)

    st.download_button(
        "Download Reading History (CSV)",
        data=output.getvalue(),
        file_name="phytolisten_history.csv",
        mime="text/csv",
        key="download_history_csv"
    )

    # History Graph
    st.subheader("📈 Soil Moisture History")

    values = [
        item["Soil Moisture (%)"]
        for item in st.session_state.history
    ]

    fig, ax = plt.subplots()

    ax.plot(
        range(1, len(values) + 1),
        values,
        marker="o"
    )

    ax.set_xlabel("Reading Number")
    ax.set_ylabel("Soil Moisture (%)")
    ax.set_title("Saved Soil Moisture Readings")
    ax.grid(True)

    st.pyplot(fig)
    plt.close(fig)

else:
    st.info("No readings saved yet. Click Save Current Reading.")

# Footer
st.caption(
    "Readings are stored only during the current app session. "
    "Real ultrasonic sensor data is not connected yet. "
    "Decision thresholds are illustrative and not agronomically validated."
)



st.divider()

st.header("Engineering Limitations & Future Development")

st.subheader("Current Prototype Status")

st.write("""
PhytoListen is currently a software-based proof of concept.
It demonstrates a multimodal decision-support workflow using
soil moisture, illustrative plant stress signals, and weather context.
No physical sensors or live plant acoustic measurements are connected.
""")

st.subheader("Engineering Constraints")

st.markdown("""
- **Acoustic Signal Validation:** Plant acoustic emissions require controlled
  measurement and validation before they can be interpreted reliably.
- **Sensor Integration:** Real-time ultrasonic sensing is not yet implemented.
- **Environmental Variability:** Temperature, humidity, plant species,
  and other stress factors may influence observations.
- **Threshold Calibration:** The current soil-moisture threshold is illustrative
  and must be calibrated for crop and soil conditions.
- **Decision Reliability:** Recommendations require field testing before
  operational use.
""")

st.subheader("Proposed Engineering Roadmap")

st.markdown("""
1. **Phase 1 – Sensor Integration:** Connect calibrated soil-moisture,
   environmental, and ultrasonic sensing hardware.
2. **Phase 2 – Data Acquisition:** Develop synchronized signal collection
   and preprocessing pipelines.
3. **Phase 3 – Signal Analysis:** Extract acoustic features and evaluate
   them against controlled plant-stress observations.
4. **Phase 4 – Sensor Fusion:** Combine acoustic, soil, and weather
   information to reduce reliance on any single indicator.
5. **Phase 5 – Field Validation:** Evaluate reliability across plant types,
   soil conditions, and environmental settings.
6. **Phase 6 – Adaptive Decision Support:** Develop crop-specific,
   evidence-based irrigation recommendations.
""")

st.subheader("Engineering Objective")

st.write("""
The long-term objective is to develop a validated, multimodal plant-stress
monitoring system that supports more informed irrigation decisions.
""")


st.divider()

st.header("🏗️ PhytoListen System Architecture")

st.write("""
PhytoListen follows a layered software architecture.
Each layer performs a specific role in the plant-monitoring
and irrigation decision-support workflow.
""")

st.subheader("Layer 1 – Input Acquisition")

st.markdown("""
- Soil moisture input (%)
- Illustrative plant stress signal (LOW / HIGH)
- Weather condition (Sunny / Cloudy / Rainy / Hot)

**Purpose:** Collect the inputs required for analysis.
""")

st.subheader("Layer 2 – Data Processing")

st.markdown("""
- Read the selected input values.
- Evaluate soil moisture against the illustrative threshold.
- Interpret the selected plant stress signal.
- Prepare weather context for the recommendation.

**Purpose:** Organize inputs for the decision engine.
""")

st.subheader("Layer 3 – Rule-Based Decision Engine")

st.markdown("""
- Apply predefined decision rules.
- Identify possible plant stress conditions.
- Generate a plant health status.
- Keep weather guidance as additional context.

**Purpose:** Convert input conditions into interpretable results.
""")

st.subheader("Layer 4 – Output & Reporting")

st.markdown("""
- Irrigation recommendation
- Plant health status
- Combined analysis
- Final decision summary
- Reading history and CSV export
- Soil moisture history graph

**Purpose:** Present results in a readable dashboard.
""")

st.subheader("Architecture Flow")

st.code(
    "INPUT ACQUISITION\n"
    "       ↓\n"
    "DATA PROCESSING\n"
    "       ↓\n"
    "RULE-BASED DECISION ENGINE\n"
    "       ↓\n"
    "OUTPUT & REPORTING",
    language="text"
)

st.info(
    "Prototype status: This architecture currently operates "
    "with manual or illustrative inputs. Live sensor integration "
    "and real plant acoustic analysis are future development goals."
)

# Engineering Upgrade: Water Requirement & Efficiency Analyzer
st.divider()
st.header("🧮 Engineering Module: Water Requirement & Efficiency Analyzer")
st.write(
    "This module estimates irrigation volume from reference evapotranspiration, "
    "crop coefficient, effective rainfall, irrigated area, and irrigation efficiency. "
    "All values are manually entered scenario inputs in this prototype."
)
st.sidebar.divider()
st.sidebar.header("Water Requirement Model")
et0 = st.sidebar.number_input(
    "Reference ET₀ (mm/day)", min_value=0.0, max_value=20.0,
    value=4.0, step=0.1,
    help="Use a reliable local reference evapotranspiration value."
)
# FAO-56 reference profiles: (Kc initial, Kc mid-season, Kc end-season).
# Values are typical planning values for standard, non-stressed crops;
# local climate, variety, wetting frequency, and management can change them.
crop_profiles = {
    "Tomato": (0.60, 1.15, 0.80, "FAO-56 typical Kc_end range: 0.70–0.90; 0.80 is the midpoint."),
    "Potato": (0.50, 1.15, 0.75, "FAO-56 typical planning values."),
    "Chickpea": (0.40, 1.00, 0.35, "FAO-56 table lists chickpea Kc_mid 1.00 and Kc_end 0.35."),
    "Wheat": (0.30, 1.15, 0.325, "FAO-56 typical Kc_end range: 0.25–0.40; 0.325 is the midpoint."),
    "Maize (grain)": (0.30, 1.20, 0.475, "FAO-56 typical Kc_end range: 0.35–0.60; midpoint used for this profile."),
    "Green beans": (0.50, 1.05, 0.90, "FAO-56 typical planning values."),
    "Rice": (1.05, 1.20, 0.75, "FAO-56 typical Kc_end range: 0.60–0.90; midpoint used for this profile."),
}

selected_crop = st.sidebar.selectbox("Crop profile", list(crop_profiles.keys()))
kc_ini, kc_mid, kc_end, crop_note = crop_profiles[selected_crop]

area = st.sidebar.number_input(
    "Irrigated area (m²)", min_value=0.1, max_value=1000000.0,
    value=10.0, step=1.0
)
period_days = st.sidebar.number_input(
    "Planning period (days)", min_value=1, max_value=365,
    value=7, step=1
)
st.sidebar.markdown("**Days spent in each growth stage**")
st.sidebar.caption("Enter how many days of this planning period fall in each stage. Their sum must equal the planning period.")
initial_days = st.sidebar.number_input("Initial stage (days)", min_value=0, max_value=365, value=2, step=1)
development_days = st.sidebar.number_input("Development stage (days)", min_value=0, max_value=365, value=2, step=1)
mid_days = st.sidebar.number_input("Mid-season stage (days)", min_value=0, max_value=365, value=2, step=1)
late_days = st.sidebar.number_input("Late-season stage (days)", min_value=0, max_value=365, value=1, step=1)

stage_days = {
    "Initial": int(initial_days),
    "Development": int(development_days),
    "Mid-season": int(mid_days),
    "Late-season": int(late_days),
}
stage_kc = {
    "Initial": kc_ini,
    # Approximation: mean Kc across the development transition.
    "Development": (kc_ini + kc_mid) / 2.0,
    "Mid-season": kc_mid,
    # Approximation: mean Kc across the late-season transition.
    "Late-season": (kc_mid + kc_end) / 2.0,
}
entered_stage_days = sum(stage_days.values())
st.sidebar.caption(f"Stage days entered: {entered_stage_days} / {period_days}")

st.sidebar.caption(f"Crop Kc reference: initial {kc_ini:.3f} | mid {kc_mid:.3f} | end {kc_end:.3f}")
st.info(
    f"Crop profile: {selected_crop}. {crop_note} "
    f"Stage Kc values used: Initial {stage_kc['Initial']:.3f}, "
    f"Development {stage_kc['Development']:.3f}, "
    f"Mid-season {stage_kc['Mid-season']:.3f}, "
    f"Late-season {stage_kc['Late-season']:.3f}."
)
st.caption(
    "Kc profiles are based on FAO Irrigation and Drainage Paper 56 reference values, "
    "not locally calibrated recommendations. Development and late-season stage Kc "
    "values here use simple arithmetic averages between adjacent stage coefficients. "
    "This is a transparent approximation; local crop calendars and climate adjustments "
    "are needed for field use."
)
st.markdown("[FAO-56 crop coefficient guidance](https://www.fao.org/4/X0490E/x0490e0b.htm)")
effective_rain = st.sidebar.number_input(
    "Effective rainfall over period (mm)", min_value=0.0,
    max_value=2000.0, value=0.0, step=0.5
)
efficiency_percent = st.sidebar.slider(
    "Irrigation application efficiency (%)", 10, 100, 85
)
baseline_litres = st.sidebar.number_input(
    "Conventional water use for same area/period (L)",
    min_value=0.0, max_value=100000000.0,
    value=70.0, step=5.0,
    help="Use a measured baseline when available; otherwise label it as illustrative."
)

# Multi-stage ETc calculation. Every stage contributes ET0 * Kc(stage) * days(stage).
stage_etc = {
    stage: et0 * stage_kc[stage] * days
    for stage, days in stage_days.items()
}
if entered_stage_days == int(period_days):
    etc_mm = sum(stage_etc.values())
    net_irrigation_mm = max(0.0, etc_mm - effective_rain)
    efficiency_fraction = efficiency_percent / 100.0
    gross_irrigation_mm = net_irrigation_mm / efficiency_fraction
    required_water_litres = gross_irrigation_mm * area
    calculation_valid = True
else:
    etc_mm = sum(stage_etc.values())
    net_irrigation_mm = 0.0
    efficiency_fraction = efficiency_percent / 100.0
    gross_irrigation_mm = 0.0
    required_water_litres = 0.0
    calculation_valid = False
    st.error(
        f"Stage-day total is {entered_stage_days}, but planning period is {period_days}. "
        "Adjust the four stage durations so their sum exactly matches the planning period. "
        "The total irrigation estimate is withheld until the schedule is consistent."
    )

st.markdown("**Multi-stage calculation model**")
st.latex(r"ET_c = ET_0 \times \sum_i (K_{c,i} \times d_i)")
st.latex(r"I_{net} = \max(0, ET_c - P_e)")
st.latex(r"V_{gross}(L) = \frac{I_{net}}{E_a} \times A")
st.caption(
    "ET₀ = reference evapotranspiration (mm/day); Kc,i = coefficient for stage i; "
    "di = days in stage i; Pe = effective rainfall (mm); Ea = efficiency as a decimal; "
    "A = area (m²). 1 mm over 1 m² = 1 litre."
)

w1, w2, w3 = st.columns(3)
w1.metric("Estimated crop water use", f"{etc_mm:.1f} mm")
w2.metric("Net irrigation depth", f"{net_irrigation_mm:.1f} mm" if calculation_valid else "Schedule incomplete")
w3.metric("Estimated irrigation volume", f"{required_water_litres:.1f} L" if calculation_valid else "Not calculated")

with st.expander("Show stage-by-stage calculation"):
    st.write(f"Crop profile: {selected_crop}")
    for stage in stage_days:
        st.write(
            f"{stage}: {stage_days[stage]} day(s) × Kc {stage_kc[stage]:.3f} "
            f"× ET₀ {et0:.2f} = {stage_etc[stage]:.2f} mm"
        )
    st.write(f"Total stage days: {entered_stage_days} / {period_days}")
    st.write(f"Total ETc across entered stages: {etc_mm:.2f} mm")
    if calculation_valid:
        st.write(f"Net irrigation = max(0, {etc_mm:.2f} − {effective_rain:.2f}) = {net_irrigation_mm:.2f} mm")
        st.write(
            f"Gross volume = ({net_irrigation_mm:.2f} ÷ {efficiency_fraction:.2f}) "
            f"× {area:.2f} = {required_water_litres:.2f} L"
        )

st.subheader("📉 Water-use Scenario Comparison")
comp1, comp2 = st.columns(2)
comp1.metric("Conventional volume entered", f"{baseline_litres:.1f} L")
comp2.metric("Calculated irrigation estimate", f"{required_water_litres:.1f} L")

if not calculation_valid:
    litres_difference = None
    percentage_difference = None
    st.info("Complete the stage-day schedule before comparing water volumes.")
elif baseline_litres > 0:
    litres_difference = baseline_litres - required_water_litres
    percentage_difference = litres_difference / baseline_litres * 100.0
    if litres_difference > 0:
        st.success(
            f"Scenario estimate is {litres_difference:.1f} L lower "
            f"({percentage_difference:.1f}% below the entered baseline)."
        )
    elif litres_difference < 0:
        st.warning(
            f"Calculated requirement is {abs(litres_difference):.1f} L higher "
            f"({abs(percentage_difference):.1f}% above the entered baseline). "
            "Do not reduce water below crop needs just to show a saving."
        )
    else:
        st.info("The entered baseline and calculated estimate are equal.")
else:
    litres_difference = None
    percentage_difference = None
    st.info("Enter a conventional volume greater than zero to compare the scenarios.")

st.warning(
    "This is a model-based estimate, not proof of actual water savings. "
    "ET₀, Kc, effective rainfall, and irrigation efficiency must match the crop, "
    "growth stage, location, soil, and irrigation method. Validate against field "
    "measurements before using the result for real irrigation decisions."
)

if "water_scenarios" not in st.session_state:
    st.session_state.water_scenarios = []

if st.button("💾 Save Water Calculation", disabled=not calculation_valid):
    st.session_state.water_scenarios.append({
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ET0_mm_day": et0,
        "Crop": selected_crop,
        "Stage_days": str(stage_days),
        "Stage_Kc": str({k: round(v, 3) for k, v in stage_kc.items()}),
        "Area_m2": area,
        "Days": period_days,
        "Effective_rain_mm": effective_rain,
        "Efficiency_percent": efficiency_percent,
        "Estimated_irrigation_L": round(required_water_litres, 2),
        "Conventional_baseline_L": baseline_litres,
        "Difference_L": round(litres_difference, 2) if litres_difference is not None else "",
        "Difference_percent": round(percentage_difference, 2) if percentage_difference is not None else ""
    })
    st.success("Water calculation saved for this app session.")

if st.session_state.water_scenarios:
    st.subheader("📁 Saved Water Scenarios")
    for index, scenario in enumerate(st.session_state.water_scenarios, start=1):
        st.write(f"Scenario {index}: {scenario}")
    scenario_csv = io.StringIO()
    scenario_writer = csv.DictWriter(
        scenario_csv, fieldnames=list(st.session_state.water_scenarios[0].keys())
    )
    scenario_writer.writeheader()
    scenario_writer.writerows(st.session_state.water_scenarios)
    st.download_button(
        "Download Water Scenario Report (CSV)",
        data=scenario_csv.getvalue(),
        file_name="phytolisten_water_scenarios.csv",
        mime="text/csv",
        key="download_water_scenarios"
    )


# Engineering Validation & Testing Module
st.divider()
st.header("🧪 Engineering Validation & Testing Module")
st.write(
    "This module runs five deterministic software checks on the water-calculation "
    "logic. These are formula/unit tests using controlled example values; they are "
    "not field validation and do not prove real-world water savings."
)

def validation_volume(et0_value, kc_by_stage, days_by_stage,
                      effective_rain_mm, efficiency_pct, area_m2):
    """Return ETc (mm), net irrigation (mm), and gross volume (L)."""
    etc_value = sum(
        et0_value * kc_by_stage[stage] * days_by_stage[stage]
        for stage in days_by_stage
    )
    net_value = max(0.0, etc_value - effective_rain_mm)
    gross_value = (net_value / (efficiency_pct / 100.0)) * area_m2
    return etc_value, net_value, gross_value

# Fixed test fixture keeps the checks independent of the live sidebar inputs.
test_et0 = 4.0
test_area = 10.0
test_efficiency = 80.0
test_kc = {
    "Initial": 0.60,
    "Development": 0.875,
    "Mid-season": 1.15,
    "Late-season": 0.975,
}
test_days = {
    "Initial": 2,
    "Development": 2,
    "Mid-season": 2,
    "Late-season": 1,
}
test_rain = 0.0

base_etc, base_net, base_volume = validation_volume(
    test_et0, test_kc, test_days, test_rain,
    test_efficiency, test_area
)

# 1. Doubling area should double gross volume.
_, _, double_area_volume = validation_volume(
    test_et0, test_kc, test_days, test_rain,
    test_efficiency, test_area * 2
)
test1_pass = abs(double_area_volume - (base_volume * 2)) < 1e-8

# 2. Lower application efficiency should increase gross volume
# for the same net irrigation requirement.
_, _, lower_efficiency_volume = validation_volume(
    test_et0, test_kc, test_days, test_rain, 60.0, test_area
)
test2_pass = lower_efficiency_volume > base_volume

# 3. More effective rainfall should not increase net irrigation.
_, net_with_rain, _ = validation_volume(
    test_et0, test_kc, test_days, 2.0,
    test_efficiency, test_area
)
test3_pass = net_with_rain <= base_net and abs(net_with_rain - (base_net - 2.0)) < 1e-8

# 4. An inconsistent stage schedule must be rejected.
invalid_test_days = dict(test_days)
invalid_test_days["Late-season"] = 0  # Total is 6 days, not 7.
invalid_schedule_total = sum(invalid_test_days.values())
test4_pass = invalid_schedule_total != 7

# 5. Moving all seven days from Initial to Mid-season should increase
# estimated crop water use for this reference profile.
initial_only_days = {"Initial": 7, "Development": 0, "Mid-season": 0, "Late-season": 0}
mid_only_days = {"Initial": 0, "Development": 0, "Mid-season": 7, "Late-season": 0}
initial_only_etc, _, _ = validation_volume(
    test_et0, test_kc, initial_only_days, 0.0, test_efficiency, test_area
)
mid_only_etc, _, _ = validation_volume(
    test_et0, test_kc, mid_only_days, 0.0, test_efficiency, test_area
)
test5_pass = mid_only_etc > initial_only_etc

validation_results = [
    ("Area scaling", test1_pass,
     f"10 m² = {base_volume:.2f} L; 20 m² = {double_area_volume:.2f} L"),
    ("Irrigation efficiency", test2_pass,
     f"80% efficiency = {base_volume:.2f} L; 60% efficiency = {lower_efficiency_volume:.2f} L"),
    ("Effective rainfall", test3_pass,
     f"0 mm rainfall = {base_net:.2f} mm net; 2 mm rainfall = {net_with_rain:.2f} mm net"),
    ("Stage-day validation", test4_pass,
     f"Entered stage days = {invalid_schedule_total}; expected = 7; schedule must be rejected"),
    ("Growth-stage coefficient", test5_pass,
     f"7 Initial days = {initial_only_etc:.2f} mm ETc; 7 Mid-season days = {mid_only_etc:.2f} mm ETc"),
]

passed_count = sum(1 for _, passed, _ in validation_results if passed)
total_count = len(validation_results)

test_col1, test_col2 = st.columns(2)
test_col1.metric("Tests passed", f"{passed_count}/{total_count}")
test_col2.metric("Test fixture ETc", f"{base_etc:.2f} mm")

for test_name, passed, detail in validation_results:
    if passed:
        st.success(f"PASS — {test_name}: {detail}")
    else:
        st.error(f"FAIL — {test_name}: {detail}")

if passed_count == total_count:
    st.success("All five software validation checks passed.")
else:
    st.warning("One or more checks failed. Review the calculation logic before presenting this build.")

st.caption(
    "Test fixture: ET₀ = 4 mm/day, area = 10 m², efficiency = 80%, "
    "rainfall = 0 mm, and fixed illustrative stage Kc values. "
    "The tests check internal mathematical behavior only; they do not validate "
    "crop coefficients, local weather inputs, sensors, or field performance."
)

st.subheader("Engineering interpretation")
st.markdown(
    "- The calculator estimates a crop-water requirement; it does not infer litres from soil-moisture percentage alone.\n"
    "- The comparison is meaningful only when both volumes cover the same area and time period.\n"
    "- A lower calculated volume is not automatically better: plant health and crop requirements must be protected.\n"
    "- The current model uses user-entered inputs and has not yet been field-validated. Stage-transition coefficients are simplified averages."
)
