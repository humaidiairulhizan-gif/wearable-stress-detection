#include <math.h>

// Constants based on your Python parameters
const int WINDOW_SIZE = 30;
const int FS_EDA = 4;   // 4 samples per second
const int FS_ACC = 32;  // 32 samples per second
const int EDA_COUNT = WINDOW_SIZE * FS_EDA; // 120 samples
const int ACC_COUNT = WINDOW_SIZE * FS_ACC; // 960 samples

// Arrays to hold the window data (to be filled by sensors)
float eda_buffer[EDA_COUNT];
float acc_x[ACC_COUNT], acc_y[ACC_COUNT], acc_z[ACC_COUNT];

void processAndPredict() {
    // 1. Calculate Mean EDA
    float sum_eda = 0;
    for(int i=0; i<EDA_COUNT; i++) sum_eda += eda_buffer[i];
    float mean_eda = sum_eda / EDA_COUNT;

    // 2. Calculate STD EDA
    float sq_sum_eda = 0;
    for(int i=0; i<EDA_COUNT; i++) sq_sum_eda += pow(eda_buffer[i] - mean_eda, 2);
    float std_eda = sqrt(sq_sum_eda / EDA_COUNT);

    // 3. Calculate EDA Slope
    float eda_slope = eda_buffer[EDA_COUNT - 1] - eda_buffer[0];

    // 4. Calculate ACC Magnitude Mean and Variance
    float sum_mag = 0;
    float magnitudes[ACC_COUNT];
    for(int i=0; i<ACC_COUNT; i++) {
        magnitudes[i] = sqrt(pow(acc_x[i], 2) + pow(acc_y[i], 2) + pow(acc_z[i], 2));
        sum_mag += magnitudes[i];
    }
    float mean_acc = sum_mag / ACC_COUNT;

    float sq_sum_acc = 0;
    for(int i=0; i<ACC_COUNT; i++) sq_sum_acc += pow(magnitudes[i] - mean_acc, 2);
    float var_acc = sq_sum_acc / ACC_COUNT;

    // 5. Final Prediction
    int state = predictState(mean_eda, std_eda, mean_acc, var_acc, eda_slope);

    // Output result
    if(state == 0) Serial.println("STRESS DETECTED - Triggering Vibration");
    else if(state == 1) Serial.println("Amusement/Exertion Detected");
    else Serial.println("State: Calm/Meditation");
}
