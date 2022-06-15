# TIFX04-LEMA-DataProcessing
Data processing for our Bachelor thesis in applied physics (TIFX04-22-82) where we built and optimized a linear electromagnetic accelerator (LEMA).


In ==dataProcessing.py== CSV-files containing measurements are read. Then the data is processed based on the type of data.

"S_analysis" means analysis of 10 measurements taken directly after each other. 

"I_coils_analysis" is the current (I) through all coils for one measurement.

"DX_stage2_analysis" measurements for stage 2, X-position of sensor (diode)

"eta_calc" and "eta_calc_per_stage" is the efficiency of the LEMA.
