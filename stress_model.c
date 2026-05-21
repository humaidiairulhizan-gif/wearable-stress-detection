#include "stress_model.h"

int predictState(float mean_eda,
                 float std_eda,
                 float mean_acc,
                 float var_acc,
                 float eda_slope)
{
    if (std_eda <= 0.05) {
        if (mean_acc <= 0.12) {
            return 2; // Meditation
        } else {
            return 1; // Amusement
        }
    } else {
        if (eda_slope > 0.01) {
            if (var_acc <= 0.08) {
                return 0; // Stress
            } else {
                return 1; // Amusement / exertion
            }
        } else {
            return 2; // Baseline calm
        }
    }
}
