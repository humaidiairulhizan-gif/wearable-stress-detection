#include <stdio.h>
#include <math.h>
#include "feature_extraction.h"

#define WINDOW_SIZE 30
#define FS_EDA 4
#define FS_ACC 32
#define EDA_COUNT (WINDOW_SIZE * FS_EDA)
#define ACC_COUNT (WINDOW_SIZE * FS_ACC)

float eda_buffer[EDA_COUNT];
float acc_x[ACC_COUNT];
float acc_y[ACC_COUNT];
float acc_z[ACC_COUNT];

int predictState(float mean_eda, float std_eda,
                 float mean_acc, float var_acc,
                 float eda_slope);

void processAndPredict()
{
    float sum_eda = 0;
    for (int i = 0; i < EDA_COUNT; i++){
        sum_eda += eda_buffer[i];}

    float mean_eda = sum_eda / EDA_COUNT;

    float sq_sum_eda = 0;
    for (int i = 0; i < EDA_COUNT; i++)
        sq_sum_eda += pow(eda_buffer[i] - mean_eda, 2);

    float std_eda = sqrt(sq_sum_eda / EDA_COUNT);
    float eda_slope = eda_buffer[EDA_COUNT - 1] - eda_buffer[0];

    float sum_mag = 0;
    for (int i = 0; i < ACC_COUNT; i++) {
        float mag = sqrt(acc_x[i]*acc_x[i] +
                          acc_y[i]*acc_y[i] +
                          acc_z[i]*acc_z[i]);
        sum_mag += mag;
    }

    float mean_acc = sum_mag / ACC_COUNT;

    float var_acc = 0;
    for (int i = 0; i < ACC_COUNT; i++) {
        float mag = sqrt(acc_x[i]*acc_x[i] +
                          acc_y[i]*acc_y[i] +
                          acc_z[i]*acc_z[i]);
        var_acc += pow(mag - mean_acc, 2);
    }
    var_acc /= ACC_COUNT;

    int state = predictState(mean_eda, std_eda,
                             mean_acc, var_acc,
                             eda_slope);

    if (state == 0)
        printf("STRESS DETECTED\n");
    else if (state == 1)
        printf("Amusement Detected\n");
    else
        printf("Calm State\n");
}
