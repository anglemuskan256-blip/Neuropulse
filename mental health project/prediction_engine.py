"""
prediction_engine.py
────────────────────
Pure Python prediction logic — NO Flask dependency.
Used by streamlit_app.py so Streamlit Cloud doesn't need Flask installed.
"""

import os
import sys
from pathlib import Path

# ── Path setup ────────────────────────────────────────────────────────────────
_project_root = Path(__file__).parent
sys.path.insert(0, str(_project_root))

# ── Recommendation Engine (pure Python, no Flask) ─────────────────────────────
from utils.recommendation_engine import RecommendationEngine

_rec_engine = RecommendationEngine()


# ═══════════════════════════════════════════════════════════════════════════════
#  FEATURE ENGINEERING
# ═══════════════════════════════════════════════════════════════════════════════

def _compute_engineered_features(data: dict) -> dict:
    features = data.copy()
    features['HR_HRV_Ratio']    = float(data['Heart_Rate']) / (float(data['HRV']) + 1)
    features['BP_Average']      = (float(data['BP_Systolic']) + float(data['BP_Diastolic'])) / 2
    features['BP_Diff']         = float(data['BP_Systolic']) - float(data['BP_Diastolic'])
    features['Psych_Score']     = float(data['Cognitive_State']) + float(data['Emotional_State'])
    features['HR_Resp_Ratio']   = float(data['Heart_Rate']) / (float(data['Respiration']) + 0.1)
    features['Temp_Deviation']  = abs(float(data['Skin_Temp']) - 36.5)
    features['HRV_Norm']        = float(data['HRV']) / 500.0
    features['HR_Variability']  = features['HR_HRV_Ratio'] * features['Psych_Score']
    return features


# ═══════════════════════════════════════════════════════════════════════════════
#  RULE-BASED STRESS PREDICTION  (identical logic to app_enhanced.py)
# ═══════════════════════════════════════════════════════════════════════════════

def predict_stress(input_data: dict) -> dict:
    """
    Predict stress level from raw biometric inputs.
    Returns a dict with stress_level, condition, mental_load_index,
    recommendation, and recommendations.
    """
    try:
        _compute_engineered_features(input_data)   # validate fields exist

        # ── Psychological classification ──────────────────────────────────────
        def _psych_status(d):
            c = int(float(d.get('Cognitive_State', 3)))
            e = int(float(d.get('Emotional_State', 3)))
            if c in (1, 2) and e in (1, 2):   return 'Calm'
            if c == 3      and e == 3:         return 'Moderate'
            if c in (4, 5) and e in (4, 5):   return 'Stressed'
            return 'Moderate'

        psych = _psych_status(input_data)

        # ── Physiological scoring ─────────────────────────────────────────────
        highs = moderates = normals = 0

        hr = float(input_data.get('Heart_Rate', 75))
        if hr <= 100:             normals   += 1
        elif 101 <= hr <= 115:    moderates += 1
        else:                     highs     += 1

        hrv = float(input_data.get('HRV', 50))
        if hrv >= 50:             normals   += 1
        elif 30 <= hrv < 50:      moderates += 1
        else:                     highs     += 1

        resp = float(input_data.get('Respiration', 16))
        if 12 <= resp <= 20:      normals   += 1
        elif 21 <= resp <= 24:    moderates += 1
        elif resp > 24:           highs     += 1
        else:                     normals   += 1

        temp = float(input_data.get('Skin_Temp', 36.5))
        if 36.1 <= temp <= 37.2:                      normals   += 1
        elif 35.5 <= temp < 36.1 or 37.3 <= temp <= 38.0: moderates += 1
        else:                                          highs     += 1

        bp_sys = float(input_data.get('BP_Systolic', 120))
        if 90 <= bp_sys <= 120:   normals   += 1
        elif 121 <= bp_sys <= 140: moderates += 1
        else:                     highs     += 1

        bp_dia = float(input_data.get('BP_Diastolic', 80))
        if 60 <= bp_dia <= 80:    normals   += 1
        elif 81 <= bp_dia <= 90:  moderates += 1
        else:                     highs     += 1

        # ── Final condition ───────────────────────────────────────────────────
        if psych == 'Stressed' or highs >= 2:
            final_condition = 'Stressed'
        elif psych == 'Calm' and normals >= 4:
            final_condition = 'Calm'
        else:
            final_condition = 'Moderate'

        # ── Stress level label ────────────────────────────────────────────────
        if final_condition == 'Calm':
            stress_level = 'Low';           recommend_key = 0
        elif final_condition == 'Moderate':
            if highs >= 1 or moderates >= 2:
                stress_level = 'Moderate-High'; recommend_key = 2
            else:
                stress_level = 'Moderate-Low';  recommend_key = 2
        else:
            stress_level = 'High';          recommend_key = 3

        # ── Mental Load Index ─────────────────────────────────────────────────
        metric_points = (moderates * 1) + (highs * 2)
        psych_points  = 0 if psych == 'Calm' else (1 if psych == 'Moderate' else 2)
        normalized    = (metric_points + psych_points) / 14.0
        raw_score     = normalized * 100.0

        if final_condition == 'Calm':
            mli = int(max(0,  min(30,  round(5  + raw_score * 0.25))))
        elif final_condition == 'Moderate':
            mli = int(max(31, min(70,  round(31 + raw_score * 0.39))))
        else:
            mli = int(max(71, min(100, round(71 + raw_score * 0.29))))
        mli = max(0, min(100, mli))

        # ── Advisory text ─────────────────────────────────────────────────────
        _advisories = {
            0: {'title': '✓ Maintain Current State',
                'primary': "You're managing stress well — keep it up!",
                'actions': ['✓ Continue regular exercise',
                            '✓ Maintain your sleep schedule',
                            '✓ Keep healthy eating habits']},
            1: {'title': '⚠ Light Stress Management',
                'primary': 'Minor stress detected. Take preventive steps.',
                'actions': ['→ Take 5-10 minute breaks every hour',
                            '→ Practice deep breathing (4-7-8 technique)',
                            '→ Go for a short walk']},
            2: {'title': '⚠ Moderate Stress Response',
                'primary': 'Noticeable stress. Implement stress management.',
                'actions': ['→ Try meditation (10-15 minutes)',
                            '→ Do light exercise or yoga',
                            '→ Connect with friends or family',
                            '→ Take a warm shower or bath']},
            3: {'title': '🚨 High Stress Alert',
                'primary': 'High stress detected. Seek help if this persists.',
                'actions': ['→ Consider talking to a counselor',
                            '→ Practice intensive relaxation techniques',
                            '→ Medical consultation may be recommended',
                            '→ Avoid additional stressful activities']},
        }
        recommendation = _advisories.get(recommend_key, {})

        # ── Full recommendations (tiered) ─────────────────────────────────────
        rec_key = ('Low' if final_condition == 'Calm'
                   else 'High' if final_condition == 'Stressed'
                   else 'Moderate')
        full_recs = _rec_engine.generate_recommendations(rec_key, mli)

        return {
            'stress_level':     stress_level,
            'condition':        final_condition,
            'mental_load_index': mli,
            'recommendation':   recommendation,
            'recommendations': {
                'natural_interventions': full_recs.get('natural_interventions', []),
                'otc_options':           full_recs.get('otc_options', []),
                'professional_services': full_recs.get('professional_services', []),
            },
        }

    except Exception as e:
        return {'error': str(e)}
