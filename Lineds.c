#include "Lineds.h"
#include <CarMaker.h>
#include "Vehicle/Sensor_Line.h"

/*  
** call in User_DeclQuants ()
*/   

void
Lineds_DeclQuants (void)
{
	const char* variableNames[3] = { "x", "y", "z" };
	for (int i = 0; i < 100; i++) {
        for (int j = 0; j < 3; j++) {
            // 动态生成变量名
            char UAQ[20];
            sprintf(UAQ, "LineL1_p%d_%s", i+1, variableNames[j]);

            // 动态生成指针
            double* variablePointer = &(Lds.L1.p[i].x) + j; 

            // 定义变量
            DDefDouble4(NULL, UAQ, "m", variablePointer, DVA_None);
        }
    }
	for (int i = 0; i < 100; i++) {
        for (int j = 0; j < 3; j++) {
            // 动态生成变量名
            char UAQ[20];
            sprintf(UAQ, "LineL2_p%d_%s", i+1, variableNames[j]);

            // 动态生成指针
            double* variablePointer = &(Lds.L2.p[i].x) + j; 

            // 定义变量
            DDefDouble4(NULL, UAQ, "m", variablePointer, DVA_None);
        }
    }
	for (int i = 0; i < 100; i++) {
        for (int j = 0; j < 3; j++) {
            // 动态生成变量名
            char UAQ[20];
            sprintf(UAQ, "LineR1_p%d_%s", i+1, variableNames[j]);

            // 动态生成指针
            double* variablePointer = &(Lds.R1.p[i].x) + j; 

            // 定义变量
            DDefDouble4(NULL, UAQ, "m", variablePointer, DVA_None);
        }
    }
	for (int i = 0; i < 100; i++) {
        for (int j = 0; j < 3; j++) {
            // 动态生成变量名
            char UAQ[20];
            sprintf(UAQ, "LineR2_p%d_%s", i+1, variableNames[j]);

            // 动态生成指针
            double* variablePointer = &(Lds.R2.p[i].x) + j; 

            // 定义变量
            DDefDouble4(NULL, UAQ, "m", variablePointer, DVA_None);
        }
    }

   
}


/*
** Lineds_TestRun_Start_atEnd ()
**
** initialises struct at the start of a new TestRun
**
** call in User_TestRun_Start_atEnd ()
*/
int
Lineds_TestRun_Start_atEnd (void)
{
	for (int i = 0; i < 100; i++) {
        for (int j = 0; j < 3; j++) {
			 // 获取当前点的指针
            double* coordPtr = &(Lds.L1.p[i].x)  + j;
			*coordPtr = 0;
		}
	}
	for (int i = 0; i < 100; i++) {
        for (int j = 0; j < 3; j++) {
			 // 获取当前点的指针
            double* coordPtr = &(Lds.L2.p[i].x)  + j;
			*coordPtr = 0;
		}
	}
	for (int i = 0; i < 100; i++) {
        for (int j = 0; j < 3; j++) {
			 // 获取当前点的指针
            double* coordPtr = &(Lds.R1.p[i].x)  + j;
			*coordPtr = 0;
		}
	}
	for (int i = 0; i < 100; i++) {
        for (int j = 0; j < 3; j++) {
			 // 获取当前点的指针
            double* coordPtr = &(Lds.R2.p[i].x)  + j;
			*coordPtr = 0;
		}
	}

   
     
    return 0;
}    
     
     
/*  
** call in User_Calc ()
*/   
     
int  
Lineds_Calc (double dt)
{    
     
    /*Execute only during simulation*/
    if (SimCore.State != SCState_Simulate) return 0;
     
    /*Execute only if at least 1 line is detected on the left or  right side*/
    if (LineSensor[0].RLines.nLine == 0 || LineSensor[0].LLines.nLine == 0) {
		for (int i = 0; i < 100; i++) {
        	for (int j = 0; j < 3; j++) {
			 	// 获取当前点的指针
            	double* coordPtr = &(Lds.L1.p[i].x)  + j;
				*coordPtr = 0;
			}
		}
		for (int i = 0; i < 100; i++) {
        	for (int j = 0; j < 3; j++) {
			 	// 获取当前点的指针
            	double* coordPtr = &(Lds.L2.p[i].x)  + j;
				*coordPtr = 0;
			}
		}
		for (int i = 0; i < 100; i++) {
        	for (int j = 0; j < 3; j++) {
			 	// 获取当前点的指针
            	double* coordPtr = &(Lds.R1.p[i].x)  + j;
				*coordPtr = 0;
			}
		}
		for (int i = 0; i < 100; i++) {
        	for (int j = 0; j < 3; j++) {
			 	// 获取当前点的指针
            	double* coordPtr = &(Lds.R2.p[i].x)  + j;
				*coordPtr = 0;
			}
		}

    

        return 0;
    };

		for (int i = 0; i < 100; i++) {
        	for (int j = 0; j < 3; j++) {
			 	// 获取当前点的指针
            	double* coordPtr = &(Lds.L1.p[i].x)  + j;
				*coordPtr = LineSensor[0].LLines.L[0].ds[i][j];
			}
		}
		for (int i = 0; i < 100; i++) {
        	for (int j = 0; j < 3; j++) {
			 	// 获取当前点的指针
            	double* coordPtr = &(Lds.L2.p[i].x)  + j;
				*coordPtr = LineSensor[0].LLines.L[1].ds[i][j];
			}
		}
		for (int i = 0; i < 100; i++) {
        	for (int j = 0; j < 3; j++) {
			 	// 获取当前点的指针
            	double* coordPtr = &(Lds.R1.p[i].x)  + j;
				*coordPtr = LineSensor[0].RLines.L[0].ds[i][j];
			}
		}
		for (int i = 0; i < 100; i++) {
        	for (int j = 0; j < 3; j++) {
			 	// 获取当前点的指针
            	double* coordPtr = &(Lds.R2.p[i].x)  + j;
				*coordPtr = LineSensor[0].RLines.L[1].ds[i][j];
			}
		}

        
        return 0;
}

