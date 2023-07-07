typedef struct tLds tLds;

struct tLds {

    struct {
        struct {
            double x;
            double y;
            double z;
        } p[100];
    } L1, L2, R1, R2;

};

extern tLds Lds;

int		Lineds_TestRun_Start_atEnd	(void);
void	Lineds_DeclQuants			(void);
int		Lineds_Calc					(double dt);