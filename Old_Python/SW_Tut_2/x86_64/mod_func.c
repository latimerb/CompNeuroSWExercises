#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;

extern void _k_reg(void);
extern void _leak_reg(void);
extern void _na_reg(void);
extern void _VVClamp_reg(void);

void modl_reg(){
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");

    fprintf(stderr," k.mod");
    fprintf(stderr," leak.mod");
    fprintf(stderr," na.mod");
    fprintf(stderr," VVClamp.mod");
    fprintf(stderr, "\n");
  }
  _k_reg();
  _leak_reg();
  _na_reg();
  _VVClamp_reg();
}
