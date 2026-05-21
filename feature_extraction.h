#ifndef FEATURE_EXTRACTION_H
#define FEATURE_EXTRACTION_H

#ifdef __cplusplus
extern "C" {
#endif

void processAndPredict();

#ifdef __cplusplus
}
#endif

// Constants
extern const int WINDOW_SIZE;
extern const int FS_EDA;
extern const int FS_ACC;
extern const int EDA_COUNT;
extern const int ACC_COUNT;

// Sensor buffers
extern float eda_buffer[];
extern float acc_x[];
extern float acc_y[];
extern float acc_z[];

// Main processing function
void processAndPredict();

#endif  // FEATURE_EXTRACTION_H
