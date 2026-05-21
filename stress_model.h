#ifndef STRESS_MODEL_H
#define STRESS_MODEL_H

/*
 * ESP32 Stress Detection Logic
 * Result:
 * 0 = Stress
 * 1 = Amusement
 * 2 = Meditation
 */

int predictState(float mean_eda,
                 float std_eda,
                 float mean_acc,
                 float var_acc,
                 float eda_slope);

#endif  // STRESS_MODEL_H
